import json
import re
from itertools import chain

from django.http import JsonResponse
from django.shortcuts import *

from outsource.models import Projects, Collection, Jingbiao, Confirm, Developers
from .models import *
from functions.decorators import login_required


# Create your views here.


def register(request):
    return render(request, 'user/register.html')


# 提交注册页的表单
def register_handle(request):
    # 获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    # 校正数据
    # 数据有空
    if not all([username, password, email]):
        return render(request, 'user/register.html', {'errmsg': '数据不能为空'})
    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'user/register.html', {'errmsg': '邮箱不正确'})
    # 业务处理，向系统中添加账户
    try:
        User.objects.add_one_passport(
            username=username,
            password=password,
            email=email
        )
    # 打印异常
    except Exception as e:
        print("e:", e)
        return render(request, 'user/register.html', {'errmsg': '用户名已存在'})
    # 注册完返回登录页
    return render(request, 'user/login.html')


# 显示登录页面
def login(request):
    # 如果能从cookies中获取到username则表示点击过“保存用户名”
    if request.COOKIES.get('username'):
        username = request.COOKIES.get('username')
        checked = 'checked'
    else:
        username = ''
        checked = ''
    context = {
        'username': username,
        'checked': checked,
    }
    return render(request, 'user/login.html', context)


# 验证登录
def login_check(request):
    # 1.获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    # 2.验证数据
    if not all([username, password, remember]):
        # 有数据为空
        return JsonResponse({"res": 2})

    # 3.进行处理：根据用户名和密码查找账户信息
    passport = User.objects.get_one_passport(username=username, password=password)
    if passport:
        turn_to = reverse('outsource:index')
        jres = JsonResponse({"res": 1, "turn_to": turn_to})

        # 是否记住用户名
        if remember == 'true':
            jres.set_cookie('username', username, max_age=7 * 24 * 3600)
        else:
            jres.delete_cookie('username')

        # 记住用户的登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        return jres
    else:
        # 用户名密码错误
        return JsonResponse({"res": 0})


# 登出
def logout(request):
    # 清除session信息
    request.session.flush()
    return redirect(reverse('outsource:index'))


@login_required
def user(request):
    if request.method == 'GET':
        passport_id = request.session.get('passport_id')  # 数据表中的id
        user = User.objects.get(id=passport_id)
        return render(request, 'user/user_center_info.html', locals())
    else:
        return HttpResponse("请使用GET请求数据!")


@login_required
def user_change(request):
    if request.method == 'GET':
        return render(request, 'user/change_user_info.html')
    elif request.method == 'POST':
        # 添加用户信息
        passport_id = request.session.get('passport_id')
        print("passport_id：---------------", passport_id)  # 数据表中的id
        user = User.objects.get(id=passport_id)
        if not user:
            return HttpResponse('Sorry~~~ user is not exist')
        phone = request.POST.get('phone')
        nickname = request.POST.get('nickname')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        # 保存数据
        user.phone = phone
        user.nickname = nickname
        user.name = name
        user.description = desc
        user.save()
        # return render(request, 'user/user_center_info.html')
        return redirect(reverse('user:user'))


def SuccessResponse(code):
    data = {}
    data['status'] = 'SUCCESS'
    data['code'] = code
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


# def collection(request):
#     if request.method == 'GET':
#         passport_id = request.session.get('passport_id')  # 数据表中的id
#         # user = User.objects.get(id=passport_id)
#         collection_obj = Collection.objects.filter(user_id=passport_id)
#         if not collection_obj:
#             item = {}
#             return render(request, 'user/collection.html', item)
#         item = {}
#         for project_obj in collection_obj:
#             # print(project_obj.projects_id_id)  # <QuerySet [<Projects: 众筹系统源码购买>]>
#             projects = Projects.objects.filter(id=project_obj.projects_id_id)
#             # ..........获取数据库的N条数据 存储为字典
#             item['projects'] = projects
#             print(item)
#             return render(request, 'user/collection.html', item)
#     else:
#         return HttpResponse('请使用GET进行请求!')
def collection(request):
    if request.method == 'GET':
        passport_id = request.session.get('passport_id')  # 数据表中的id
        # 收藏表中查询用户 得到收藏用户列表
        collection_obj = Collection.objects.filter(user_id=passport_id)

        # 收藏用户不存在 返回空
        if not collection_obj:
            item = {}
            return render(request, 'user/collection.html', item)
        # 收藏用户存在(多个) 得到多个收藏的项目id
        project_list = []
        for project_obj in collection_obj:
            # 得到每个具体的项目对象
            project1 = Projects.objects.filter(id=project_obj.projects_id_id)
            # 根据project_id从Jingbiao表里面查询竞标人数
            jingbiao_count = len(Jingbiao.objects.filter(project_id=project_obj.projects_id_id))
            print('+++++++++')
            print(jingbiao_count)
            project1.jingbiao_count = jingbiao_count
            project_list.append(project1)
        print(project_list)

        return render(request, 'user/collection.html', locals())


# 我发布的项目
def my_publish(request):
    if request.method == 'GET':
        passport_id = request.session.get('passport_id')
        project_list = Projects.objects.filter(user_id=passport_id)
        for project in project_list:
            # 根据project_id从Jingbiao表里面查询竞标人数
            project_id = project.id
            jingbiao_count = len(Jingbiao.objects.filter(project_id=project_id))
            # 给每一个project一个新的字段jingbiao_count
            project.jingbiao_count = jingbiao_count
        return render(request, 'user/my_publish.html', locals())


# 我开发的项目
def my_develop(request):
    if request.method == 'GET':
        # Confirm表中获取当前登录用户开发的项目
        passport_id = request.session.get('passport_id')  # 12
        try:
            developer_id = Developers.objects.filter(user_id=passport_id)[0]
            developer_id = developer_id.id  # 5
            project_list = Confirm.objects.filter(developer_id=developer_id)
            for project in project_list:
                # 根据project_id从Projects表里面查询项目信息
                project_id = project.project_id
                projects = Projects.objects.filter(id=project_id)
        except Exception as e:
            print(e)
            return redirect(reverse('outsource:reg_dev'))
        print('----------', locals())
        return render(request, 'user/my_develop.html', locals())


# 我竞标的项目
def my_jingbiao(request):
    if request.method == 'GET':
        passport_id = int(request.session.get('passport_id'))  # 12
        jingbiao_projects_obj = Jingbiao.objects.filter(user_id=passport_id)
        temp = Jingbiao.objects.none()
        jingbiao_list = []
        for i in jingbiao_projects_obj:
            jingbiao_projects = Projects.objects.filter(id=i.project_id)  # 10 14 15
            jingbiao_list.append(jingbiao_projects)
        for i in jingbiao_list:
            temp = temp | i
        jingbiao_list = chain(temp)
        print('*******/*/*', jingbiao_list)
    return render(request, 'user/my_jingbiao.html', locals())
