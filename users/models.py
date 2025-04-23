from django.contrib.auth.models import AbstractUser
from django.db import models


def get_user_directory_path(instance, filename):
    return f'users/{instance.id}/photos/{filename}'


class User(AbstractUser):
    photo = models.ImageField(
        verbose_name='Аватар',
        upload_to=get_user_directory_path,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
