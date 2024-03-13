from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMessage
from django.test import Client, TestCase
from django.test.client import Client
from django.urls import reverse
from django.utils.text import slugify

from authentication.models import UserProfile

from .forms import BlogForm
from .models import Blog, Comment, Subscribe, UserProfile


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


class PublishViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

        self.login_url = reverse("authentication:login")
        self.publish_url = reverse("blog:publish")

        self.client = Client()

    def test_publish_valid_post(self):
        self.client.login(username="testuser", password="password")

        post_data = {
            "title": "Test Blog",
            "tag": "Test Tag",
            "content": "Test content of the blog post.",
            # 'image' is not included, simulating a submission without an image
        }

        response = self.client.post(self.publish_url, post_data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Blog.objects.count(), 1)
        blog_post = Blog.objects.first()

        self.assertEqual(blog_post.title, "Test Blog")
        self.assertEqual(blog_post.tag, "Test Tag")
        self.assertEqual(blog_post.content, "Test content of the blog post.")
        self.assertEqual(blog_post.author, self.user)


class AboutViewTest(TestCase):
    def test_about_view_status_code(self):
        # Retrieve the URL for the 'about' view and make a GET request
        response = self.client.get(reverse("blog:about"))
        # Check that the response is successful (HTTP 200)
        self.assertEqual(response.status_code, 200)

    def test_about_view_uses_correct_template(self):
        # Make a GET request
        response = self.client.get(reverse("blog:about"))
        # Verify that the response uses the correct template
        self.assertTemplateUsed(response, "blog/about.html")


class BlogsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authoring blogs
        test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )

        # Create some blog posts with tags
        tags = [
            "Python Django",
            "Python",
            "Django Rest Framework",
            "Web Development Django",
            "Python Web",
        ]
        for i in range(5):
            Blog.objects.create(
                title=f"Blog post {i}",
                tag=tags[i],
                content="Sample content",
                author=test_user,
            )

    def test_blogs_view_status_code(self):
        response = self.client.get(reverse("blog:blogs"))
        self.assertEqual(response.status_code, 200)

    def test_blogs_view_uses_correct_template(self):
        response = self.client.get(reverse("blog:blogs"))
        self.assertTemplateUsed(response, "blog/blogs.html")

    def test_blogs_view_context(self):
        response = self.client.get(reverse("blog:blogs"))
        self.assertIn("hot_tags", response.context)
        self.assertIn("current_tag", response.context)
        # Check if the hot_tags list contains exactly 5 items
        self.assertEqual(len(response.context["hot_tags"]), 5)

    def test_blogs_view_with_tag(self):
        # Test the view with a specific tag
        response = self.client.get(reverse("blog:blogs", kwargs={"tag": "Python"}))
        self.assertIn("current_tag", response.context)
        self.assertEqual(response.context["current_tag"], "Python")


class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user and user profile for the author
        author_user = User.objects.create_user(
            username="authoruser", password="testpass"
        )
        author_profile = UserProfile.objects.create(user=author_user)

        # Create a test blog post
        cls.blog = Blog.objects.create(
            title="Test Blog Post",
            content="Content of the blog post.",
            author=author_user,
            slug="test-blog-post",
        )

        # Create a user and user profile for the subscriber
        subscriber_user = User.objects.create_user(
            username="subscriberuser", password="testpass"
        )
        subscriber_profile = UserProfile.objects.create(user=subscriber_user)
        Subscribe.objects.create(user=subscriber_profile, author=author_profile)

        cls.blog_slug_url = reverse(
            "blog:blog_detail", kwargs={"blog_title_slug": cls.blog.slug}
        )

    def test_blog_detail_view_status_code(self):
        response = self.client.get(self.blog_slug_url)
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_view_uses_correct_template(self):
        response = self.client.get(self.blog_slug_url)
        self.assertTemplateUsed(response, "blog/blog_detail.html")

    def test_blog_detail_view_context_data(self):
        self.client.login(username="subscriberuser", password="testpass")
        response = self.client.get(self.blog_slug_url)
        self.assertTrue("subscribed" in response.context)
        self.assertTrue(response.context["subscribed"])


class SearchResultsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for authoring blogs
        author_user = User.objects.create_user(
            username="author", email="author@example.com", password="testpass"
        )

        # Create some blogs
        Blog.objects.create(
            title="Python Tutorial",
            content="Content about Python.",
            tag="Programming",
            author=author_user,
        )
        Blog.objects.create(
            title="Django for Beginners",
            content="Content about Django.",
            tag="Web Development",
            author=author_user,
        )
        Blog.objects.create(
            title="Understanding AI",
            content="Content about AI.",
            tag="Technology",
            author=author_user,
        )

    def test_search_results_view_with_title(self):
        response = self.client.get(
            reverse("blog:search_results") + "?search_content=Python Tutorial"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("blogs" in response.context)
        self.assertEqual(len(response.context["blogs"]), 1)
        self.assertContains(response, "Python Tutorial")

    def test_search_results_view_with_tag(self):
        # Search for blogs by tag
        response = self.client.get(
            reverse("blog:search_results") + "?search_content=Programming"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("blogs" in response.context)
        # Assuming 'Programming' tag is unique to one blog
        self.assertEqual(len(response.context["blogs"]), 1)
        self.assertContains(response, "Programming")

    def test_search_results_view_with_content(self):
        response = self.client.get(
            reverse("blog:search_results") + "?search_content=AI"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("blogs" in response.context)
        self.assertEqual(len(response.context["blogs"]), 1)
        self.assertContains(response, "Understanding AI")


class ProfileSettingsViewTest(TestCase):
    def test_profile_settings_view_status_code(self):
        # Retrieve the URL for the 'profile_settings' view and make a GET request
        response = self.client.get(reverse("blog:profile_settings"))
        # Check that the response is successful (HTTP 200)
        self.assertEqual(response.status_code, 200)

    def test_profile_settings_view_uses_correct_template(self):
        # Make a GET request
        response = self.client.get(reverse("blog:profile_settings"))
        # Verify that the response uses the correct template
        self.assertTemplateUsed(response, "blog/profile_settings.html")


class ProfileCommentsViewTest(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Create a blog post
        self.blog = Blog.objects.create(
            title="Blog Post", content="Content", author=self.user1
        )

        # Create comments for each user on the blog post
        Comment.objects.create(
            blog=self.blog, author=self.user1, content="User 1 comment"
        )
        Comment.objects.create(
            blog=self.blog, author=self.user1, content="Another User 1 comment"
        )
        Comment.objects.create(
            blog=self.blog, author=self.user2, content="User 2 comment"
        )

        self.client.login(username="user1", password="password123")

    def test_profile_comments_view_status_code(self):
        response = self.client.get(reverse("blog:profile_comments"))
        self.assertEqual(response.status_code, 200)

    def test_profile_comments_view_uses_correct_template(self):
        response = self.client.get(reverse("blog:profile_comments"))
        self.assertTemplateUsed(response, "blog/profile_comments.html")

    def test_profile_comments_view_context_comments(self):
        response = self.client.get(reverse("blog:profile_comments"))
        # Ensure the context contains 'comments'
        self.assertTrue("comments" in response.context)
        # Ensure all comments in the context belong to user1
        self.assertTrue(
            all(
                comment.author == self.user1 for comment in response.context["comments"]
            )
        )
        # Ensure the correct number of comments is returned
        self.assertEqual(response.context["comments"].count(), 2)
