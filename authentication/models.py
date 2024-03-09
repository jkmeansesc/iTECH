from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userProfile')

    picture = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.jpg')
    
    def __str__(self):
        return  self.user.username



