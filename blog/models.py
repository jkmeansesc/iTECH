from django.db import models
from ckeditor.fields import RichTextField

class Blog(models.Model):

    title = models.CharField(max_length=200, default='')
    tag = models.CharField(max_length=200, default='')
    content = RichTextField(default="Please input your content here")
    comment_num = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog_images', blank=True)
    # date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content