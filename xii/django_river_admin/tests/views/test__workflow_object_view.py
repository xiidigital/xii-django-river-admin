from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from hamcrest import assert_that, equal_to, has_length
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from xii.django_river.models import State, Workflow
from xii.django_river_admin.tests.models import WorkflowObjectTestModel

User = get_user_model()


class WorkflowObjectViewTest(TestCase):
    """
    workflow_object_view.py operates on whatever arbitrary model a
    Workflow's content_type points at (a user's own business model, not
    one of river's own) - WorkflowObjectTestModel is a stand-in for that.
    See its docstring for why it uses a plain FK instead of StateField.
    """

    def setUp(self):
        self.initial_state = State.objects.create(label="state1")
        content_type = ContentType.objects.get_for_model(WorkflowObjectTestModel)
        self.workflow = Workflow.objects.create(
            field_name="my_field", content_type=content_type, initial_state=self.initial_state
        )
        self.workflow_object = WorkflowObjectTestModel.objects.create(test_field="hello", my_field=self.initial_state)

        # All the read endpoints below only need IsAuthenticated (no
        # specific Django permission) - the delete tests further down log
        # in their own users since they need delete_workflowobjecttestmodel
        # (or deliberately don't, to check the 403 case).
        reader = User.objects.create_user(username="reader")
        self.client.force_login(reader)

    def test__shouldReturnNotFoundWhenWorkflowDoesNotExist(self):
        response = self.client.get('/workflow-object/identify/999/%d/' % self.workflow_object.pk)
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnNotFoundWhenObjectDoesNotExist(self):
        response = self.client.get('/workflow-object/identify/%d/999/' % self.workflow.pk)
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldIdentifyWorkflowObjectByItsStringRepresentation(self):
        response = self.client.get('/workflow-object/identify/%d/%d/' % (self.workflow.pk, self.workflow_object.pk))
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, equal_to(str(self.workflow_object)))

    def test__shouldReturnCurrentState(self):
        response = self.client.get(
            '/workflow-object/current-state/%d/%d/' % (self.workflow.pk, self.workflow_object.pk)
        )
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data["label"], equal_to(self.initial_state.label))

    def test__shouldReturnCurrentIterationAsZeroBeforeAnyTransition(self):
        response = self.client.get(
            '/workflow-object/current-iteration/%d/%d/' % (self.workflow.pk, self.workflow_object.pk)
        )
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, equal_to(0))

    def test__shouldReturnEmptyStateHistoryBeforeAnyTransition(self):
        response = self.client.get(
            '/workflow-object/state/list/%d/%d/' % (self.workflow.pk, self.workflow_object.pk)
        )
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnEmptyTransitionListBeforeAnyTransition(self):
        response = self.client.get(
            '/workflow-object/transition/list/%d/%d/' % (self.workflow.pk, self.workflow_object.pk)
        )
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnEmptyTransitionApprovalListBeforeAnyTransition(self):
        response = self.client.get(
            '/workflow-object/transition-approval/list/%d/%d/' % (self.workflow.pk, self.workflow_object.pk)
        )
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnNotFoundWhenDeletingAnInexistentWorkflowObject(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_workflowobjecttestmodel"))
        self.client.force_login(user)

        response = self.client.delete('/workflow-object/delete/%d/999/' % self.workflow.pk)
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteWorkflowObjectWhenUserHasThePermissionOnItsOwnModel(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_workflowobjecttestmodel"))
        self.client.force_login(user)

        response = self.client.delete('/workflow-object/delete/%d/%d/' % (self.workflow.pk, self.workflow_object.pk))
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(WorkflowObjectTestModel.objects.filter(pk=self.workflow_object.pk).exists(), equal_to(False))

    def test__shouldRejectDeleteWithoutPermissionOnTheWorkflowObjectsOwnModel(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        response = self.client.delete('/workflow-object/delete/%d/%d/' % (self.workflow.pk, self.workflow_object.pk))
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(WorkflowObjectTestModel.objects.filter(pk=self.workflow_object.pk).exists(), equal_to(True))
