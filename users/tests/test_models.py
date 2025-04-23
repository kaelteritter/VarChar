from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='exampleuser',
            email='test@example.com',
            password='!changeMe'
        )


    def test_user_can_be_created(self):
        '''
        Тест: Пользователь создается (кастомная версия)
        '''
        self.assertTrue(User.objects.filter(username='exampleuser').exists())
