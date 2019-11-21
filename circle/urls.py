# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  urls.py
# 当前系统日期时间：2019/11/21，13:03 
from django.conf.urls import url
from . import views

app_name = "circle"
urlpatterns = [
    # http://127.0.0.1:8000/circle
    url(r'^$', views.index),
    # http://127.0.0.1:8000/circle/index
    url(r'^index$', views.index),
]
