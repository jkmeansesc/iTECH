from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
]

