from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


from posts.models import Post

User = get_user_model()


class BaseSeleniumTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


class HomePageTest(BaseSeleniumTest):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        for i in range(5):
            Post.objects.create(
                author=self.user,
                title=f'Мой тестовый пост #{i}',
                text=f'Текст поста #{i}'
            )
   
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


class LoginAndLogoutTest(BaseSeleniumTest):
    def test_user_click_login(self):
        # Неавторизованный пользователь видит кнопку "Войти", при клике его перебрасывает
        # на страницу авторизации
        self.browser.get(self.live_server_url)
        login = self.browser.find_element(By.LINK_TEXT, 'Войти')
        login.click()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('users:login'))
        

