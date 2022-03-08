from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ()  # add here custom fields


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ()  # add here custom fields
