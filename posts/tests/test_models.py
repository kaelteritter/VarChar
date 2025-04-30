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