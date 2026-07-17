from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from xii.django_river.models import Workflow, DONE

from xii.django_river_admin.views import get, delete
from xii.django_river_admin.views.serializers import StateDto, WorkflowObjectStateDto, TransitionDto, TransitionApprovalDto


@get(r'^workflow-object/identify/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_identifier(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)
    return Response(str(workflow_object), status=status.HTTP_200_OK)


@get(r'^workflow-object/current-state/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_current_state(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    current_state = getattr(workflow_object, workflow.field_name)
    return Response(StateDto(current_state).data, status=status.HTTP_200_OK)


@get(r'^workflow-object/current-iteration/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def get_current_iteration(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    current_state = getattr(workflow_object, workflow.field_name)
    iterations = workflow.transitions.filter(
        workflow=workflow,
        object_id=workflow_object.pk,
        destination_state=current_state,
        status=DONE
    ).values_list("iteration", flat=True)

    last_iteration = max(iterations) + 1 if iterations else 0
    return Response(last_iteration, status=status.HTTP_200_OK)


@delete(r'^workflow-object/delete/(?P<workflow_pk>\w+)/(?P<object_id>\w+)/$')
def delete_it(request, workflow_pk, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_pk)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    # Permission is checked against the business object's own model/app
    # here, not via a static `permission=` kwarg on @delete - unlike the
    # river-owned models above (Workflow, State, Function, ...),
    # `model_class` is whatever the caller's app registered the workflow
    # field on, so the right permission (<app_label>.delete_<model_name>)
    # can only be known once the object is resolved. No object is passed to
    # has_perm() here: Django's default ModelBackend doesn't do per-object
    # permission checks (that needs a third-party backend like
    # django-guardian) - passing one in just makes has_perm() return False
    # unconditionally, permission or not.
    delete_permission = "%s.delete_%s" % (model_class._meta.app_label, model_class._meta.model_name)
    if not request.user.has_perm(delete_permission):
        return Response(status=status.HTTP_403_FORBIDDEN)

    workflow_object.delete()
    return Response(status=status.HTTP_200_OK)


@get(r'^workflow-object/state/list/(?P<workflow_id>\w+)/(?P<object_id>\w+)/$')
def list_states(request, workflow_id, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    states = []
    processed_states = []
    # select_related: source_state/destination_state are read directly
    # below and also end up in WorkflowObjectStateDto (StateDto) - without
    # it, each transition costs 2 extra queries.
    for transition in workflow.transitions.filter(object_id=workflow_object.pk).select_related("source_state", "destination_state"):
        source_iteration = transition.iteration - 1
        destination_iteration = transition.iteration

        source_state_key = str(source_iteration) + str(transition.source_state.pk)
        if source_state_key not in processed_states:
            states.append({"iteration": source_iteration, "state": transition.source_state})
            processed_states.append(source_state_key)

        destination_state_key = str(destination_iteration) + str(transition.destination_state.pk)
        if destination_state_key not in processed_states:
            states.append({"iteration": destination_iteration, "state": transition.destination_state})
            processed_states.append(destination_state_key)

    return Response(WorkflowObjectStateDto(states, many=True).data, status=HTTP_200_OK)


@get(r'^workflow-object/transition/list/(?P<workflow_id>\w+)/(?P<object_id>\w+)/$')
def list_transitions(request, workflow_id, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    return Response(TransitionDto(workflow.transitions.filter(object_id=workflow_object.pk), many=True).data, status=HTTP_200_OK)


@get(r'^workflow-object/transition-approval/list/(?P<workflow_id>\w+)/(?P<object_id>\w+)/$')
def list_transition_approvals(request, workflow_id, object_id):
    workflow = get_object_or_404(Workflow.objects.all(), pk=workflow_id)
    model_class = workflow.content_type.model_class()
    workflow_object = get_object_or_404(model_class.objects.all(), pk=object_id)

    # TransitionApprovalDto nests transactioner (UserDto) and permissions/
    # groups (M2M, many=True) - select_related for the FK, prefetch_related
    # for the M2Ms, otherwise each row costs 3 extra queries.
    approvals = workflow.transition_approvals.filter(object_id=workflow_object.pk) \
        .select_related("transactioner").prefetch_related("permissions", "groups")
    return Response(TransitionApprovalDto(approvals, many=True).data, status=HTTP_200_OK)
