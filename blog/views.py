from django.shortcuts import render

from .forms import BlogForm
from .models import Blog
from .forms import BlogForm


# from django.core.mail import send_mail
# from .utils import send_mails


def index(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():

            form.save(commit=False)
            context_dict = {"message": "have a good day"}
            blogs = Blog.objects.all()
            context_dict["blogs"] = blogs
            form = BlogForm()
            context_dict["form"] = form

            # update the images
            if 'image' in request.FILES:
                form.image = request.FILES['image']

            form.save()

            return render(request, "blog/publish.html", context=context_dict)
        else:
            print(form.errors)

    else:

        context_dict = {"message": "have a good day"}
        blogs = Blog.objects.all()
        context_dict["blogs"] = blogs
        form = BlogForm()
        context_dict["form"] = form

        return render(request, "blog/publish.html", context=context_dict)


def publish(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():

            form.save(commit=False)
            context_dict = {"message": "have a good day"}
            blogs = Blog.objects.all()
            context_dict["blogs"] = blogs
            form = BlogForm()
            context_dict["form"] = form

            # update the images
            if 'image' in request.FILES:
                form.image = request.FILES['image']

            form.save()

            return render(request, "blog/publish.html", context=context_dict)
        else:
            print(form.errors)

    else:

        context_dict = {"message": "have a good day"}
        blogs = Blog.objects.all()
        context_dict["blogs"] = blogs
        form = BlogForm()
        context_dict["form"] = form

        return render(request, "blog/publish.html", context=context_dict)


def about(request):
    return render(request, 'blog/about.html')


def blogs(request):
    return render(request, 'blog/blogs.html')


def blog_detail(request):
    return render(request, 'blog/blog_detail.html')


def search_results(request):
    return render(request, 'blog/search_results.html')
