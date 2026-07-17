from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from hamcrest import equal_to, assert_that, has_entry, has_length, has_item, all_of, not_none, is_, none
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN
from xii.django_river.models import State

from xii.django_river_admin.views import DUPLICATE_ITEM

User = get_user_model()


class StateViewTest(TestCase):

    def test__shouldReturnNotFoundWhenAnInexistentStateIsRequested(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        response = self.client.get('/state/get/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldReturnState(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        state = State.objects.create(label="state-1", description="test-description")
        response = self.client.get('/state/get/%d/' % state.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(state.id)))
        assert_that(response.data, has_entry("label", equal_to(state.label)))
        assert_that(response.data, has_entry("slug", equal_to(state.slug)))
        assert_that(response.data, has_entry("description", equal_to(state.description)))

    def test__shouldReturnEmptyListWhenThereIsNoStates(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        response = self.client.get('/state/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(0))

    def test__shouldReturnListOfStates(self):
        user = User.objects.create_user(username="reader")
        self.client.force_login(user)

        state_1 = State.objects.create(label="state-1")
        state_2 = State.objects.create(label="state-2")

        response = self.client.get('/state/list/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_length(2))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(state_1.id)),
                    has_entry("label", equal_to(state_1.label)),
                    has_entry("slug", equal_to(state_1.slug))
                )
            )
        )

        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("id", equal_to(state_2.id)),
                    has_entry("label", equal_to(state_2.label)),
                    has_entry("slug", equal_to(state_2.slug))
                )
            )
        )

    def test__shouldNotCreateStateWhenLabelIsMissing(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_state"))
        self.client.force_login(user)

        response = self.client.post('/state/create/', data={})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldCreateState(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_state"))
        self.client.force_login(user)

        response = self.client.post('/state/create/', data={"label": "state-1"})
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        created_state = State.objects.first()
        assert_that(created_state, not_none())
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, has_entry("id", equal_to(created_state.pk)))

    def test__shouldRejectCreateWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        response = self.client.post('/state/create/', data={"label": "state-1"})
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(State.objects.filter(label="state-1").first(), is_(none()))

    def test__shouldNotCreateStateWhenLabelIsDuplicate(self):
        user = User.objects.create_user(username="creator")
        user.user_permissions.add(Permission.objects.get(codename="add_state"))
        self.client.force_login(user)

        state = State.objects.create(label="state-1")
        response = self.client.post('/state/create/', data={"label": state.label})
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))
        assert_that(
            response.data,
            has_item(
                all_of(
                    has_entry("error_code", equal_to(DUPLICATE_ITEM)),
                    has_entry(
                        "detail",
                        has_entry(
                            "duplicates",
                            all_of(
                                has_length(1),
                                has_item(equal_to("UNIQUE constraint failed: xii_django_river_state.slug"))
                            )
                        )
                    )
                )
            )
        )

    def test__shouldReturnNotFoundWhenAnInexistentStateIsRequestedToDelete(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_state"))
        self.client.force_login(user)

        response = self.client.delete('/state/delete/1/')
        assert_that(response.status_code, equal_to(HTTP_404_NOT_FOUND))

    def test__shouldDeleteState(self):
        user = User.objects.create_user(username="deleter")
        user.user_permissions.add(Permission.objects.get(codename="delete_state"))
        self.client.force_login(user)

        state = State.objects.create(label="state-1")
        response = self.client.delete('/state/delete/%d/' % state.id)
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(State.objects.filter(label="state-1").first(), is_(none()))

    def test__shouldRejectDeleteWithoutPermission(self):
        user = User.objects.create_user(username="no-perms")
        self.client.force_login(user)

        state = State.objects.create(label="state-1")
        response = self.client.delete('/state/delete/%d/' % state.id)
        assert_that(response.status_code, equal_to(HTTP_403_FORBIDDEN))
        assert_that(State.objects.filter(label="state-1").first(), not_none())
