from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from authentication.models import UserProfile



class Blog(models.Model):

    title = models.CharField(max_length=200, default='')
    tag = models.CharField(max_length=200, default='')
    content = RichTextField(default="Please input your content here")
    comment_num = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog_images', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # 作者, 作者是一个外键，指向用户表
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='')
    content = models.TextField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.reviewer} on {self.blog}'
