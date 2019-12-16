import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import *
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
        return render(request, 'user/register.html', {'errmsg': '参数不能为空'})
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
        print(user)
        return render(request, 'user/user_center_info.html', locals())
    else:
        passport_id = request.session.get('passport_id')  # 数据表中的id
        user = User.objects.get(id=passport_id)
        return render(request, 'user/user_center_info.html', locals())


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
        return render(request, 'user/user_center_info.html')
