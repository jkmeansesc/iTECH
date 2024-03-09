from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BlogForm
from .models import Blog
from .forms import BlogForm
from .utils import send_mails
from django.contrib.auth.decorators import login_required
# 导入HttpResponse
from django.http import HttpResponse


# from django.core.mail import send_mail
# from .utils import send_mails


def index(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        else:
            print(form.errors)

        context_dict = {"message": "The latest blogs"}
        # Get latest 6 blogs
        blogs_latest = Blog.objects.order_by("-date")[:6]
        context_dict["blogs_latest"] = blogs_latest

        form = BlogForm()
        context_dict["form"] = form

        return render(request, "blog/index.html", context=context_dict)

    else:

        context_dict = {"message": "The latest blogs"}
        # Get latest 6 blogs
        blogs_latest = Blog.objects.order_by("-date")[:6]
        context_dict["blogs_latest"] = blogs_latest

        form = BlogForm()
        context_dict["form"] = form

        return render(request, "blog/index.html", context=context_dict)


@login_required
def publish(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog_instance = form.save(commit=False)

            if "image" in request.FILES:
                blog_instance.image = request.FILES["image"]
            else:
                print("no image")

            blog_instance.author = request.user

            blog_instance.save()

            return redirect("blog:index")
        else:
            print(form.errors)
            context_dict = {"message": "have a good day"}
            form = BlogForm()
            context_dict["form"] = form
            return render(request, "blog/publish.html", context=context_dict)
            return render(request, "blog/publish.html", context=context_dict)
    else:
        context_dict = {"message": "have a good day"}
        form = BlogForm()
        context_dict["form"] = form
        return render(request, "blog/publish.html", context=context_dict)


def publish_comment(request, blog_title_slug):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=False)

            context_dict = {}
            try:
                blog = Blog.objects.get(slug=blog_title_slug)
                context_dict["blog"] = blog
            except Blog.DoesNotExist:
                context_dict["blog"] = None

            context_dict["form"] = comment_form
            comment_form.save()

            return render(request, "blog/blog_detail1.html", context=context_dict)

        else:
            print(comment_form.errors)
            context_dict = {}
            comment_form = CommentForm()
            context_dict["form"] = comment_form
            return render(request, "blog/blog_detail1.html", context=context_dict)
    else:
        context_dict = {}
        comment_form = CommentForm()
        context_dict["form"] = comment_form
        return render(request, "blog/blog_detail1.html", context=context_dict)


def about(request):
    return render(request, 'blog/about.html')



def blogs(request, tag=None):
    # Get all blogs
    blogs_all = Blog.objects.all()

    # 收集所有的blogs的tag
    tags = []
    for blog in blogs_all:
        # 将每个blog的tag根据空格分开
        blog_tags = blog.tag.split(" ")
        for blog_tag in blog_tags:
            tags.append(blog_tag)

    # 找到数量最多的tag，作为热门tag
    tag_count = {}
    for tag_ in tags:
        if tag_ in tag_count:
            tag_count[tag_] += 1
        else:
            tag_count[tag_] = 1
    # 将tag_count按照value排序
    tag_count = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)

    # 取前5个tag作为热门tag,只取tag名字
    hot_tags = []
    for tag_ in tag_count[:5]:
        hot_tags.append(tag_[0])

    context_dict = {"hot_tags": hot_tags}

    if tag:
        # 转变为字符串
        tag = str(tag)
        context_dict["tag"] = tag

    return render(request, 'blog/blogs.html', context=context_dict)


def blog_detail(request, blog_title_slug):
    context_dict = {}
    try:
        blog = Blog.objects.get(slug=blog_title_slug)
        context_dict["blog"] = blog
    except Blog.DoesNotExist:
        context_dict["blog"] = None

    return render(request, "blog/blog_detail1.html", context=context_dict)



def search_results(request):
    search_content = request.GET.get('search_content')
    # 用blog的title和tag进行搜索
    # search_content可能包含多个单词，用空格分开
    search_content = search_content.split(" ")

    blogs = Blog.objects.all()
    # 床架一个空的queryset
    blogs = Blog.objects.none()

    for word in search_content:
        # 用title进行搜索
        blogs_title = Blog.objects.filter(title__icontains=word)
        # 用tag进行搜索
        blogs_tag = Blog.objects.filter(tag__icontains=word)
        # 将两个queryset合并，并添加到blogs中
        blogs = blogs | blogs_title | blogs_tag

    context_dict = {"blogs": blogs}

    return render(request, 'blog/search_results.html', context=context_dict)

    
    

def profile_settings(request):
    return render(request, 'blog/profile_settings.html')


def profile_blogs(request):
    return render(request, 'blog/profile_blogs.html')


def profile_comments(request):
    return render(request, 'blog/profile_comments.html')
