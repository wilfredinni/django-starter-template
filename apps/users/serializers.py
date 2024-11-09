from .models import CustomUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs: dict) -> dict:
        email = attrs.get("email")
        password = attrs.get("password")

        # The authenticate call simply returns None for is_active=False users
        if email and password:
            user: CustomUser = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=5)
    password2 = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "password2")

    def validate(self, data: dict) -> dict:
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data: dict) -> CustomUser:
        validated_data.pop("password2")
        return CustomUser.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def update(self, instance: CustomUser, validated_data: dict) -> CustomUser:
        password = validated_data.pop("password", None)
        user: CustomUser = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginResponseSerializer(serializers.Serializer):
    expiry = serializers.DateTimeField()
    token = serializers.CharField()
    user = UserProfileSerializer()

    def get_user(self, obj):
        user = obj.get("user")
        return {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
