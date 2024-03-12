from datetime import timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import UserProfile


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        self.client = Client()
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.test_profile = UserProfile.objects.create(user=self.test_user)

    def test_registration_view(self):
        response = self.client.get(reverse("authentication:register"))
        self.assertEqual(response.status_code, 200)

    def test_user_login_view(self):
        response = self.client.post(
            reverse("authentication:login"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 302)

    def test_user_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("authentication:logout"))
        self.assertEqual(response.status_code, 302)

    def test_change_password_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("authentication:set_password"),
            {"password": "newpassword", "password1": "newpassword"},
        )
        self.assertEqual(response.status_code, 302)
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password("newpassword"))

    def test_password_reset_view(self):
        response = self.client.post(
            reverse("authentication:password_reset"), {"email": self.test_user.email}
        )
        self.assertEqual(response.status_code, 200)
