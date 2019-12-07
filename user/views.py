import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import *
from .models import *
import hashlib
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
    # 开发中，注册完返回登录页
    # return redirect(reverse('use'))
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
    passport_id = request.session.get('passport_id')
    print(passport_id)  # 数据表中的id
    print(locals())
    return render(request, 'user/user_center_info.html', locals())

# def logging_check(fn):
#     def wrap(request, *args, **kwargs):
#         # 检查登录状态
#         # session没登录
#         if not request.session.get('uid') or not request.session.get('username'):
#             # cookies没登录
#             if not request.COOKIES.get('uid') or not request.COOKIES.get('username'):
#                 return HttpResponseRedirect('/user/login')
#             # 有cookies
#             else:
#                 # 有cookies 回写session
#                 uid = request.COOKIES.get('uid')
#                 username = request.COOKIES.get("username")
#                 request.session['uid'] = uid
#                 request.session['username'] = username
#         # 1.将用户的uid绑定给request对象 传递给视图函数
#         uid = request.session.get('uid')
#         # 2.直接查询出用户数据 将用户对象绑定给request
#         # user = User.Objects.get(id = uid)
#         # request.my_user = user
#         request.my_uid = uid
#         return fn(request, *args, **kwargs)
#
#     return wrap


# def reg_view(request):
#     if request.method == 'GET':
#         return render(request, 'user/register.html')
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         password_1 = request.POST.get('password_1')
#         password_2 = request.POST.get('password_2')
#         # 判断是否存在
#
#         # 判断username是否已被注册
#         users = User.objects.filter(username=username)
#         if users:
#             # 用户名已注册
#             return HttpResponse("用户名已被注册! ")
#         if password_1 != password_2:
#             return HttpResponse("两次密码不相同! ")
#         # hash md5 加密明文密码
#         m = hashlib.md5()
#         m.update(password_1.encode())
#         try:
#             # 创建成功 用一个对象接收一下
#             user = User.objects.create(username=username, password=m.hexdigest())
#         except Exception as e:
#             print("注册失败! ")
#             print(e)
#             return HttpResponse("服务器繁忙! ")
#         # 注册成功
#         # 存储cookies,两个 uid 和 username 有效期一天
#         resp = HttpResponse("注册成功! ")
#         resp.set_cookie("uid", user.id, 3600 * 24)
#         resp.set_cookie("username", username, 3600 * 24)
#         return resp

# def login_view(request):
#     if request.method == 'GET':
#         # 1.优先检查session
#         if request.session.get('uid') and request.session.get('username'):
#             # 登陆过
#             # return HttpResponse("你已经登陆过了!")
#             return HttpResponseRedirect('/index')
#         # 2.没session 检查cookies
#         uid = request.COOKIES.get('uid')
#         username = request.COOKIES.get('username')
#         if uid and username:
#             # 证明用户之前点击过 checkbox
#             # 3.有 cookies 回写session
#             request.session['uid'] = uid
#             request.session['username'] = username
#             return HttpResponse("你已经登陆过了!!")
#
#         return render(request, 'user/login.html')
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # remember = request.POST.get("remember")
#         old_users = User.objects.filter(username=username)
#         if not old_users:
#             # 提示此信息 是防止用户撞库  实则是用户名未注册
#             return HttpResponse("用户名或密码错误!")
#
#         # 校验密码
#         m = hashlib.md5()
#         m.update(password.encode())
#         user = old_users[0]
#         if user.password != m.hexdigest():
#             # 密码错误
#             return HttpResponse("用户名或密码错误!")
#
#         # 保存登录状态
#         # 1.先存session
#         request.session['uid'] = user.id
#         request.session['username'] = user.username
#
#         # 2.检查是否要存cookies
#         resp = HttpResponseRedirect('/index')
#         # resp = HttpResponse("登陆成功")
#         if 'remember' in request.POST.keys():
#             # 3.用户勾选了 存cookies 记住用户名
#             resp.set_cookie("uid", user.id, 3600 * 24 * 30)
#             resp.set_cookie("username", username, 3600 * 24 * 30)
#         return resp
#
#
# def logout_view(request):
#     # 登出
#     # 删除 session
#     if 'uid' in request.session:
#         del request.session['uid']
#     if 'username' in request.session:
#         del request.session['username']
#     # 删除cookies
#     resp = HttpResponse("已登出! ")
#     if 'uid' in request.COOKIES:
#         resp.delete_cookie('uid')
#     if 'username' in request.COOKIES:
#         resp.delete_cookie('username')
#     return resp
#
#
# @logging_check
# def index_view(request):
#     uid = request.my_uid
#     return HttpResponseRedirect('outsource/index.html', locals())
#
#
# def user(request):
#     return render(request, 'user/user.html')
