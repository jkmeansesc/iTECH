from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMessage
from django.test import Client, TestCase
from django.urls import reverse

from authentication.models import UserProfile

from .forms import BlogForm
from .models import Blog, Comment, Subscribe


class BlogTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.test_profile = UserProfile.objects.create(user=self.test_user)
        # Create a test blog post
        self.test_blog = Blog.objects.create(
            title="test title",
            tag="test tag",
            content="test content",
            author=self.test_user,
        )

    def test_str_returned_is_title(self):
        self.assertEquals(str(self.test_blog), "test title")

    def test_save_slugifies_title(self):
        self.assertEqual(self.test_blog.slug, "test-title")


class CommentTestCase(TestCase):
    def setUp(self):
        # Use the same setup as for the Blog tests
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.test_profile = UserProfile.objects.create(user=self.test_user)
        self.test_blog = Blog.objects.create(
            title="test title",
            tag="test tag",
            content="test content",
            author=self.test_user,
        )
        self.test_comment = Comment.objects.create(
            blog=self.test_blog, author=self.test_user, content="test comment"
        )

    def test_str_returned_is_content(self):
        self.assertEquals(str(self.test_comment), "test comment")


class SubscribeTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.test_profile1 = UserProfile.objects.create(user=self.test_user)
        self.test_user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.test_profile2 = UserProfile.objects.create(user=self.test_user2)
        self.test_subscription = Subscribe.objects.create(
            user=self.test_profile1, author=self.test_profile2
        )

    def test_str_returned_correctly(self):
        self.assertEquals(str(self.test_subscription), "testuser subscribed testuser2")


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.test_user = User.objects.create_user(
            "testuser", "test@test.com", "testpass"
        )
        self.test_user_profile = UserProfile.objects.create(user=self.test_user)

    def test_blog_form_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")
        self.failUnless(isinstance(response.context["form"], BlogForm))

    @patch("django.core.mail.send_mail")
    def test_publish_POST_adds_blog_post(self, mocked_send_mail):
        # create a simple mock image file
        image_mock = SimpleUploadedFile(
            name="test_image.png",
            content=open("static/image/1.png", "rb").read(),
            content_type="image/png",
        )
        self.client.force_login(self.test_user)
        response = self.client.post(
            self.index_url,
            {
                "title": "Test title",
                "tag": "Test tag",
                "content": "Test content",
                "image": image_mock,
            },
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Blog.objects.first().title, "Test title")

        # Verify that a one off email has been sent.
        self.assertTrue(mocked_send_mail.called)
        self.assertEquals(mocked_send_mail.call_count, 1)
