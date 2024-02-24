from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    context_dict = {'message': "have a good day"}
    return render(request, 'blog/index.html', context=context_dict)

