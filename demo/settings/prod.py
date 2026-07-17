import dj_database_url

from .base import *

# django-heroku was dropped: unmaintained since ~2020 and incompatible with
# modern Django (it patches settings in ways that assume a pre-4.x DATABASES
# shape). dj-database-url + whitenoise cover the same ground (parse
# DATABASE_URL, serve static files) without the abandoned dependency.

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# base.py's SECRET_KEY is a fixed, publicly-visible placeholder meant only
# for local dev/tests - fine there, but every prod deployment sharing it
# would let anyone forge session cookies, password reset tokens, etc.
# against any other deployment. Required here, with no insecure fallback.
try:
    SECRET_KEY = os.environ["SECRET_KEY"]
except KeyError as e:
    raise RuntimeError(
        "SECRET_KEY environment variable is required in production - "
        "see demo/settings/prod.py."
    ) from e

DATABASES = {
    'default': dj_database_url.config(default="sqlite:///%s" % os.path.join(BASE_DIR, 'db.sqlite3')),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + [m for m in MIDDLEWARE if m != 'django.middleware.security.SecurityMiddleware']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# No CACHES override here, so Django falls back to LocMemCache - fine for a
# single-process demo, but worth knowing if you run this behind multiple
# gunicorn workers/machines: LocMemCache is per-process, so
# xii.django_river_admin.views.auth_view.LoginRateThrottle's counter isn't
# shared across workers. With N workers, the effective login rate limit
# becomes N times looser than DEFAULT_THROTTLE_RATES['login'] says, since
# each worker counts independently. For a real multi-worker deployment,
# point CACHES at something shared (Redis via django-redis, Memcached)
# so the throttle counts against one shared total instead.
