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
    path('blog_delete/<int:blog_id>', views.blog_delete, name='blog_delete'),
    path('profile_comments/', views.profile_comments, name='profile_comments'),
    path('comment_delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
    path('blog_detail/<slug:blog_title_slug>', views.blog_detail, name='blog_detail'),
    path('blogs_edit/<int:blog_id>/', views.blogs_edit, name='blogs_edit'),
    path('manage_blogs/', views.manage_blogs, name='manage_all_blogs'),
    path('manage_accounts/', views.manage_accounts, name='manage_all_accounts'),
    path('manage_comments/', views.manage_comments, name='manage_all_comments'),

    path('search_results/', views.search_results, name='search_results'),
    path('subscribe/<slug:blog_title_slug>', views.subscribe, name='subscribe'),
    path('unsubscribe/<slug:blog_title_slug>', views.unsubscribe, name='unsubscribe'),

    path('blog_delete_manage/<int:blog_id>', views.blog_delete_manage, name='blog_delete_manage'),
    path('comment_delete_manage/<int:comment_id>', views.comment_delete_manage, name='comment_delete_manage'),
]
