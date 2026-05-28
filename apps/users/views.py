import logging

from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, serializers, status, throttling
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .schema import (
    LOGIN_RESPONSE_SCHEMA,
    PROFILE_DETAIL_SCHEMA,
    PROFILE_PATCH_SCHEMA,
    PROFILE_PUT_SCHEMA,
    USER_CREATE_RESPONSE_SCHEMA,
)
from .serializers import (
    CreateUserSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
)
from .throttles import UserLoginRateThrottle

logger = logging.getLogger(__name__)


@extend_schema(responses=LOGIN_RESPONSE_SCHEMA)
class LoginView(TokenObtainPairView):
    """Login view using SimpleJWT token authentication."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [UserLoginRateThrottle]

    def post(self, request, format=None) -> Response:
        serializer = CustomTokenObtainPairSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        login(request, user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


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
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CreateUserSerializer
    throttle_classes = [throttling.UserRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            # Explicitly validate the data including password complexity checks
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info("User %s created.", serializer.data["email"])
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except serializers.ValidationError as e:
            logger.warning("Failed to create user: %s", e.detail)
            raise

    def perform_create(self, serializer):
        serializer.save()
