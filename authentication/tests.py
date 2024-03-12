from datetime import timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import UserProfile


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user and associated profile
        cls.user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="12345"
        )
        cls.profile = UserProfile.objects.create(user=cls.user)

    def test_token_generation(self):
        self.profile.generate_token()
        self.assertIsNotNone(self.profile.token)
        self.assertIsNotNone(self.profile.token_created_at)

    def test_token_validity(self):
        self.profile.generate_token()
        is_token_valid = self.profile.is_token_valid()
        self.assertTrue(is_token_valid)

        # Simulate token expiry
        self.profile.token_created_at -= timedelta(minutes=4)
        self.profile.save()
        is_token_valid_after_expiry = self.profile.is_token_valid()
        self.assertFalse(is_token_valid_after_expiry)

    def test_default_picture(self):
        self.assertEqual(self.profile.picture.name, "images/default.jpg")

    def test_profile_string_representation(self):
        self.assertEqual(str(self.profile), "testuser")


class AuthenticationTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.test_user = User.objects.create_user(username="test", password="test123")
        self.test_user.save()

    def test_register(self):
        response = self.client.post(
            reverse("authentication:register"),
            {"username": "test2", "password": "test123", "email": "test2@gmail.com"},
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_login(self):
        response = self.client.post(
            reverse("authentication:user_login"),
            {"username": "test", "password": "test123"},
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_login_failure(self):
        response = self.client.post(
            reverse("authentication:user_login"),
            {"username": "wrong", "password": "wrong"},
        )
        self.assertEqual(
            response.status_code, 200
        )  # Expecting a rendered form with error message

    def test_logout(self):
        self.client.login(username="test", password="test123")
        response = self.client.get(reverse("authentication:user_logout"))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_set_username(self):
        self.client.login(username="test", password="test123")
        response = self.client.post(
            reverse("authentication:set_username"), {"username": "newname"}
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
