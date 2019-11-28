from django.shortcuts import render
from django.db import models
from .models import *


# Create your views here.
def index(request):
    projects = Project.objects.all()
    return render(request, 'trade/trade.html', locals())


def detail(request):
    projects = Project.objects.all()
    id = request.GET['id']
    # userinfo = UserInfo.objects.get(user=course.user)
    # comment = Comment.objects.filter(course=course)
    return render(request, 'trade/detail.html', locals())
