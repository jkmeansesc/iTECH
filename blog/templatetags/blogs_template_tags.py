from django import template
from blog.models import Blog

register = template.Library()


@register.inclusion_tag('blog/blogs_smallBlogs.html')
def get_all_blogs(limit=None, tag=None):
    # 找到符合标签的博客
    if tag:
        blogs_to_show = []
        blogs_all = Blog.objects.all()

        for blog in blogs_all:
            if tag in blog.tag:
                blogs_to_show.append(blog)
    else:
        blogs_all = Blog.objects.all()
        blogs_to_show = blogs_all
    
    # 如果有限制，就只显示限制数量的博客
    if limit:
        blogs = blogs_to_show[:limit]
        # blogs = Blog.objects.all()[:limit]
    else:
        blogs = blogs_to_show
        # blogs = Blog.objects.all()
    return {'blogs': blogs}
