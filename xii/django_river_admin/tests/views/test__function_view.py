from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, not_none, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN
from xii.django_river.models import Function

User = get_user_model()


class FunctionViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentFunctionIsRequested(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        response = self.client.get('/function/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnFunction(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        function = Function.objects.create(name="test-function", body="function-body")
        response = self.client.get('/function/get/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(function.id)))
        assert_that(response.data, has_entry("name", equal_to(function.name)))
        assert_that(response.data, has_entry("body", equal_to(function.body)))

    def test__shouldReturnEmptyListWhenThereIsNoStates(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        response = self.client.get('/function/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfStates(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        function_1 = Function.objects.create(name="test-function-1", body="function-body")
        function_2 = Function.objects.create(name="test-function-2", body="function-body")

        response = self.client.get('/function/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(function_1.id)),
                    has_entry("name", equal_to(function_1.name)),
                    has_entry("body", equal_to(function_1.body))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(function_2.id)),
                    has_entry("name", equal_to(function_2.name)),
                    has_entry("body", equal_to(function_2.body))
                )
            )
        )

    def test__shouldNotCreateFunctionWhenNameIsMissing(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_function"))
        self.client.force_login(user)

        response = self.client.post('/function/create/', data={"body": "function-body"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldNotCreateFunctionWhenBodyIsMissing(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_function"))
        self.client.force_login(user)

        response = self.client.post('/function/create/', data={"name": "test-function"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateFunction(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_function"))
        self.client.force_login(user)

        response = self.client.post('/function/create/', data={"name": "test-function", "body": "function-body"})
        created_function = Function.objects.first()
        assert_that(created_function, not_none())
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(created_function.pk)))

    def test__shouldNotCreateFunctionWhenNameIsDuplicate(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_function"))
        self.client.force_login(user)

        function = Function.objects.create(name="test-function", body="function-body")
        response = self.client.post('/function/create/', data={"name": function.name, "body": "test-body"})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldRejectCreateWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        response = self.client.post('/function/create/', data={"name": "test-function", "body": "function-body"})
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))

    def test__shouldReturnNotFoundWhenAnInexistentFunctionIsRequestedToDelete(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_function"))
        self.client.force_login(user)

        response = self.client.delete('/function/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteState(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_function"))
        self.client.force_login(user)

        function = Function.objects.create(name="test-function", body="function-body")
        response = self.client.delete('/function/delete/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(Function.objects.filter(name=function.name).first(), is_(none()))

    def test__shouldRejectDeleteWithoutPermission(self):
        function = Function.objects.create(name="test-function", body="function-body")
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        response = self.client.delete('/function/delete/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))

    def test__shouldRejectApprovalWithoutPermission(self):
        function = Function.objects.create(name="test-function", body="function-body")
        approver = User.objects.create_user(username="no-perms")
        self.client.force_login(approver)

        response = self.client.post('/function/approve/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        function.refresh_from_db()
        assert_that(function.is_approved, is_(False))

    def test__shouldRejectSelfApprovalWithoutSelfApprovePermission(self):
        author = User.objects.create_user(username="author")
        author.user_permissions.add(Permission.objects.get(codename="approve_function"))
        function = Function.objects.create(name="test-function", body="function-body", created_by=author, updated_by=author)
        self.client.force_login(author)

        response = self.client.post('/function/approve/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        function.refresh_from_db()
        assert_that(function.is_approved, is_(False))

    def test__shouldApproveFunctionOfAnotherUser(self):
        author = User.objects.create_user(username="author")
        function = Function.objects.create(name="test-function", body="function-body", created_by=author, updated_by=author)

        reviewer = User.objects.create_user(username="reviewer")
        reviewer.user_permissions.add(Permission.objects.get(codename="approve_function"))
        self.client.force_login(reviewer)

        response = self.client.post('/function/approve/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("is_approved", equal_to(True)))
        function.refresh_from_db()
        assert_that(function.is_approved, is_(True))
        assert_that(function.approved_by_id, equal_to(reviewer.id))

    def test__shouldSelfApproveFunctionWithSelfApprovePermission(self):
        author = User.objects.create_user(username="author")
        author.user_permissions.add(
            Permission.objects.get(codename="approve_function"),
            Permission.objects.get(codename="self_approve_function"),
        )
        function = Function.objects.create(name="test-function", body="function-body", created_by=author, updated_by=author)
        self.client.force_login(author)

        response = self.client.post('/function/approve/%d/' % function.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        function.refresh_from_db()
        assert_that(function.is_approved, is_(True))
