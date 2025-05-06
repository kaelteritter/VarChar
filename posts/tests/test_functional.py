from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class HomePageTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)

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
            menu = self.browser.find_element(By.XPATH, '//nav[@class="navigation"]')
        except NoSuchElementException:
            self.fail('Не найдено меню с корректными селекторами на главной странице')


if __name__ == '__main__':
    import unittest
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    unittest.main()