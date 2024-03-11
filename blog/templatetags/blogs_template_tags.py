from django import template
from blog.models import Blog

register = template.Library()


@register.inclusion_tag('blog/blogs_smallBlogs.html')
def get_all_blogs(limit=None, tag=None):
    # get blogs with specific tags
    if tag:
        blogs_to_show = []
        blogs_all = Blog.objects.all()

        for blog in blogs_all:
            if tag in blog.tag:
                blogs_to_show.append(blog)
    else:
        blogs_all = Blog.objects.all()
        blogs_to_show = blogs_all
    
    # if number is limited, the limited number of blogs will be presented
    if limit:
        blogs = blogs_to_show[:limit]
        # blogs = Blog.objects.all()[:limit]
    else:
        blogs = blogs_to_show
        # blogs = Blog.objects.all()
    return {'blogs': blogs}
