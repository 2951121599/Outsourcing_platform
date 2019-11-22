from django.shortcuts import render
from django.db import models

# Create your views here.
def index(request):
    return render(request, 'trade/index.html')


    # def detail(request):
    #     project = models.Project.objects.all()
    #     id = request.GET['id']
    # course = models.Project.objects.get(pk=id)
    # userinfo = UserInfo.objects.get(user=course.user)
    # comment = models.Comment.objects.filter(course=course)
    # return render(request, 'course/detail.html',
    #               {'course': course, 'userinfo': userinfo, 'course_type': course_type, 'comment': comment})
