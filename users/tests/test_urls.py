from django.test import Client, TestCase


class LoginURLTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/login/'

    def test_login_page_get_response_code(self):
        '''
        Тест: страница авторизации по GET-запросу получает 200 ОК
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_page_uses_correct_template(self):
        '''
        Тест: страница авторизации использует шаблон login.html
        '''
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/login.html')