import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUsersManagers:

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        assert user.email == "normal@user.com"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.username is None
        # username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        assert user.username is None

        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(TypeError):
            User.objects.create_user(email="")
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        assert admin_user.email == "super@user.com"
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser
        # username is None for the AbstractUser option
        # username does not exist for the AbstractBaseUser option
        assert admin_user.username is None

        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )
