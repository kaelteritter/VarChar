from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/'

    def test_home_page_is_available(self):
        '''
        Тест: домашняя страница доступна
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class PostDetailPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.post = Post.objects.create(author=self.user, text='test')

    def test_post_detail_page(self):
        '''
        Для поста есть отдельное представление
        '''
        self.assertEqual(Post.objects.count(), 1)
        response = self.client.get(reverse('posts:post_detail', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, 200)