from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BlogForm, CommentForm
from .models import Blog, Comment, Subscribe
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

            # send email to all the subscribers
            author = blog_instance.author.userProfile
            subscribers = Subscribe.objects.filter(author=author)
            recipient_list = []
            for subscriber in subscribers:
                user = subscriber.user.user
                recipient_list.append(user.email)
            subject = "Blog update"
            message = blog_instance.author.username + " has updated the blog. Please check it out."
            from_email = "2079459973@qq.com"

            send_mails(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)


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

    context_dict = {"hot_tags": hot_tags, "current_tag": tag}

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

    # check if the user has subscribed the author
    subscribed = False
    if request.user.is_authenticated:
        user = request.user.userProfile
        author = blog.author.userProfile
        if Subscribe.objects.filter(user=user, author=author).exists():
            subscribed = True

    return render(
        request,
        "blog/blog_detail.html",
        {"blog": blog, "comment_form": comment_form, "comments": comments, "subscribed": subscribed},
    )



def search_results(request):
    search_content = request.GET.get("search_content")
    print(search_content)

    # search_content may contain multiple words, so we need to split it
    search_content = search_content.split(" ")

    blogs = Blog.objects.all()
    # get a empty queryset
    blogs = Blog.objects.none()

    for word in search_content:
        # search by title
        blogs_title = Blog.objects.filter(title__icontains=word)
        # search by tag
        blogs_tag = Blog.objects.filter(tag__icontains=word)
        # search by content
        blogs_content = Blog.objects.filter(content__icontains=word)
        # put all the blogs together
        blogs = blogs | blogs_title | blogs_tag | blogs_content

    context_dict = {"blogs": blogs}

    return render(request, "blog/search_results.html", context=context_dict)


def profile_settings(request):
    return render(request, "blog/profile_settings.html")


def profile_blogs(request):
    # return all the blogs of the current user
    blogs = Blog.objects.filter(author=request.user)
    context_dict = {"blogs": blogs}
    return render(request, "blog/profile_blogs.html", context=context_dict)


def profile_comments(request):
    # return all the comments of the current user
    comments = Comment.objects.filter(author=request.user)
    context_dict = {"comments": comments}

    return render(request, "blog/profile_comments.html", context=context_dict)


def comment_delete(request, comment_id):
    # delete comment
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(reverse("blog:comment_delete"))


def blog_delete(request, blog_id):
    # delete_blog
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect(reverse("blog:blog_delete"))


def blogs_edit(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog_instance = form.save(commit=False)

            # check if the image is None
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

    # get all the normal users, cannot be superuser, cannot be staff, cannot be active=False
    users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
    current_page = 'manage_accounts'

    context_dict = {"users": users,
                    "current_page": current_page}
    return render(request, 'blog/manage_all_accounts.html', context=context_dict)


def manage_blogs(request):
    # get all the blogs
    blogs = Blog.objects.all()
    current_page = 'manage_blogs'
    context_dict = {"blogs": blogs,
                    "current_page": current_page}

    return render(request, 'blog/manage_all_blogs.html', context=context_dict)


def manage_comments(request):
    # get all the comments
    comments = Comment.objects.all()
    current_page = 'manage_comments'
    context_dict = {"comments": comments,
                    "current_page": current_page}

    return render(request, 'blog/manage_all_comments.html', context=context_dict)

def blog_delete_manage(request, blog_id):
    # delete_blog
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect(reverse('blog:mange_all_blogs'))

@login_required
def subscribe(request, blog_title_slug):    
    user = request.user.userProfile
    blog = Blog.objects.get(slug=blog_title_slug)
    author = blog.author.userProfile
    # add a new subscribe
    subscribe = Subscribe(user=user, author=author)
    subscribe.save()    
    comments = blog.comments.all().order_by("-date_posted")
    comment_form = CommentForm()
    return render(
        request,
        "blog/blog_detail.html",
        {"blog": blog, "comment_form": comment_form, "comments": comments, "subscribed": True},
    )

@login_required
def unsubscribe(request, blog_title_slug):    
    user = request.user.userProfile
    blog = Blog.objects.get(slug=blog_title_slug)
    author = blog.author.userProfile
    # unsubscribe
    Subscribe.objects.filter(user=user, author=author).delete()
    comments = blog.comments.all().order_by("-date_posted")
    comment_form = CommentForm()
    return render(
        request,
        "blog/blog_detail.html",
        {"blog": blog, "comment_form": comment_form, "comments": comments, "subscribed": False},
    )
