from django.contrib.auth.decorators import login_required
# 导入HttpResponse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BlogForm, CommentForm
from .models import Blog, Comment
from .utils import send_mails
from django.contrib.auth.models import User

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
    else:
        context_dict = {"message": "have a good day"}
        form = BlogForm()
        context_dict["form"] = form
        return render(request, "blog/publish.html", context=context_dict)


def about(request):
    return render(request, "blog/about.html")


def blogs(request, tag=None):
    # Get all blogs
    blogs_all = Blog.objects.all()

    # Get all tags
    tags = []
    for blog in blogs_all:

        blog_tags = blog.tag.split(" ")
        for blog_tag in blog_tags:
            tags.append(blog_tag)

    # count the number of each tag
    tag_count = {}
    for tag_ in tags:
        if tag_ in tag_count:
            tag_count[tag_] += 1
        else:
            tag_count[tag_] = 1
    # sort the tag_count
    tag_count = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)

    # only get the top 5 tags
    hot_tags = []
    for tag_ in tag_count[:5]:
        hot_tags.append(tag_[0])

    context_dict = {"hot_tags": hot_tags}

    if tag:
        tag = str(tag)
        context_dict["tag"] = tag

    return render(request, "blog/blogs.html", context=context_dict)


def blog_detail(request, blog_title_slug):
    blog = get_object_or_404(Blog, slug=blog_title_slug)
    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            comment_form = CommentForm()
            data = {
                "comment_num": blog.comment_num,
                "author": comment.author.username,
                "content": comment.content,
                "date_posted": comment.date_posted.strftime("%Y-%m-%d %H:%M:%S"),
            }
            comments = blog.comments.all().order_by("-date_posted")
            # return render(request, 'blog/blog_detail1.html',
            #             #               {'blog': blog, 'comment_form': comment_form, 'comments': comments})
            return JsonResponse(data)
    else:
        comment_form = CommentForm()

    # sort the comment by the latest date
    comments = blog.comments.all().order_by("-date_posted")
    return render(
        request,
        "blog/blog_detail.html",
        {"blog": blog, "comment_form": comment_form, "comments": comments},
    )


def search_results(request):
    search_content = request.GET.get("search_content")
    print(search_content)
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
        # 用content进行搜索
        blogs_content = Blog.objects.filter(content__icontains=word)
        # 将三个个queryset合并，并添加到blogs中
        blogs = blogs | blogs_title | blogs_tag | blogs_content

    context_dict = {"blogs": blogs}

    return render(request, "blog/search_results.html", context=context_dict)


def profile_settings(request):
    return render(request, "blog/profile_settings.html")


def profile_blogs(request):
    # 返回本用户的所有blog
    blogs = Blog.objects.filter(author=request.user)
    context_dict = {"blogs": blogs}
    return render(request, "blog/profile_blogs.html", context=context_dict)


def profile_comments(request):
    # 返回本用户所有的comment
    comments = Comment.objects.filter(author=request.user)
    context_dict = {"comments": comments}

    return render(request, "blog/profile_comments.html", context=context_dict)


def comment_delete(request, comment_id):
    # 删除comment
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(reverse("blog:profile_comments"))


def blog_delete(request, blog_id):
    # 删除blog
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect(reverse("blog:profile_blogs"))


def manage_accounts(request):
    return render(request, "blog/manage_all_accounts.html")


def manage_blogs(request):
    return render(request, "blog/manage_all_blogs.html")


def manage_comments(request):
    return render(request, "blog/manage_all_comments.html")


def blogs_edit(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog_instance = form.save(commit=False)

            # 判断背景图有没有更新
            if "image" in request.FILES:
                blog_instance.image = request.FILES["image"]

            blog_instance.save()

            return redirect("blog:profile_blogs")
        else:
            context_dict = {"blog": blog}
            form = BlogForm(instance=blog, initial={"image": None})

            context_dict["form"] = form
            return render(request, "blog/blog_edit.html", context=context_dict)
    else:
        context_dict = {"blog": blog}
        form = BlogForm(instance=blog, initial={"image": None})

        context_dict["form"] = form
        return render(request, 'blog/blog_edit.html', context=context_dict)


def manage_accounts(request):
    # 获取所有的普通用户，不能是superuser，不能是staff, 不能是active=False
    users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
    current_page = 'manage_accounts'

    context_dict = {"users": users,
                    "current_page": current_page}
    return render(request, 'blog/manage_all_accounts.html', context=context_dict)


def manage_blogs(request):
    # 获取所有的blogs
    blogs = Blog.objects.all()
    current_page = 'manage_blogs'
    context_dict = {"blogs": blogs,
                    "current_page": current_page}

    return render(request, 'blog/manage_all_blogs.html', context=context_dict)


def manage_comments(request):
    # 获取所有的comments
    comments = Comment.objects.all()
    current_page = 'manage_comments'
    context_dict = {"comments": comments,
                    "current_page": current_page}

    return render(request, 'blog/manage_all_comments.html', context=context_dict)



