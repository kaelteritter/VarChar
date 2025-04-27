from django.contrib.auth import get_user_model
from django.test import Client, TestCase


User = get_user_model()

class LoginViewTest(TestCase):
    def setUp(self):
        self.url = '/login/'
        self.user = User.objects.create_user(username='testuser1', password='1234')
        self.client = Client()

    def test_exisiting_user_can_login(self):
        '''
        Тест: Существующий пользователь может авторизоваться
        '''
        data = {
                'username': self.user.username,
                'password': self.user.password,
            }
        response = self.client.post(path=self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)