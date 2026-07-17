from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.test import TestCase
from hamcrest import assert_that, equal_to
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS

User = get_user_model()


class HasRiverPermissionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="reader")
        self.client.force_login(self.user)

    def test__shouldReturnFalseForAStandardOperationWithoutThePermission(self):
        response = self.client.get('/user/has_river_permission/add/state/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, equal_to(False))

    def test__shouldReturnTrueForAStandardOperationWithThePermission(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_state"))
        response = self.client.get('/user/has_river_permission/add/state/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, equal_to(True))

    def test__shouldRejectAnInvalidOperation(self):
        response = self.client.get('/user/has_river_permission/frobnicate/state/')
        assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldReturnFalseForApproveWithoutThePermission(self):
        # object_type is ignored for "approve" - it only ever maps to
        # xii_django_river.approve_function (see auth_view.has_river_permission).
        response = self.client.get('/user/has_river_permission/approve/function/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, equal_to(False))

    def test__shouldReturnTrueForApproveWithThePermission(self):
        self.user.user_permissions.add(Permission.objects.get(codename="approve_function"))
        response = self.client.get('/user/has_river_permission/approve/function/')
        assert_that(response.status_code, equal_to(HTTP_200_OK))
        assert_that(response.data, equal_to(True))


class LoginThrottleTest(TestCase):
    """
    /api-token-auth/ is the one endpoint reachable without already being
    authenticated - see xii.django_river_admin.views.auth_view.
    LoginRateThrottle / ThrottledObtainAuthToken.
    """

    def setUp(self):
        # DRF's AnonRateThrottle keys its counter off the client's cache
        # backend - clear it so an earlier test's attempts don't leak into
        # this one's count.
        cache.clear()
        User.objects.create_user(username="realuser", password="realpassword")

    def test__shouldAllowLoginAttemptsUpToTheRateLimit(self):
        for _ in range(10):
            response = self.client.post('/api-token-auth/', {"username": "realuser", "password": "wrong"})
            assert_that(response.status_code, equal_to(HTTP_400_BAD_REQUEST))

    def test__shouldThrottleLoginAttemptsBeyondTheRateLimit(self):
        for _ in range(10):
            self.client.post('/api-token-auth/', {"username": "realuser", "password": "wrong"})

        response = self.client.post('/api-token-auth/', {"username": "realuser", "password": "wrong"})
        assert_that(response.status_code, equal_to(HTTP_429_TOO_MANY_REQUESTS))

    def test__shouldStillThrottleEvenWithCorrectCredentials(self):
        # Throttling is per-client (IP, by default for AnonRateThrottle),
        # not per-failed-attempt - a correct login shouldn't be exempt,
        # otherwise the limit does nothing against a slow/patient attacker.
        for _ in range(10):
            self.client.post('/api-token-auth/', {"username": "realuser", "password": "wrong"})

        response = self.client.post('/api-token-auth/', {"username": "realuser", "password": "realpassword"})
        assert_that(response.status_code, equal_to(HTTP_429_TOO_MANY_REQUESTS))
