from django.urls import path
from blog import views
from .views import article_upload

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', article_upload, name='article_upload'),
]

