import os

BASE_DIR = os.path.dirname(__file__)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

RIVER_INJECT_MODEL_ADMIN = False
USE_TZ = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'xii.django_river',
    'xii.django_river_admin',
    # Only needed for xii.django_river_admin.tests.models.WorkflowObjectTestModel,
    # a stand-in "workflow object" model for test__workflow_object_view.py -
    # workflow_object_view.py operates on whatever arbitrary model a
    # Workflow's content_type points at. This deliberately uses a plain
    # ForeignKey(State) rather than river's StateField: StateField
    # unconditionally registers its model into the global, process-wide
    # workflow_registry (xii.django_river.models.fields.state.StateField.
    # contribute_to_class), which would silently change the results of
    # test__workflow_view.py's "list available state fields" tests (they
    # assert exact counts, assuming no other StateField model exists in the
    # process). A plain FK behaves identically for what these tests need
    # (getattr(obj, field_name) returning a State) without that side effect.
    'xii.django_river_admin.tests',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    # Without this, every endpoint defaulted to AllowAny - an unauthenticated
    # caller could hit e.g. /function/list/ and read every stored Function
    # body (arbitrary sandboxed Python source) with no token at all. Each
    # view still layers its own permission=/permission_classes= on top of
    # this where it needs more than "just logged in" (see views/__init__.py).
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Only the 'login' scope is used (xii.django_river_admin.views.auth_view.
    # LoginRateThrottle, applied to /api-token-auth/) - deliberately not
    # rate-limiting the rest of the API here, since every other endpoint
    # already requires IsAuthenticated above.
    'DEFAULT_THROTTLE_RATES': {
        'login': '10/min',
    },
    'EXCEPTION_HANDLER': 'xii.django_river_admin.views.exception_handler'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CORS_ORIGIN_ALLOW_ALL = True

STATIC_URL = '/static/'


SITE_ID = 1

SECRET_KEY = 'abcde12345'

ROOT_URLCONF = 'test_urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '(%(module)s) (%(name)s) (%(asctime)s) (%(levelname)s) %(message)s',
            'datefmt': "%Y-%b-%d %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }

    },
    'loggers': {
        'xii.django_river': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}
