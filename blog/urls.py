from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('\blogs', views.blogs, name='blogs'),

]

