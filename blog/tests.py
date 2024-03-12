from django.contrib.auth.models import User
from django.test import TestCase

from authentication.models import UserProfile

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
