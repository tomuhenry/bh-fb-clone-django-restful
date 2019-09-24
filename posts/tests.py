from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser


class TestPosts(TestCase):

    def setUp(self):
        self.client.force_login(CustomUser.objects.get_or_create(username='testuser')[0])
        self.user = CustomUser.objects.get(username='testuser')
        self.post = self.client.post(reverse('posts:list_post'), {
            'post_body': 'This is the Post body', 'author': self.user.pk})

    def test_get_posts(self):
        """ Test get all posts """
        resp = self.client.get(reverse('posts:list_post'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)

    def test_create_post(self):
        """ Test for Post Creation """
        self.assertEqual(self.post.status_code, 201)
        self.assertIn('created_at', self.post.data)

    def test_create_post_no_data(self):
        """ Test for Post Creation no data """
        resp = self.client.post(reverse('posts:list_post'), {
            'post_body': "", 'author': ""})
        self.assertEqual(resp.status_code, 400)

    def test_view_a_post(self):
        """ Test view single post """
        resp1 = self.client.get(reverse('posts:post_detail', kwargs={'pk': self.post.data['pk']}))
        self.assertEqual(resp1.status_code, 200)
        self.assertIn('post_body', resp1.data)

    def test_view_a_post_not_found(self):
        """ Test view single post not found """
        resp1 = self.client.get(reverse('posts:post_detail', kwargs={'pk': 100}))
        self.assertEqual(resp1.status_code, 404)

    def test_add_comment(self):
        """ Test add Comments """
        response = self.client.post(reverse('posts:list_comment', kwargs={'post_pk': self.post.data['pk']}),
                                    {'comment_body': "This is the comment", 'author': self.user.pk})
        self.assertEqual(response.status_code, 201)
        self.assertIn('comment_body', response.data)

    def test_get_comments(self):
        """ Test Get Comments """
        response1 = self.client.get(reverse('posts:list_comment', kwargs={'post_pk': self.post.data['pk']}))
        self.assertEqual(response1.status_code, 200)

    def test_edit_post(self):
        """ Test edit single post """
        resp2 = self.client.put(reverse('posts:post_detail', kwargs={'pk': self.post.data['pk']}),
                                {'post_body': 'This Body', 'author': self.user.pk},
                                content_type='application/json')
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('This Body', resp2.data['post_body'])

    def test_delete_own_post(self):
        """ Test delete single post """
        resp3 = self.client.delete(reverse('posts:post_detail', kwargs={'pk': self.post.data['pk']}))
        self.assertEqual(resp3.status_code, 204)
        self.assertIsNone(resp3.data)

    def test_cant_delete_others_post(self):
        """ Test cannot delete other's post """
        self.client.force_login(CustomUser.objects.get_or_create(username='otheruser')[0])
        resp = self.client.delete(reverse('posts:post_detail', kwargs={'pk': self.post.data['pk']}))
        self.assertEqual(resp.status_code, 403)

    def test_get_a_comment(self):
        """ Test get single Comment """
        comment = self.client.post(reverse('posts:list_comment', kwargs={'post_pk': self.post.data['pk']}),
                                   {'comment_body': "This is the comment", 'author': self.user.pk})
        response = self.client.get(reverse('posts:comment_detail', kwargs={'post_pk': self.post.data['pk'],
                                                                           'pk': comment.data['pk']}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comment.data['comment_body'], response.data['comment_body'])

    def test_get_comment_not_found(self):
        """ Test Comment not found """
        response = self.client.get(reverse('posts:comment_detail', kwargs={'post_pk': self.post.data['pk'],
                                                                           'pk': 100}))
        self.assertEqual(response.status_code, 404)

    def test_delete_own_comment(self):
        """ Test delete single Comment """
        comment = self.client.post(reverse('posts:list_comment', kwargs={'post_pk': self.post.data['pk']}),
                                   {'comment_body': "This is the comment", 'author': self.user.pk})
        response = self.client.get(reverse('posts:comment_detail', kwargs={'post_pk': self.post.data['pk'],
                                                                           'pk': comment.data['pk']}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comment.data['comment_body'], response.data['comment_body'])

    def test_cannot_delete_other_comment(self):
        """ Test cannot delete other's Comment """
        comment = self.client.post(reverse('posts:list_comment', kwargs={'post_pk': self.post.data['pk']}),
                                   {'comment_body': "This is the comment", 'author': self.user.pk})
        self.client.force_login(CustomUser.objects.get_or_create(username='anotheruser')[0])
        response = self.client.delete(reverse('posts:comment_detail', kwargs={'post_pk': self.post.data['pk'],
                                                                              'pk': comment.data['pk']}))
        self.assertEqual(response.status_code, 403)

    def tearDown(self):
        self.client.logout()
