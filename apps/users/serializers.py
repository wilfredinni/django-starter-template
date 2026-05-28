import logging

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser
from .utils import get_errors

logger = logging.getLogger(__name__)
MIN_PASSWORD_LENGTH = getattr(settings, "MIN_PASSWORD_LENGTH", 8)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes user data in the response.

    SimpleJWT auto-detects USERNAME_FIELD='email' from CustomUser,
    so the default validate() already handles email+password authentication.
    """

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        data["user"] = UserProfileSerializer(self.user).data
        logger.info("User %s logged in.", self.user.email)
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=MIN_PASSWORD_LENGTH)
    password2 = serializers.CharField(write_only=True, min_length=MIN_PASSWORD_LENGTH)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "password2")

    def validate(self, data: dict) -> dict:
        password = data["password"]

        # Check password match
        if password != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")

        user_data = {k: v for k, v in data.items() if k != "password2"}
        try:
            validate_password(password, self.Meta.model(**user_data))
        except Exception as e:
            if hasattr(e, "error_list"):
                errors = get_errors(e)
            else:
                errors = [
                    _("An error occurred during password validation. Please try again.")
                ]
            raise serializers.ValidationError({"password": errors}) from e

        return data

    def create(self, validated_data: dict) -> CustomUser:
        validated_data.pop("password2")
        return CustomUser.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": MIN_PASSWORD_LENGTH}
        }

    def validate(self, data: dict) -> dict:
        if "password" in data:
            try:
                validate_password(data["password"], self.Meta.model(**data))
            except Exception as e:
                if hasattr(e, "error_list"):
                    errors = get_errors(e)
                else:
                    errors = ["Password validation error. Please try again."]

                raise serializers.ValidationError({"password": errors}) from e

        return data

    def update(self, instance: CustomUser, validated_data: dict) -> CustomUser:
        password = validated_data.pop("password", None)
        user: CustomUser = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserProfileSerializer()
