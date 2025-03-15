import logging

from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, extend_schema_view
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, throttling
from rest_framework.response import Response

from .schema import (
    LOGIN_RESPONSE_SCHEMA,
    PROFILE_DETAIL_SCHEMA,
    PROFILE_PATCH_SCHEMA,
    PROFILE_PUT_SCHEMA,
    USER_CREATE_RESPONSE_SCHEMA,
)
from .serializers import (
    AuthTokenSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
)
from .throttles import UserLoginRateThrottle

logger = logging.getLogger(__name__)


@extend_schema(responses=LOGIN_RESPONSE_SCHEMA)
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    throttle_classes = [UserLoginRateThrottle]

    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        logger.info(f"User {user.email} logged in.")
        return super(LoginView, self).post(request, format=None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


@extend_schema_view(
    get=extend_schema(responses=PROFILE_DETAIL_SCHEMA),
    patch=extend_schema(responses=PROFILE_PATCH_SCHEMA),
    put=extend_schema(responses=PROFILE_PUT_SCHEMA),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = [throttling.UserRateThrottle]

    def get_object(self):
        return self.request.user


@extend_schema(responses=USER_CREATE_RESPONSE_SCHEMA)
class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateUserSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"User {user.username} created.")
