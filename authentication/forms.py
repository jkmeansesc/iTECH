from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    # 密码的最大长度 = 6
    
    # password = forms.CharField(widget=forms.PasswordInput())
    # 设置密码的最小长度为6
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'maxlength': '6', 'required': 'required'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required', 'minlength': '6'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': 'required', 'unique': 'true'}))


    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = ['website', 'picture']
        fields = ['picture']


        





        

        

        
