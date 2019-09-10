from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class TestUser(TestCase):

    def test_create_user(self):
        """ test create new user"""
        url = reverse('rest_register')
        data = {
            'username': "tommy",
            'email': "henry@tomusange.com",
            'password1': "thisPass",
            'password2': "thisPass",

        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('key', resp.data)

    def test_login_user(self):
        """ test login user """
        singup_url = reverse('rest_register')
        data = {
            'username': "tomu",
            'email': "henry@tomu.com",
            'password1': "thisPass",
            'password2': "thisPass",

        }
        self.client.post(singup_url, data)
        login_url = reverse('rest_login')
        data = {
            'username': "tomu",
            'password': "thisPass"
        }
        resp = self.client.post(login_url, data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('key', resp.data)

    def test_logout_user(self):
        """ test logout user """
        logout_url = reverse('rest_logout')
        resp_logout = self.client.post(logout_url, {})
        self.assertEqual(resp_logout.status_code, 200)
        self.assertIn('detail', resp_logout.data)

    def test_get_users(self):
        """ Get all users """
        resp = self.client.get(reverse('users:list_users'))
        self.assertEqual(resp.status_code, 200)

