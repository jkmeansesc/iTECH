from django.shortcuts import render, redirect

from .models import Blog
from .forms import BlogForm


# from django.core.mail import send_mail
# from .utils import send_mails

def index(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        else:
            print(form.errors)

        context_dict = {"message": "have a good day"}
        # 得到所有的blogs
        blogs = Blog.objects.all()
        context_dict["blogs"] = blogs
        # 将表单传递给模板
        form = BlogForm()
        context_dict["form"] = form

        return render(request, "blog/index.html", context=context_dict)

    else:

        context_dict = {"message": "have a good day"}
        # 得到所有的blogs
        blogs = Blog.objects.all()
        context_dict["blogs"] = blogs
        # 将表单传递给模板
        form = BlogForm()
        context_dict["form"] = form

        return render(request, "blog/index.html", context=context_dict)


def publish(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog_instance = form.save(commit=False)



            if 'image' in request.FILES:
                blog_instance.image = request.FILES['image']
            else:
                print("no image")

            blog_instance.save()

            return redirect("blog:index")
    else:
        context_dict = {"message": "have a good day"}
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
