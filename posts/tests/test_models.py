from django.test import TestCase

from posts.models import Post


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            text='Hi, this is the test post'
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