from django.core.exceptions import ImproperlyConfigured
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN
from xii.django_river.models import Function

from xii.django_river_admin.views import get, post, put, delete
from xii.django_river_admin.views.serializers import UpdateFunctionDto, CreateFunctionDto, FunctionDto

# FunctionDto nests created_by/updated_by/approved_by as full UserDto
# objects - without select_related, serializing N functions issues 3
# separate queries per row (one per FK) on top of the list query itself,
# an N+1 that scales with however many Functions exist.
_functions = Function.objects.select_related("created_by", "updated_by", "approved_by")


@get(r'^function/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    function = get_object_or_404(_functions, pk=pk)
    return Response(FunctionDto(function).data, status=HTTP_200_OK)


@get(r'^function/list/$')
def list_it(request):
    return Response(FunctionDto(_functions.all(), many=True).data, status=HTTP_200_OK)


@post(r'^function/create/', permission='xii_django_river.add_function')
def create_it(request):
    create_function_request = CreateFunctionDto(data=request.data)
    if create_function_request.is_valid():
        author = request.user if request.user.is_authenticated else None
        function = create_function_request.save(created_by=author, updated_by=author)
        return Response({"id": function.id}, status=HTTP_200_OK)
    else:
        return Response(create_function_request.errors, status=HTTP_400_BAD_REQUEST)


@put(r'^function/update/(?P<pk>\w+)/$', permission='xii_django_river.change_function')
def update_it(request, pk):
    function = get_object_or_404(Function.objects.all(), pk=pk)
    update_function_request = UpdateFunctionDto(data=request.data, instance=function)

    if update_function_request.is_valid():
        # A body edit resets is_approved on the model itself (see
        # xii.django_river.models.function.on_pre_save) - updated_by just
        # needs to be kept current so the self-approval check
        # (Function.approve) has the right "am I the author" answer.
        author = request.user if request.user.is_authenticated else None
        update_function_request.save(updated_by=author)
        return Response({"message": "Function is updated"}, status=HTTP_200_OK)
    else:
        return Response(update_function_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^function/delete/(?P<pk>\w+)/$', permission='xii_django_river.delete_function')
def delete_it(request, pk):
    function = get_object_or_404(Function.objects.all(), pk=pk)
    function.delete()
    return Response(status=HTTP_200_OK)


@post(r'^function/approve/(?P<pk>\w+)/$')
def approve_it(request, pk):
    """
    Exposes xii.django_river.models.Function.approve() - required since
    river's Hook.save() now rejects any callback_function that isn't
    approved (RCE-mitigation gate on db-stored, exec()'d Function bodies).
    Permission checks mirror river's own model-level rule: approving your
    own Function requires xii_django_river.self_approve_function in
    addition to xii_django_river.approve_function; approving someone
    else's only needs the latter.
    """
    function = get_object_or_404(Function.objects.all(), pk=pk)

    if not request.user.has_perm('xii_django_river.approve_function'):
        return Response({"detail": "Missing xii_django_river.approve_function permission."}, status=HTTP_403_FORBIDDEN)

    allow_self_approval = request.user.has_perm('xii_django_river.self_approve_function')
    try:
        function.approve(request.user, allow_self_approval=allow_self_approval)
    except ImproperlyConfigured as e:
        return Response({"detail": str(e)}, status=HTTP_403_FORBIDDEN)

    # Re-fetch through _functions (select_related) rather than serializing
    # `function` directly: approve() just set approved_by to `request.user`
    # in memory, but created_by/updated_by weren't loaded with their
    # related User rows, so FunctionDto would issue 2 extra queries here
    # otherwise.
    return Response(FunctionDto(get_object_or_404(_functions, pk=pk)).data, status=HTTP_200_OK)
