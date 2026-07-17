from django.db import IntegrityError
from django.db.models import ProtectedError
from django.urls import re_path
# Aliased on purpose: importing xii.django_river_admin.views.serializers below
# (needed for the WorkflowDto/StateDto/... lookup in exception_handler) makes
# Python bind that submodule as the `serializers` attribute on THIS package
# the moment it's imported - which would silently shadow a plain
# `from rest_framework import serializers` and break `ErrorResponse` further
# down. Aliasing sidesteps the collision instead of depending on import order.
from rest_framework import serializers as drf_serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import exception_handler as drf_exception_handler

from xii.django_river.models import (
    Workflow, State, TransitionMeta, TransitionApprovalMeta, Transition, TransitionApproval,
    OnTransitHook, OnApprovedHook,
)
from xii.django_river_admin.views.error_code import CAN_NOT_DELETE_DUE_TO_PROTECTION, DUPLICATE_ITEM
from xii.django_river_admin.views.serializers import (
    WorkflowDto, StateDto, TransitionMetaDto, TransitionApprovalMetaDto, TransitionHookDto, ApprovalHookDto,
)

urls = []


def _path(path, method, **options):
    def decorator(view):
        authentications = options.get("authentication_classes", [TokenAuthentication, SessionAuthentication])
        renderers = options.get("renderer_classes", [JSONRenderer])
        # DRF-level gate, applied before the view even runs: defaults to
        # whatever REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] says
        # (IsAuthenticated - see test_settings.py/demo/settings/base.py) so
        # every endpoint needs a logged-in user unless it opts out
        # explicitly (only `index` below does, to serve the SPA shell
        # before login). This is separate from `permission`, which checks a
        # specific Django permission on top of just being authenticated.
        permission_classes_option = options.get("permission_classes")
        permission = options.get("permission")

        def guarded_view(request, *args, **kwargs):
            if permission and not request.user.has_perm(permission):
                return Response(status=HTTP_403_FORBIDDEN)
            return view(request, *args, **kwargs)

        guarded_view.__name__ = view.__name__
        wrapped = authentication_classes(authentications)(renderer_classes(renderers)(guarded_view))
        if permission_classes_option is not None:
            wrapped = permission_classes(permission_classes_option)(wrapped)
        new_view = api_view([method])(wrapped)
        urls.append(re_path(path, new_view))
        return new_view

    return decorator


def get(path, **options):
    return _path(path, "GET", **options)


def post(path, **options):
    return _path(path, "POST", **options)


def put(path, **options):
    return _path(path, "PUT", **options)


def delete(path, **options):
    return _path(path, "DELETE", **options)


def exception_handler(exc, context):
    handled_exception = drf_exception_handler(exc, context)
    if handled_exception:
        return handled_exception

    errors = []
    if isinstance(exc, ProtectedError):
        error_code = CAN_NOT_DELETE_DUE_TO_PROTECTION
        protected_errors = []
        for protected_object in exc.protected_objects:
            object_type = protected_object.__class__.__name__.lower()
            serializer_class = None
            if isinstance(protected_object, Workflow):
                serializer_class = WorkflowDto
            elif isinstance(protected_object, State):
                serializer_class = StateDto
            elif isinstance(protected_object, TransitionMeta):
                serializer_class = TransitionMetaDto
            elif isinstance(protected_object, TransitionApprovalMeta):
                serializer_class = TransitionApprovalMetaDto
            elif isinstance(protected_object, Transition):
                serializer_class = None
            elif isinstance(protected_object, TransitionApproval):
                serializer_class = None
            elif isinstance(protected_object, OnTransitHook):
                serializer_class = TransitionHookDto
            elif isinstance(protected_object, OnApprovedHook):
                serializer_class = ApprovalHookDto

            if serializer_class:
                protected_errors.append({"object_type": object_type, "object": serializer_class(protected_object).data})

        if protected_errors:
            errors.append({"error_code": error_code, "detail": {"protected_errors": protected_errors}})

    elif isinstance(exc, IntegrityError):
        errors.append({"error_code": DUPLICATE_ITEM, "detail": {"duplicates": exc.args}})

    if errors:
        return Response(ErrorResponse(errors, many=True).data, status=HTTP_400_BAD_REQUEST)
    else:
        return None


class ErrorResponse(drf_serializers.Serializer):
    error_code = drf_serializers.IntegerField()
    detail = drf_serializers.DictField()


# Imported for side effect only: each module's view functions register
# themselves into `urls` via the @get/@post/@put/@delete decorators above.
# Plain module imports (not `from .X import *`) on purpose - star-imports
# used to leak each module's own imports (Q, ContentType, StateDto, etc.)
# into this package's namespace, so other modules could accidentally
# "borrow" them from here instead of importing them directly. That's how a
# stale double-definition of `get_identifier` in workflow_object_view.py and
# a couple of indirect imports elsewhere went unnoticed.
from . import auth_view  # noqa: F401
from . import state_view  # noqa: F401
from . import workflow_view  # noqa: F401
from . import transition_meta_view  # noqa: F401
from . import transition_approval_meta_view  # noqa: F401
from . import function_view  # noqa: F401
from . import transition_hook_view  # noqa: F401
from . import approval_hook_view  # noqa: F401
from . import transition_view  # noqa: F401
from . import transition_approval_view  # noqa: F401
from . import workflow_object_view  # noqa: F401


@get(r'^xii-django-river-admin/$', authentication_classes=[], renderer_classes=[TemplateHTMLRenderer], permission_classes=[AllowAny])
def index(request):
    return Response({}, template_name="index.html")
