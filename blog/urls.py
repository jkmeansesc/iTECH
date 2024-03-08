from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('publish/', views.publish, name='publish'),
    path('about/', views.about, name='about'),
    path('blogs/<tag>', views.blogs, name='blogs'),
    path('blogs/', views.blogs, name='blogs'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    path('profile_blogs/', views.profile_blogs, name='profile_blogs'),
    path('profile_comments', views.profile_comments, name='profile_comments'),

    path('blog_detail/<slug:blog_title_slug>', views.blog_detail, name='blog_detail'),
    path('search_results/', views.search_results, name='search_results'),
]
