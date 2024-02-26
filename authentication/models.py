from django.db import models

# Create your models here.
class User(models.Model):
    # 用户名不能重复，不能为null
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    # 邮箱不能重复，不能为null
    email = models.EmailField(max_length=100, unique=True, null=False)
    
    def __str__(self):
        return  "user-" + self.username



