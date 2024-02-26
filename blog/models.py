from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title