from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from xii.django_river.core.workflowregistry import workflow_registry
from xii.django_river.models import Workflow, State

from xii.django_river_admin import site as river_admin_site, DefaultRiverAdmin
from xii.django_river_admin.views import get, post, delete
from xii.django_river_admin.views.serializers import WorkflowStateFieldDto, CreateWorkflowDto, WorkflowDto, \
    TransitionMetaDto, TransitionDto, WorkflowMetadataDto, StateDto

# WorkflowDto nests content_type and initial_state as full objects, and
# both are also read directly below (content_type.model_class() to filter
# out workflows whose model no longer exists) - without select_related,
# each of those is a separate query per row, an N+1 that scales with
# however many Workflows exist.
_workflows = Workflow.objects.select_related("content_type", "initial_state")


@get(r'^workflow/get/(?P<pk>\w+)/$')
def get_it(request, pk):
    workflow = get_object_or_404(_workflows, pk=pk)
    return Response(WorkflowDto(workflow).data, status=HTTP_200_OK)


@get(r'^workflow/list/$')
def list_it(request):
    valid_workflows = [workflow for workflow in _workflows.all() if workflow.content_type.model_class()]
    return Response(WorkflowDto(valid_workflows, many=True).data, status=HTTP_200_OK)


@post(r'^workflow/create/$', permission='xii_django_river.add_workflow')
def create_it(request):
    create_workflow_request = CreateWorkflowDto(data=request.data)
    if create_workflow_request.is_valid():
        workflow = create_workflow_request.save()
        return Response({"id": workflow.id}, status=HTTP_200_OK)
    else:
        return Response(create_workflow_request.errors, status=HTTP_400_BAD_REQUEST)


@delete(r'^workflow/delete/(?P<pk>\w+)/$', permission='xii_django_river.delete_workflow')
def delete_it(request, pk):
    workflow = get_object_or_404(Workflow.objects.all(), pk=pk)
    workflow.delete()
    return Response(status=HTTP_200_OK)


@get(r'^workflow/state-field/list/$')
def list_available_state_fields(request):
    # workflow_registry.workflows is keyed directly by the model class itself
    # (see xii.django_river.core.workflowregistry.WorkflowRegistry) since
    # river moved away from indexing by id(cls) - no separate class lookup
    # needed anymore.
    result = []
    for cls, field_names in workflow_registry.workflows.items():
        content_type = ContentType.objects.get_for_model(cls)
        for field_name in field_names:
            if not Workflow.objects.filter(content_type=content_type, field_name=field_name).exists():
                result.append(
                    {
                        "content_type": content_type,
                        "field_name": field_name
                    })

    return Response(WorkflowStateFieldDto(result, many=True).data, status=HTTP_200_OK)


@get(r'^workflow/state/list/(?P<workflow_id>\w+)/$')
def list_states(request, workflow_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    state_ids = set()
    state_ids.add(workflow.initial_state.pk)
    for source_state_id, destination_state_id in workflow.transition_metas.values_list("source_state__pk", "destination_state__pk"):
        state_ids.add(source_state_id)
        state_ids.add(destination_state_id)

    return Response(StateDto(State.objects.filter(pk__in=state_ids), many=True).data, status=HTTP_200_OK)


@get(r'^workflow/transition-meta/list/(?P<workflow_id>\w+)/$')
def list_transition_meta(request, workflow_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)

    return Response(TransitionMetaDto(workflow.transition_metas.all(), many=True).data, status=HTTP_200_OK)


@get(r'^workflow/transition/list/(?P<workflow_id>\w+)/$')
def list_transitions(request, workflow_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    return Response(TransitionDto(workflow.transitions.all(), many=True).data, status=HTTP_200_OK)


@get(r'^workflow/object/list/(?P<workflow_pk>\w+)/$')
def list_workflow_objects(request, workflow_pk):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    registered_admin = river_admin_site.get(model_class, workflow.field_name, DefaultRiverAdmin.of(model_class, workflow.field_name))
    return Response({"headers": registered_admin.admin_list_displays, "workflow_objects": list(registered_admin.get_objects())}, status=HTTP_200_OK)


@get(r'^workflow/metadata/$')
def get_workflow_metadata(request):
    workflows = []
    for workflow in _workflows.all():
        model_class = workflow.content_type.model_class()
        if model_class:
            registered_admin = river_admin_site.get(model_class, workflow.field_name, DefaultRiverAdmin.of(model_class, workflow.field_name))
            workflows.append({"id": workflow.id, "name": registered_admin.admin_name, "icon": registered_admin.admin_icon})

    return Response(WorkflowMetadataDto(workflows, many=True).data, status=HTTP_200_OK)
