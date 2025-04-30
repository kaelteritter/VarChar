import os
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from posts.models import Post

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser')
        self.post = Post.objects.create(
            text='Hi, this is the test post',
            author=self.user
        )
        self.testfiles = []

    def test_string_representation(self):
        '''
        Тест: Post имеет строковое представление
        '''
        self.assertEqual(str(self.post), 'Hi, this is the test post')

    def test_verbose_names(self):
        '''
        Тест: Post имеет человекочитаемое имя
        '''
        self.assertTrue(hasattr(self.post._meta, 'verbose_name'))
        self.assertTrue(hasattr(self.post._meta, 'verbose_name_plural'))
        self.assertEqual(self.post._meta.verbose_name, 'Пост')
        self.assertEqual(self.post._meta.verbose_name_plural, 'Посты')

    def test_post_has_author(self):
        self.assertTrue(hasattr(self.post, 'author'))
        self.assertTrue(self.post.author.username, 'TestAuthor')

    def test_photo_can_be_attached_to_post(self):
        '''
        Тест: Для поста загружается картинка
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

        new_post = Post.objects.create(
            text='Test post with a pic',
            author=self.user,
            pic=gif_file
            )
        with open(new_post.pic.path, 'rb') as f:
            self.assertEqual(f.read(), pic)

        self.testfiles.append(new_post.pic.path)

        expected_path = 'media/users/id1/posts/2/test_image.gif'
        print(new_post.pic.path)
        self.assertTrue(new_post.pic.path.endswith(expected_path))

    def tearDown(self):
        for f in self.testfiles:
            if os.path.exists(f):
                os.remove(f)