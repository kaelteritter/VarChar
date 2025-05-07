from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


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
                'username': 'testuser1',
                'password': '1234',
            }
        response = self.client.post(path=self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class SignUpViewTest(TestCase):
    def setUp(self):
        self.url = '/signup/'
        self.client = Client()

    def test_client_can_sign_up(self):
        '''
        Тест: Пользователь может зарегистрироваться
        '''
        data = {
            'username': 'testuser2',
            'password1': '!changeMe',
            'password2': '!changeMe',
        }
        response = self.client.post(path=self.url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser2').exists())


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser1')
        self.client.force_login(self.user)

    def test_user_logout(self):
        '''
        Тест: юзер может разлогиниться
        '''
        self.assertTrue(self.user.is_authenticated)

        response = self.client.get(reverse('users:logout'))
        self.assertTrue(response.status_code, 302)