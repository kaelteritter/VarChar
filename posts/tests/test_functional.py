import unittest
import os
import django
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from posts.models import Post

User = get_user_model()

class HomePageTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)

        cls.user = User.objects.create(username='testuser')
        num_posts = 5
        for i in range(num_posts):
            Post.objects.create(
                author=cls.user,
                title=f'Мой тестовый пост #{i}',
                text=f'Тестовый текст для поста #{i}'
            )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
        
    def test_home_page_content(self):
        # Пользователь видит в заголовке странице название/Главная
        self.browser.get(self.live_server_url)
        self.assertIn('Главная', self.browser.title)

        # Вверху он видит блок меню
        try:
            self.browser.find_element(By.XPATH, '//nav[contains(@class, "navbar")]')
        except NoSuchElementException:
            self.fail('Не найдено меню с корректными селекторами на главной странице')

        # В меню есть ссылка на главную и на войти/выйти
        titles = ['Главная', 'Войти']
        try:
            nav_items = [e.text for e in self.browser.find_elements(By.CLASS_NAME, 'nav-link')]
            for title in titles:
                self.assertIn(title, nav_items)
        except NoSuchElementException:
            self.fail('Нет одного из пунктов навигации')

        # В главном блоке он видит несколько опубликованных постов
        posts = self.browser.find_elements(By.CLASS_NAME, 'post-item')
        self.assertTrue(posts, 'Не найдено постов на главной странице')


if __name__ == '__main__':
    unittest.main()