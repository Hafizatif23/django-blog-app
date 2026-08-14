from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

# Create your tests here.

class PostCreationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')


    def test_logged_in_user_can_create_post(self):

        self.client.login(username='testuser', password='testpass123')

        response = self.client.post('/write/', {
            'title': 'Testcase1',
            'category': 'Tech',
            'content':  'This is test post '
        })

        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Post.objects.count(), 1) 


    def test_logged_out_user_cannot_create_post(self):

        response = self.client.post('/write/', {
            'title': 'Logout Post',
            'category': 'Tech',
            'content':  'This is test post for logout '
        })

        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Post.objects.count(), 0) 


    def test_non_author_cannot_delete_post(self):

        otheruser = User.objects.create_user(username='otheruser', password='testpass123')

        self.client.login(username='testuser', password='testpass123')
        self.client.post('/write/', {
            'title': 'sneaky Post',
            'category': 'Tech',
            'content':  'This post is for authorization test'
        })

        post = Post.objects.first()

        self.client.logout()
        self.client.login(username='otheruser', password='testpass123')

        delete_response = self.client.post(f'/post/{post.id}/delete/', {})

        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(Post.objects.count(), 1)
