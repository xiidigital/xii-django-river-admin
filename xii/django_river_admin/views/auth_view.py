from django.contrib.auth.models import Permission, Group
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle

from xii.django_river_admin.views import get
from xii.django_river_admin.views.serializers import PermissionDto, GroupDto, UserDto


class LoginRateThrottle(AnonRateThrottle):
    """
    DRF's built-in ObtainAuthToken has no throttling at all by default -
    without this, /api-token-auth/ allows unlimited password guesses per
    IP. Scoped separately from any other 'anon' throttle the project might
    configure, so tuning login-attempt limits doesn't also affect
    unrelated anonymous traffic (there mostly isn't any here, since every
    other endpoint requires IsAuthenticated - see REST_FRAMEWORK settings -
    but this keeps the two independently configurable regardless).
    """
    scope = "login"


class ThrottledObtainAuthToken(ObtainAuthToken):
    throttle_classes = [LoginRateThrottle]


@get(r'^permission/get/(?P<pk>\w+)/$')
def get_permission(request, pk):
    permission = get_object_or_404(Permission.objects.all(), pk=pk)
    return Response(PermissionDto(permission).data, status=HTTP_200_OK)


@get(r'^permission/list/$')
def list_permissions(request):
    return Response(PermissionDto(Permission.objects.all(), many=True).data, status=HTTP_200_OK)


@get(r'^group/get/(?P<pk>\w+)/$')
def get_group(request, pk):
    group = get_object_or_404(Group.objects.all(), pk=pk)
    return Response(GroupDto(group).data, status=HTTP_200_OK)


@get(r'^group/list/$')
def list_group(request):
    return Response(GroupDto(Group.objects.all(), many=True).data, status=HTTP_200_OK)


@get(r'^user/get/$')
def get_user_profile(request):
    return Response(UserDto(request.user).data, status=HTTP_200_OK)


@get(r'^user/has_river_permission/(?P<operation>\w+)/(?P<object_type>\w+)/$')
def has_river_permission(request, operation, object_type):
    """
    "approve" is handled separately from the standard add/change/delete/view
    operations: it doesn't map onto Django's default per-model permissions
    (there's no "approve_<object_type>" for arbitrary models) - it only
    exists as the custom xii_django_river.approve_function permission
    (see xii.django_river.models.function.Function.Meta.permissions), so
    object_type is ignored for it. This is only reachable for "function"
    from the UI (auth.js's APPROVE/FUNCTION pair), but the check itself
    doesn't need to enforce that.
    """
    standard_operations = ["add", "change", "delete", "view"]
    if operation == "approve":
        return Response(request.user.has_perm("xii_django_river.approve_function"), status=HTTP_200_OK)
    elif operation in standard_operations:
        return Response(request.user.has_perm("xii_django_river.%s_%s" % (operation, object_type)), status=HTTP_200_OK)
    else:
        return Response({"message": "Invalid operation '%s'. Available operations are '%s'" % (operation, standard_operations + ["approve"])}, status=HTTP_400_BAD_REQUEST)
