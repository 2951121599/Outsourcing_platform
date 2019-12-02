# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  urls.py
# 当前系统日期时间：2019/11/19，17:20 
from django.conf.urls import url
from django.conf import settings
from . import views
from django.views.static import serve

app_name = "outsource"
urlpatterns = [
    # http://127.0.0.1:8000/
    url(r'^$', views.index),
    # http://127.0.0.1:8000/index/
    url(r'^index$', views.index),
    # 图片上传
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # http://127.0.0.1:8000/projects
    url(r'^projects$', views.projects),
    # http://127.0.0.1:8000/projects/detail/projects_id  项目详情页
    url(r'^projects/detail/(\d+)$', views.detail_projects),
    # http://127.0.0.1:8000/developers
    url(r'^developers$', views.developers),
    # http://127.0.0.1:8000/cases/detail/projects_id  案例详情页
    url(r'^cases/detail/(\d+)$', views.cases_projects),
    # http://127.0.0.1:8000/help
    url(r'^help$', views.help_menu),
    # http://127.0.0.1:8000/publish
    url(r'^publish$', views.publish),
    # # http://127.0.0.1:8000/reg
    # url(r'^reg$', views.reg),
    # # http://127.0.0.1:8000/login
    # url(r'^login$', views.login),
    # # http://127.0.0.1:8000/user
    # url(r'^user$', views.user),
    # http://127.0.0.1:8000/help/guide1
    url(r'^help/guide1$', views.guide1),
    # http://127.0.0.1:8000/help/guide2
    url(r'^help/guide2$', views.guide2),
]
