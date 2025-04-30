from multiprocessing import Process
import os
import signal
import time
from unittest import TestCase
import unittest
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def run_server():
    execute_from_command_line(["manage.py", "runserver", "--noreload", "8000"])

server_process = None
browser = None
address = None


def setUpModule():
    global server_process, browser, address
    server_process = Process(target=run_server)
    server_process.start()
    time.sleep(2)

    browser = webdriver.Firefox()
    address = 'http://127.0.0.1:8000'


def tearDownModule():
    global server_process, browser
    if browser:
        browser.quit()

    if server_process:
        os.kill(server_process.pid, signal.SIGTERM)
        server_process.join()


class LoginPageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = address + '/login/'
        super().setUpClass()

    def test_explore_login_page(self):
        '''
        Тест: Авторизация пользователя
        '''
        # Пользователь заходит на /login/ и видит страницу авторизации
        # Вверху заголовок "Авторизация"
        browser.get(self.url)
        self.assertIn("Авторизация", browser.title)

        # Пользователь находит форму с авторизацией
        try:
            form = browser.find_element(By.TAG_NAME, 'form')
            self.assertIsNotNone(form, 'Форма не найдена на странице')
        except NoSuchElementException:
            self.fail('Форма не найдена на странице')

        # Пользователь видит поля для заполнения
        try:
            inputs = browser.find_elements(By.TAG_NAME, 'input')
            self.assertTrue(len(inputs) > 0, 'Нет полей ввода данных в форме')
        except NoSuchElementException:
            self.fail('Нет полей ввода данных в форме')

        # Он видит поля: username, пароль
        try:
            username_field = browser.find_element(By.XPATH, '//input[@name="username"]')
            password_field = browser.find_element(By.XPATH, '//input[@name="password"]')
            self.assertIsNotNone(username_field)
            self.assertIsNotNone(password_field)
        except NoSuchElementException:
            self.fail('Нет полей username или password или не заданы их атрибуты в форме авторизации')

        # Случай 1: Пользователь вводит невалидные данные в форму и на этой же странице
        # видит сверху от формы всплывающее сообщение о том, что данные некорректны
        data = {'username': 'unexistinguser', 'password': '1234'}
        username_field = browser.find_element(By.XPATH, '//input[@name="username"]')
        password_field = browser.find_element(By.XPATH, '//input[@name="password"]')
        username_field.send_keys(data['username'])
        password_field.send_keys(data['password'])
        password_field.send_keys(Keys.RETURN)
        try:
            wait = WebDriverWait(browser, 10)
            error_message_got = wait.until(
                expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'alert')
                )
                )
        except TimeoutException:
            try:
                element = browser.find_element(By.CLASS_NAME, 'alert')
            except NoSuchElementException:
                self.fail('Сообщение об ошибке не появилось после ввода невалидных данных в авторизации')

        error_message_expected = 'Неверный логин или пароль'
        self.assertEqual(error_message_got.text, 
                         error_message_expected, 
                         f'Неверное сообщение об ошибке валидации: {error_message_got.text}'
                         f'Нужно: {error_message_expected}')

        # Случай 2: Пользователь вводит валидные данные в форму и его переносит на главную страницу
        # (должен быть создан пользователь, так как используем unittest вместо django
        # и не можем создать тест-юзера)
        username_field = browser.find_element(By.XPATH, '//input[@name="username"]')
        password_field = browser.find_element(By.XPATH, '//input[@name="password"]')
        username_field.clear()
        password_field.clear()
        data = {'username': 'root', 'password': '1234'}
        try:
            username_field.send_keys(data['username'])
            password_field.send_keys(data['password'])
            password_field.send_keys(Keys.RETURN)
            wait = WebDriverWait(browser, 5)
            wait.until(expected_conditions.url_to_be(address + '/'))
            self.assertEqual(browser.current_url, address + '/', 
                             'После валидации пользователь не переносится на главную страницу')
        except NoSuchElementException:
            self.fail('Нет одного из необходимых полей: username, password')

        # На главной он видит всплывающее сообщение об успешной авторизации



class SignUpPageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = address + '/signup/'
        super().setUpClass()

    def test_explore_signup_page(self):
        '''
        Тест: регистрация пользователя
        '''
        # Пользователь заходит на /signup/ и видит страницу регистрации
        # Вверху заголовок "Регистрация"
        browser.get(self.url)
        self.assertIn('Регистрация', browser.title)

        # Пользователь находит форму с регистрацией
        try:
            form = browser.find_element(By.TAG_NAME, 'form')
            self.assertIsNotNone(form, 'На странице не найдена форма регистрации')
        except NoSuchElementException:
            self.fail('На странице не найдена форма регистрации')

        # Пользователь видит поля для заполнения: username, два поля для пароля (с подтверждением)
        try:
            username_field = browser.find_element(By.XPATH, '//input[@name="username"]')
            password1_field = browser.find_element(By.XPATH, '//input[@name="password1"]')
            password2_field = browser.find_element(By.XPATH, '//input[@name="password2"]')
            self.assertIsNotNone(username_field, 'Нет поля username')
            self.assertIsNotNone(password1_field, 'Нет поля пароля')
            self.assertIsNotNone(password2_field, 'Нет поля подвтерждения пароля')
        except NoSuchElementException:
            self.fail('Нет одного из полей: username или password1 или password2')


        # Пользователь вводит данные в форму и его переносит на главную страницу
        # Случай 1: Пользователь вводит невалидные данные
        wait = WebDriverWait(browser, 10)
        username_field = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "username")))
        password1_field = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "password1")))
        password2_field = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "password2")))
        data = {
            'username': 'unexistinguser',
            'password1': '1234',
            'password2': '1235'
        }
        try:
            username_field.send_keys(data['username'])
            password1_field.send_keys(data['password1'])
            password2_field.send_keys(data['password2'])
            password2_field.send_keys(Keys.RETURN)
            wait = WebDriverWait(browser, 10)
            error_message_got = wait.until(expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "invalid-feedback")
            ))
        except TimeoutException:
            self.fail('Сообщение об ошибке не появилось')

        error_message_expected = 'Пароли не совпадают'
        self.assertIn(error_message_expected, error_message_got.text, 'Неверное сообщение об ошибке')

        # На главной он видит всплывающее сообщение об успешной авторизации

if __name__ == '__main__':
    unittest.main(warnings='ignore')