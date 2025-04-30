from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(
        blank=False, 
        null=False
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.text}'