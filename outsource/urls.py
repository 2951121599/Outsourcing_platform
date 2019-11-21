# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  urls.py
# 当前系统日期时间：2019/11/19，17:20 
from django.conf.urls import url
from . import views

app_name = "outsource"
urlpatterns = [
    # http://127.0.0.1:8000/
    url(r'^$', views.index),
    # http://127.0.0.1:8000/index
    url(r'^index$', views.index),
    # http://127.0.0.1:8000/projects
    url(r'^projects$', views.projects),
    # http://127.0.0.1:8000/reg
    url(r'^reg$', views.reg),
]
