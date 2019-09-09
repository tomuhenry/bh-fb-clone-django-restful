from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser


class TestPosts(TestCase):

    def setUp(self):
        self.client.force_login(CustomUser.objects.create(
            username="tomu",
            email="henry@tomu.com",
            password="thisPass"
        ))

    def test_get_posts(self):
        """ Test get all posts """
        resp = self.client.get(reverse('posts:list_post'))
        self.assertEqual(resp.status_code, 200)

    def test_get_users(self):
        resp = self.client.get(reverse('users:list_users'))
        self.assertEqual(resp.status_code, 200)

    def test_create_post(self):
        """ Test for Post Creation """
        resp = self.client.post(reverse('posts:list_post'), {'post_body': 'This is the Post body'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('created_at', resp.data)
