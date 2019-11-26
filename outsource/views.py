from django.http import *
from django.shortcuts import render
from outsource.models import PublishProject


# Create your views here.

def logging_check(fn):
    def wrap(request, *args, **kwargs):
        # 检查登录状态
        # session没登录
        if not request.session.get('uid') or not request.session.get('username'):
            # cookies没登录
            if not request.COOKIES.get('uid') or not request.COOKIES.get('username'):
                return HttpResponseRedirect('/user/login')
            # 有cookies
            else:
                # 有cookies 回写session
                uid = request.COOKIES.get('uid')
                username = request.COOKIES.get("username")
                request.session['uid'] = uid
                request.session['username'] = username
        # 1.将用户的uid绑定给request对象 传递给视图函数
        uid = request.session.get('uid')
        # 2.直接查询出用户数据 将用户对象绑定给request
        # user = User.Objects.get(id = uid)
        # request.my_user = user
        request.my_uid = uid
        return fn(request, *args, **kwargs)

    return wrap


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


@logging_check
def publish(request):
    if request.method == 'GET':
        return render(request, 'outsource/publish.html')
    elif request.method == 'POST':
        # 处理数据
        class_id = request.POST.get('class_id')
        project_name = request.POST.get('project_name')
        # kind 类似 remember
        kind = request.POST.getlist('kind', [])
        # budget
        budget = request.POST.get('budget')
        # 项目描述
        project_descrption = request.POST.get('project_descrption')
        # 创建
        PublishProject.objects.create(class_id=class_id, project_name=project_name, kind=kind, budget=budget,
                                      project_descrption=project_descrption, user_id=request.my_uid)
        return render(request, 'outsource/publish.html', locals())


def reg(request):
    return render(request, 'outsource/reg.html')


def login(request):
    return render(request, 'outsource/login.html')


def user(request):
    return render(request, 'outsource/user.html')


def guide1(request):
    return render(request, 'outsource/guide1.html')


def guide2(request):
    return render(request, 'outsource/guide2.html')
