from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from xii.django_river.models import TransitionApproval, Transition

from xii.django_river_admin.views import get
from xii.django_river_admin.views.serializers import TransitionApprovalDto, ApprovalHookDto


@get(r'^transition-approval/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition_approval = get_object_or_404(TransitionApproval.objects.all(), pk=pk)
    return Response(TransitionApprovalDto(transition_approval).data, status=HTTP_200_OK)


@get(r'^transition-approval/get-by-transition/(?P<transition_id>\w+)/$')
def get_by_transition(request, transition_id):
    transition = get_object_or_404(Transition.objects.all(), pk=transition_id)
    # TransitionApprovalDto nests transactioner (UserDto) and permissions/
    # groups (M2M, many=True) - select_related for the FK, prefetch_related
    # for the M2Ms, otherwise each row costs 3 extra queries.
    return Response(
        TransitionApprovalDto(
            transition.transition_approval.select_related("transactioner").prefetch_related("permissions", "groups")
        ).data,
        status=HTTP_200_OK
    )


@get(r'^transition-approval/approval-hook/list/(?P<transition_approval_id>\w+)/$')
def list_approval_hooks(request, transition_approval_id):
    transition_approval = get_object_or_404(TransitionApproval.objects.all(), pk=transition_approval_id)
    return Response(
        ApprovalHookDto(
            # ApprovalHookDto nests callback_function as a full FunctionDto,
            # which itself nests created_by/updated_by/approved_by - without
            # this, each hook row costs 4 extra queries when serialized.
            transition_approval.meta.on_approved_hooks.filter(
                Q(object_id__isnull=True) | Q(object_id=transition_approval.object_id)
            ).select_related(
                "callback_function", "callback_function__created_by",
                "callback_function__updated_by", "callback_function__approved_by",
            ),
            many=True
        ).data,
        status=HTTP_200_OK
    )
