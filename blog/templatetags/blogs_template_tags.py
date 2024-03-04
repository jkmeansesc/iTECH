from django import template
from blog.models import Blog

register = template.Library()


@register.inclusion_tag('blog/blogs_smallBlogs.html')
def get_all_blogs(limit=None):
    if limit:
        blogs = Blog.objects.all()[:limit]
    else:
        blogs = Blog.objects.all()
    return {'blogs': blogs}
