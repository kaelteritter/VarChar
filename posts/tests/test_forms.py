from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Post, User


class CommentFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser2'
        )
        self.client.force_login(self.user)
        self.post = Post.objects.create(author=self.user, text='Test')
    
    def test_comment_is_being_created_after_form_sent(self):
        '''
        Комментарии создаются через форму
        '''
        data = {'text': 'Test comment for a post'}
        self.client.post(reverse('posts:create_comment', kwargs={'post_id': self.post.pk}), data=data)
        self.assertEqual(Comment.objects.count(), 1)