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

    def test_create_post(self):
        """ Test for Post Creation """
        resp = self.client.post(reverse('posts:list_post'), {'post_body': 'This is the Post body'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('created_at', resp.data)

    def test_view_single_post(self):
        """ Test view single post """
        post = self.client.post(reverse('posts:list_post'), {'post_body': 'This is the Post body'})
        resp = self.client.get(reverse('posts:post_detail', kwargs={'pk': post.data['pk']}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('post_body', resp.data)

    def test_delete_single_post(self):
        """ Test delete own post """
        post = self.client.post(reverse('posts:list_post'), {'post_body': 'This is the Post body'})
        resp = self.client.delete(reverse('posts:post_detail', kwargs={'pk': post.data['pk']}))
        self.assertEqual(resp.status_code, 204)
        self.assertIsNone(resp.data)

    def test_edit_single_post(self):
        """ Test edit own post """
        post = self.client.post(reverse('posts:list_post'), {'post_body': 'This is the Post body'})
        resp = self.client.put(reverse('posts:post_detail', kwargs={'pk': post.data['pk']}),
                               {'post_body': 'This Body'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('This Body', resp.data['post_body'])


