from django.urls import re_path

from xii.django_river_admin.views import urls
from xii.django_river_admin.views.auth_view import ThrottledObtainAuthToken

urlpatterns = [
                  # ThrottledObtainAuthToken, not DRF's bare obtain_auth_token:
                  # the login endpoint needs its own rate limit (see
                  # LoginRateThrottle) - it's the one endpoint that's reachable
                  # without already being authenticated, so it's the one
                  # brute-force entry point into the whole API.
                  re_path(r'^api-token-auth/', ThrottledObtainAuthToken.as_view()),
              ] + urls
