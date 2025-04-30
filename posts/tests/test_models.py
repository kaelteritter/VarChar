from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser')
        self.post = Post.objects.create(
            text='Hi, this is the test post',
            author=self.user
        )

    def test_string_representation(self):
        '''
        Тест: Post имеет строковое представление
        '''
        self.assertEqual(str(self.post), 'Hi, this is the test post')

    def test_verbose_names(self):
        '''
        Тест: Post имеет человекочитаемое имя
        '''
        self.assertTrue(hasattr(self.post._meta, 'verbose_name'))
        self.assertTrue(hasattr(self.post._meta, 'verbose_name_plural'))
        self.assertEqual(self.post._meta.verbose_name, 'Пост')
        self.assertEqual(self.post._meta.verbose_name_plural, 'Посты')

    def test_post_has_author(self):
        self.assertTrue(hasattr(self.post, 'author'))
        self.assertTrue(self.post.author.username, 'TestAuthor')