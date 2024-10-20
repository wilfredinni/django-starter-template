from django.contrib.auth import login
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import (
    AuthSerializer,
    AuthTokenSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
)


class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
