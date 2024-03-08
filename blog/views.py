from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import BlogForm, CommentForm
from .models import Blog, Comment
from .forms import BlogForm
from .utils import send_mails
from django.contrib.auth.decorators import login_required


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
            return render(request, "blog/publish1.html", context=context_dict)
    else:
        context_dict = {"message": "have a good day"}
        form = BlogForm()
        context_dict["form"] = form
        return render(request, "blog/publish1.html", context=context_dict)


def publish_comment(request, blog_title_slug):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=False)

            context_dict = {}
            try:
                comment = Comment.objects.get(blog=blog_title_slug)
                context_dict["comment"] = comment
            except Blog.DoesNotExist:
                context_dict["comment"] = None

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


def filter_blogs_author(request, author):
    context_dict = {}
    try:
        blogs = Blog.objects.filter(author=author)
        context_dict["blogs"] = blogs
    except Blog.DoesNotExist:
        context_dict["blogs"] = None

    return render(request, "blog/profile_blogs.html", context=context_dict)

def filter_comments_author(request, author):
    context_dict = {}
    try:
        comments = Comment.objects.filter(reviewer=author)
        context_dict["comments"] = comments
    except Comment.DoesNotExist:
        context_dict["comments"] = None

    return render(request, "blog/profile_comments.html", context=context_dict)

def about(request):
    return render(request, 'blog/about.html')


def blogs(request, tag=None):
    # Get all blogs
    blogs_all = Blog.objects.all()
    current_tag = tag

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

    return render(request, 'blog/blogs.html', context=context_dict)


def blog_detail(request, blog_title_slug):

    blog = get_object_or_404(Blog, slug=blog_title_slug)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():

            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            comment_form = CommentForm()
            comments = blog.comments.all().order_by('-date_posted')
            return render(request, 'blog/blog_detail1.html',
                          {'blog': blog, 'comment_form': comment_form, 'comments': comments})
    else:
        comment_form = CommentForm()

    # sort the comment by the latest date
    comments = blog.comments.all().order_by('-date_posted')
    return render(request, 'blog/blog_detail1.html',
                  {'blog': blog, 'comment_form': comment_form, 'comments': comments})


def search_results(request):
    return render(request, "blog/search_results.html")


def search_results(request):
    return render(request, 'blog/search_results.html')


def profile_settings(request):
    return render(request, 'blog/profile_settings.html')


def profile_blogs(request):
    return render(request, 'blog/profile_blogs.html')
