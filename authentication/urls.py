from django.urls import path, include
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='password_reset')
]
