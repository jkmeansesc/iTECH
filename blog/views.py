from django.shortcuts import render, redirect

from .models import Blog
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


            if 'image' in request.FILES:
                blog_instance.image = request.FILES['image']
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


def about(request):
    return render(request, 'blog/about.html')


def blogs(request):
    # Get all blogs
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        else:
            print(form.errors)

        blogs_all = Blog.objects.all()
        context_dict = {"blogs_all": blogs_all}
        form = BlogForm()
        context_dict["form"] = form

        return render(request, 'blog/blogs.html', context=context_dict)
    else:
        blogs_all = Blog.objects.all()
        context_dict = {"blogs_all": blogs_all}
        form = BlogForm()
        context_dict["form"] = form

        return render(request, 'blog/blogs.html', context=context_dict)



def blog_detail(request, blog_title_slug):
    context_dict = {}
    try:
        blog = Blog.objects.get(slug=blog_title_slug)
        context_dict["blog"] = blog
    except Blog.DoesNotExist:
        context_dict["blog"] = None

    return render(request, 'blog/blog_detail1.html', context=context_dict)




def search_results(request):
    return render(request, 'blog/search_results.html')
