from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userProfile')

    picture = models.ImageField(upload_to='profile_images', blank=True, default='images/default.jpg')

    
    token = models.CharField(max_length=100, null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def generate_token(self):
        # 生成随机令牌
        self.token = default_token_generator.make_token(self.user)
        self.token_created_at = timezone.now()
        self.save()

    def is_token_valid(self):
        if self.token_created_at:
            expiration_time = self.token_created_at + timedelta(minutes=3) # 3分钟内有效
            return timezone.now() <= expiration_time
        return False

    def __str__(self):
        return  self.user.username



