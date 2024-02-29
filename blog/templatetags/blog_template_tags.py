from django import template
from blog.models import Blog

register = template.Library()


@register.inclusion_tag('blog/smallBlogs.html')
def get_blogs_list():
    return {'blogs': Blog.objects.all()}
