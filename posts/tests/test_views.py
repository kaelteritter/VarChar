from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Post


User = get_user_model()

class HomeViewTest(TestCase):
    def setUp(self):
        self.url = '/'
        self.client = Client()
        self.user = User.objects.create_user(username='testuser1')

    def test_bunch_of_posts_can_be_seen_at_index_page(self):
        '''
        Тест: на главной странице в контекст передаются посты пользователей
        '''
        number_of_posts = 5
        for i in range(number_of_posts):
            Post.objects.create(
                text=f'Пост №{i + 1}',
                author=self.user
            )
        response = self.client.get(self.url)
        first_post = response.context.get('posts')[0]

        self.assertEqual(Post.objects.count(), number_of_posts)
        self.assertEqual(first_post.text, 'Пост №1')