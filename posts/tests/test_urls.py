from django.test import Client, TestCase


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
