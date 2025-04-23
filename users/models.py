from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    # username = ...
    # email = ...
    # photo = ...
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
