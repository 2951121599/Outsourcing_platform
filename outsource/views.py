from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'outsource/index.html')


def projects(request):
    return render(request, 'outsource/projects.html')


def reg(request):
    return render(request, 'outsource/reg.html')
