# from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # more fields here

    def __str__(self):
        return f"{self.username}"
