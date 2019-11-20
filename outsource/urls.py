# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  urls.py
# 当前系统日期时间：2019/11/19，17:20 
from django.conf.urls import url
from . import views

app_name = "outsource"
urlpatterns = [
    url(r'^', views.index, name="主页"),
    url(r'^index', views.index, name="主页"),
]
