from django.db import transaction
from django.db.models import F
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from xii.django_river.models import TransitionApprovalMeta

from xii.django_river_admin.views import get, post, delete
from xii.django_river_admin.views.serializers import RePrioritizeTransitionApprovalMetaDto, TransitionApprovalMetaDto, CreateTransitionApprovalMetaDto, ApprovalHookDto

# TransitionApprovalMetaDto nests `permissions` and `groups` as full
# many=True serializers - each is a many-to-many, so without
# prefetch_related every row issues 2 extra queries when serialized (one
# per M2M), an N+1 that select_related can't fix (that's for FKs/o2o only).
_transition_approval_metas = TransitionApprovalMeta.objects.prefetch_related("permissions", "groups")


@get(r'^transition-approval-meta/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    transition_approval_meta = get_object_or_404(_transition_approval_metas, pk=pk)
    return Response(TransitionApprovalMetaDto(transition_approval_meta).data, status=HTTP_200_OK)


@get(r'^transition-approval-meta/list/$')
def list_it(request):
    return Response(TransitionApprovalMetaDto(_transition_approval_metas.all(), many=True).data, status=HTTP_200_OK)


@delete(r'^transition-approval-meta/delete/(?P<pk>\w+)/$', permission='xii_django_river.delete_transitionapprovalmeta')
def delete_it(request, pk):
    transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=pk)
    transition_approval_meta.delete()
    return Response(status=HTTP_200_OK)


@post(r'^transition-approval-meta/create/$', permission='xii_django_river.add_transitionapprovalmeta')
def create_it(request):
    create_transition_approval_meta_request = CreateTransitionApprovalMetaDto(data=request.data)
    if create_transition_approval_meta_request.is_valid():
        transition_approval_meta = create_transition_approval_meta_request.save()
        return Response({"id": transition_approval_meta.id}, status=HTTP_200_OK)
    else:
        return Response(create_transition_approval_meta_request.errors, status=HTTP_400_BAD_REQUEST)


@transaction.atomic
@post(r'^transition-approval-meta/re-prioritize/', permission='xii_django_river.change_transitionapprovalmeta')
def re_prioritize_it(request):
    re_prioritize_transition_approval_meta_request = RePrioritizeTransitionApprovalMetaDto(data=request.data, many=True)
    if re_prioritize_transition_approval_meta_request.is_valid():

        request_map = {
            reprioritize_request["transition_approval_meta_id"]: reprioritize_request["priority"]
            for reprioritize_request in re_prioritize_transition_approval_meta_request.validated_data
        }

        TransitionApprovalMeta.objects.filter(pk__in=request_map.keys()).update(priority=F('priority') + len(request_map.keys()) * 10)
        for transition_approval_meta_id, priority in request_map.items():
            transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=transition_approval_meta_id)
            transition_approval_meta.priority = priority
            transition_approval_meta.save()

        return Response(status=HTTP_200_OK)
    else:
        return Response(re_prioritize_transition_approval_meta_request.errors, status=HTTP_400_BAD_REQUEST)


@get(r'^transition-approval-meta/approval-hook/list/(?P<transition_approval_meta_id>\w+)/$')
def list_approval_hooks(request, transition_approval_meta_id):
    transition_approval_meta = get_object_or_404(TransitionApprovalMeta.objects.all(), pk=transition_approval_meta_id)
    return Response(
        ApprovalHookDto(
            # ApprovalHookDto nests callback_function as a full FunctionDto,
            # which itself nests created_by/updated_by/approved_by - without
            # this, each hook row costs 4 extra queries when serialized.
            transition_approval_meta.on_approved_hooks.filter(
                transition_approval__isnull=True, object_id__isnull=True
            ).select_related(
                "callback_function", "callback_function__created_by",
                "callback_function__updated_by", "callback_function__approved_by",
            ),
            many=True
        ).data,
        status=HTTP_200_OK
    )
