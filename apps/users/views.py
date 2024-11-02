from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .schema import (
    LOGIN_RESPONSE_SCHEMA,
    PROFILE_RESPONSE_SCHEMA,
    USER_CREATE_RESPONSE_SCHEMA,
)
from .serializers import (
    AuthSerializer,
    AuthTokenSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
)


@extend_schema(tags=["User Authentication"], responses=LOGIN_RESPONSE_SCHEMA)
class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


@extend_schema(tags=["User Profile"], responses=PROFILE_RESPONSE_SCHEMA)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


@extend_schema(tags=["User Creation"], responses=USER_CREATE_RESPONSE_SCHEMA)
class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateUserSerializer
