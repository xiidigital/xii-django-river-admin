import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, has_property, is_, none, not_none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from xii.django_river.models import State, Workflow, TransitionMeta, TransitionApprovalMeta, OnApprovedHook, Function

from xii.django_river_admin.tests.helpers import make_approved_function

User = get_user_model()


class TransitionApprovalMetaViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentTransitionApprovalMetaIsRequested(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        response = self.client.get('/transition-approval-meta/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnTransitionApprovalMeta(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        response = self.client.get('/transition-approval-meta/get/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(transition_approval_meta.id)))
        assert_that(response.data, has_entry("workflow", equal_to(workflow.id)))
        assert_that(response.data, has_entry("transition_meta", equal_to(transition_meta.id)))
        assert_that(response.data, has_entry("priority", equal_to(transition_approval_meta.priority)))
        assert_that(response.data, has_entry("permissions", has_length(0)))
        assert_that(response.data, has_entry("groups", has_length(0)))

    def test__shouldReturnEmptyListWhenThereIsNoTransitionApprovalMeta(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        response = self.client.get('/transition-approval-meta/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfTransitionApprovalMeta(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")
        state_3 = State.objects.create(label="state-3")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta_1 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        transition_meta_2 = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_3)

        transition_approval_meta_1 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta_1, priority=0)
        transition_approval_meta_2 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta_2, priority=0)

        response = self.client.get('/transition-approval-meta/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_approval_meta_1.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("transition_meta", equal_to(transition_meta_1.id)),
                    has_entry("priority", equal_to(transition_approval_meta_1.priority)),
                    has_entry("permissions", has_length(0)),
                    has_entry("groups", has_length(0))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(transition_approval_meta_2.id)),
                    has_entry("workflow", equal_to(workflow.id)),
                    has_entry("transition_meta", equal_to(transition_meta_2.id)),
                    has_entry("priority", equal_to(transition_approval_meta_2.priority)),
                    has_entry("permissions", has_length(0)),
                    has_entry("groups", has_length(0))
                )
            )
        )

    def test__shouldNotCreateTransitionApprovalMetaWhenWorkflowIsMissing(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_transitionapprovalmeta"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        response = self.client.post('/transition-approval-meta/create/', data={"transition_meta": transition_meta.id, "permissions": [], "groups": [], "priority": 0})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateTransitionApprovalMetaWhenTransitionMetaIsMissing(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_transitionapprovalmeta"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "permissions": [], "groups": [], "priority": 0})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateTransitionApprovalMetaEvenPriorityIsMissing(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_transitionapprovalmeta"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)
        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "transition_meta": transition_meta.id, "permissions": [], "groups": []})
        assert_that(response.status_code, equal_to(HTTP_200_OK))

        created_transition_approval_meta = TransitionApprovalMeta.objects.first()
        assert_that(response.data, has_entry("id", equal_to(created_transition_approval_meta.pk)))
        assert_that(created_transition_approval_meta, has_property("priority", equal_to(0)))

    def test__shouldCreateTransitionApprovalMetaWithGivenPriority(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_transitionapprovalmeta"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "transition_meta": transition_meta.id, "permissions": [], "groups": [], "priority": 5})
        assert_that(response.status_code, equal_to(HTTP_200_OK))

        created_transition_approval_meta = TransitionApprovalMeta.objects.first()
        assert_that(response.data, has_entry("id", equal_to(created_transition_approval_meta.pk)))
        assert_that(created_transition_approval_meta, has_property("priority", equal_to(5)))

    def test__shouldRejectCreateWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        response = self.client.post('/transition-approval-meta/create/', data={"workflow": workflow.id, "transition_meta": transition_meta.id, "permissions": [], "groups": [], "priority": 5})
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(TransitionApprovalMeta.objects.filter(workflow=workflow).first(), is_(none()))

    def test__shouldReturnNotFoundWhenAnInexistentTransitionApprovalMetaIsRequestedToDelete(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_transitionapprovalmeta"))
        self.client.force_login(user)

        response = self.client.delete('/transition-approval-meta/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteTransitionApprovalMeta(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_transitionapprovalmeta"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        response = self.client.delete('/transition-approval-meta/delete/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(TransitionApprovalMeta.objects.filter(id=transition_approval_meta.id).first(), is_(none()))

    def test__shouldRejectDeleteWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=0)

        response = self.client.delete('/transition-approval-meta/delete/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(TransitionApprovalMeta.objects.filter(id=transition_approval_meta.id).first(), not_none())

    def test__shouldRePrioritizeTransitionApprovalMeta(self):
        user = User.objects.create_user(username="reprioritizer")
        user.user_permissions.add(Permission.objects.get(codename="change_transitionapprovalmeta"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta_1 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        transition_approval_meta_2 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=2)
        response = self.client.post('/transition-approval-meta/re-prioritize/', json.dumps([
            {"transition_approval_meta_id": transition_approval_meta_1.id, "priority": 50},
            {"transition_approval_meta_id": transition_approval_meta_2.id, "priority": 40}
        ]), content_type='application/json')

        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(TransitionApprovalMeta.objects.get(pk=transition_approval_meta_1.pk), has_property("priority", equal_to(50)))
        assert_that(TransitionApprovalMeta.objects.get(pk=transition_approval_meta_2.pk), has_property("priority", equal_to(40)))

    def test__shouldRejectRePrioritizeWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta_1 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        transition_approval_meta_2 = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=2)
        response = self.client.post('/transition-approval-meta/re-prioritize/', json.dumps([
            {"transition_approval_meta_id": transition_approval_meta_1.id, "priority": 50},
            {"transition_approval_meta_id": transition_approval_meta_2.id, "priority": 40}
        ]), content_type='application/json')

        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(TransitionApprovalMeta.objects.get(pk=transition_approval_meta_1.pk), has_property("priority", equal_to(1)))
        assert_that(TransitionApprovalMeta.objects.get(pk=transition_approval_meta_2.pk), has_property("priority", equal_to(2)))

    def test__shouldReturnEmptyListWhenThereIsNoApprovalHooks(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)

        response = self.client.get('/transition-approval-meta/approval-hook/list/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfApprovalHooks(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        function_1 = make_approved_function(Function, "test-function-1")
        function_2 = make_approved_function(Function, "test-function-2")

        approval_hook_1 = OnApprovedHook.objects.create(workflow=workflow, callback_function=function_1, transition_approval_meta=transition_approval_meta)
        approval_hook_2 = OnApprovedHook.objects.create(workflow=workflow, callback_function=function_2, transition_approval_meta=transition_approval_meta)

        response = self.client.get('/transition-approval-meta/approval-hook/list/%d/' % transition_approval_meta.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(approval_hook_1.id)),
                    has_entry("callback_function", all_of(
                        has_entry("id", equal_to(function_1.id)),
                        has_entry("name", equal_to(function_1.name)),
                        has_entry("body", equal_to(function_1.body))
                    )),
                    has_entry("transition_approval_meta", equal_to(transition_approval_meta.id)),
                    has_entry("transition_approval", none()),
                    has_entry("object_id", none()),
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(approval_hook_2.id)),
                    has_entry("callback_function", all_of(
                        has_entry("id", equal_to(function_2.id)),
                        has_entry("name", equal_to(function_2.name)),
                        has_entry("body", equal_to(function_2.body))
                    )),
                    has_entry("transition_approval_meta", equal_to(transition_approval_meta.id)),
                    has_entry("transition_approval", none()),
                    has_entry("object_id", none()),
                )
            )
        )
