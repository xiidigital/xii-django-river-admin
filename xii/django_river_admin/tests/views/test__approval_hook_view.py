import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, not_none, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_403_FORBIDDEN
from xii.django_river.models import State, OnApprovedHook, Workflow, TransitionMeta, TransitionApprovalMeta, Function

from xii.django_river_admin.tests.helpers import make_approved_function

User = get_user_model()


class ApprovalHookViewTest(TestCase):

    def test__shouldCreateApprovalHook(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_onapprovedhook"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        function = make_approved_function(Function, "test-function-1")
        response = self.client.post('/approval-hook/create/', json.dumps({
            "workflow": workflow.id,
            "content_type": content_type.id,
            "transition_approval_meta": transition_approval_meta.id,
            "callback_function": function.id,
            "transition_approval": None,
            "object_id": None

        }), content_type='application/json')

        assert_that(response.status_code, equal_to(HTTP_200_OK))

        created_approval_hook = OnApprovedHook.objects.first()
        assert_that(created_approval_hook, not_none())
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(created_approval_hook.pk)))

    def test__shouldRejectCreateWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        function = make_approved_function(Function, "test-function-1")
        response = self.client.post('/approval-hook/create/', json.dumps({
            "workflow": workflow.id,
            "content_type": content_type.id,
            "transition_approval_meta": transition_approval_meta.id,
            "callback_function": function.id,
            "transition_approval": None,
            "object_id": None

        }), content_type='application/json')

        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(OnApprovedHook.objects.first(), is_(none()))

    def test__shouldReturnNotFoundWhenAnInexistentApprovalHookIsRequestedToDelete(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_onapprovedhook"))
        self.client.force_login(user)

        response = self.client.delete('/approval-hook/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteApprovalHook(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_onapprovedhook"))
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        function = make_approved_function(Function, "test-function-1")

        approval_hook = OnApprovedHook.objects.create(workflow=workflow, callback_function=function, transition_approval_meta=transition_approval_meta)

        response = self.client.delete('/approval-hook/delete/%d/' % approval_hook.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(OnApprovedHook.objects.filter(pk=approval_hook.id).first(), is_(none()))

    def test__shouldRejectDeleteWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        initial_state = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        content_type = ContentType.objects.first()
        workflow = Workflow.objects.create(initial_state=initial_state, content_type=content_type, field_name="test-field")
        transition_meta = TransitionMeta.objects.create(workflow=workflow, source_state=initial_state, destination_state=state_2)

        transition_approval_meta = TransitionApprovalMeta.objects.create(workflow=workflow, transition_meta=transition_meta, priority=1)
        function = make_approved_function(Function, "test-function-1")

        approval_hook = OnApprovedHook.objects.create(workflow=workflow, callback_function=function, transition_approval_meta=transition_approval_meta)

        response = self.client.delete('/approval-hook/delete/%d/' % approval_hook.id)
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(OnApprovedHook.objects.filter(pk=approval_hook.id).first(), not_none())
