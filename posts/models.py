from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

def get_post_pic_directory_path(instance, filename):
    return f'users/id{instance.author.id}/posts/{instance.id}/{filename}'

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
    pic = models.ImageField(
        verbose_name='Картинка',
        upload_to=get_post_pic_directory_path,
        blank=True,
        null=True
        )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.text}'
    
    def save(self, *args, **kwargs):
        if not self.id and self.pic:
            pic = self.pic
            self.pic = None
            super().save(*args, **kwargs)
            self.pic = pic
            super().save(update_fields=['pic'])
        else:
            super().save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Автор'
        )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )

    def __str__(self):
        return f'A:{self.author.id} P:{self.to_post.id} {self.text}'