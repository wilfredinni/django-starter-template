from django.contrib.auth import login
from drf_spectacular.utils import OpenApiResponse, extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import (
    AuthSerializer,
    AuthTokenSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
    LoginResponseSerializer,
)


class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=LoginResponseSerializer,
                description="Successful login response",
            )
        }
    )
    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateUserSerializer
