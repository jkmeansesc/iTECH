from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('set_username/', views.set_username, name='set_username'),
    path('set_email/', views.set_email, name='set_email'),
    path('set_avatar/', views.set_avatar, name='set_avatar'),
    path('set_password/', views.set_password, name='set_password'),
]
