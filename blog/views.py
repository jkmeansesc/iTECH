from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ArticleForm
from .models import Article

def index(request):
    context_dict = {'message': "have a good day"}
    return render(request, 'blog/index.html', context=context_dict)


def article_upload(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/url/')  # Edit to the true URL 
    else:
        form = ArticleForm()
    return render(request, 'upload.html', {'form': form})