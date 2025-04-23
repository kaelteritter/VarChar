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
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


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

        # Пользователь вводит данные в форму и его переносит на главную страницу
        # На главной он видит всплывающее сообщение об успешной авторизации


if __name__ == '__main__':
    unittest.main(warnings='ignore')