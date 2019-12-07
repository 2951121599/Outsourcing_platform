# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  login_required.py
# 当前系统日期时间：2019/12/7，10:03
from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('islogin'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect(reverse('user:login'))

    return wrapper
