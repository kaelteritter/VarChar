import os
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='exampleuser',
            email='test@example.com',
            password='!changeMe'
        )
        self.testfiles = []

    def test_user_can_be_created(self):
        '''
        Тест: Пользователь создается (кастомная версия)
        '''
        self.assertTrue(User.objects.filter(username='exampleuser').exists())

    def test_string_representation(self):
        '''
        Тест: User имеет строковое представление
        '''
        self.assertTrue(hasattr(self.user, '__str__'))

    def test_verbose_name(self):
        '''
        Тест: модель User имеет человекочитаемое имя
        '''
        self.assertTrue(hasattr(self.user._meta, 'verbose_name'))
        self.assertTrue(hasattr(self.user._meta, 'verbose_name_plural'))
        self.assertEqual(self.user._meta.verbose_name, 'Пользователь')
        self.assertEqual(self.user._meta.verbose_name_plural, 'Пользователи')

    def test_photo_can_be_uploaded(self):
        '''
        Тест: Для модели пользователя загружается фотография
        '''
        pic = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
        b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
        b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        )
        gif_file = SimpleUploadedFile(
            'test_image.gif',
            pic,
            content_type='image/gif'
        )
        new_user = User.objects.create_user(username='testuser2', photo=gif_file)

        with open(new_user.photo.path, 'rb') as f:
            self.assertEqual(f.read(), pic)

        self.testfiles.append(new_user.photo.path)

        expected_path = 'media/users/id2/photos/test_image.gif'
        self.assertTrue(new_user.photo.path.endswith(expected_path))

    def tearDown(self):
        for f in self.testfiles:
            if os.path.exists(f):
                os.remove(f)

