from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(
        blank=False, 
        null=False
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        verbose_name='Автор'
        )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.text}'