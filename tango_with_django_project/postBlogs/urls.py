from django.urls import path
from postBlogs import views

urlpatterns = [
    path('', views.index, name='index'),  # The home page of postBlogs
    path('create/', views.create_post, name='create_post'),  # Page to create a new blog post
    path('<int:post_id>/', views.post_detail, name='post_detail'),  # Detail view for a specific post
]