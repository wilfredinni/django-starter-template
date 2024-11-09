from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .schema import (
    LOGIN_RESPONSE_SCHEMA,
    USER_CREATE_RESPONSE_SCHEMA,
    PROFILE_DETAIL_SCHEMA,
    PROFILE_PUT_SCHEMA,
    PROFILE_PATCH_SCHEMA,
)
from .serializers import (
    AuthTokenSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
)


@extend_schema(tags=["User Authentication"], responses=LOGIN_RESPONSE_SCHEMA)
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @extend_schema(tags=["User Profile"], responses=PROFILE_DETAIL_SCHEMA)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["User Profile"], responses=PROFILE_PATCH_SCHEMA)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["User Profile"], responses=PROFILE_PUT_SCHEMA)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


@extend_schema(tags=["User Creation"], responses=USER_CREATE_RESPONSE_SCHEMA)
class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateUserSerializer
