from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from xii.django_river.models import Transition

from xii.django_river_admin.views import get
from xii.django_river_admin.views.serializers import TransitionDto, TransitionHookDto, TransitionApprovalDto


@get(r'^transition/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition = get_object_or_404(Transition.objects.all(), pk=pk)
    return Response(TransitionDto(transition).data, status=HTTP_200_OK)


@get(r'^transition/transition-approval/list/(?P<transition_id>\w+)/$')
def list_transition_approvals(request, transition_id):
    transition = get_object_or_404(Transition.objects.all(), pk=transition_id)

    # TransitionApprovalDto nests transactioner (UserDto) and permissions/
    # groups (M2M, many=True) - select_related for the FK, prefetch_related
    # for the M2Ms, otherwise each row costs 3 extra queries.
    approvals = transition.transition_approvals.all().order_by("transition", "priority") \
        .select_related("transactioner").prefetch_related("permissions", "groups")
    return Response(TransitionApprovalDto(approvals, many=True).data, status=HTTP_200_OK)


@get(r'^transition/transition-hook/list/(?P<transition_id>\w+)/$')
def list_transition_hooks(request, transition_id):
    transition = get_object_or_404(Transition.objects.all(), pk=transition_id)
    return Response(
        TransitionHookDto(
            # TransitionHookDto nests callback_function as a full FunctionDto,
            # which itself nests created_by/updated_by/approved_by - without
            # this, each hook row costs 4 extra queries when serialized.
            transition.meta.on_transit_hooks.filter(
                Q(object_id__isnull=True) | Q(object_id=transition.object_id)
            ).select_related(
                "callback_function", "callback_function__created_by",
                "callback_function__updated_by", "callback_function__approved_by",
            ),
            many=True
        ).data,
        status=HTTP_200_OK
    )
