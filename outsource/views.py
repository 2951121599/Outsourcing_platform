from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'outsource/index.html')


def projects(request):
    return render(request, 'outsource/projects.html')


def detail_projects(request):
    return render(request, 'outsource/detail_projects.html')


def cases(request):
    return render(request, 'outsource/cases.html')


def cases_projects(request):
    return render(request, 'outsource/detail_cases.html')


def help_menu(request):
    return render(request, 'outsource/help.html')


def publish(request):
    return render(request, 'outsource/publish.html')


def reg(request):
    return render(request, 'outsource/reg.html')


def login(request):
    return render(request, 'outsource/login.html')


def user(request):
    return render(request, 'outsource/user.html')
