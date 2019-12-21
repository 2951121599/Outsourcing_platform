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
    url(r'^$', views.index, name='index'),
    # http://127.0.0.1:8000/index/
    url(r'^index$', views.index),
    # # http://127.0.0.1:8000/news/detail/projects_id  新闻详情页
    # url(r'^news/detail/(\d+)$', views.news_detail),
    # 图片上传
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # http://127.0.0.1:8000/projects
    url(r'^projects$', views.projects, name='projects'),
    # 分类列表页
    url(r'^projects/(?P<kind>\d+)/(?P<page>\d+)/$', views.projects_list, name='projects_list'),  # 列表页
    # http://127.0.0.1:8000/projects/detail/projects_id  项目详情页
    url(r'^projects/detail/(?P<projects_id>\d+)$', views.projects_detail, name='detail'),
    # http://127.0.0.1:8000/developers
    url(r'^developers$', views.developers),
    # http://127.0.0.1:8000/developers/detail/developers_id  开发者详情页
    url(r'^developers/detail/(\d+)$', views.developers_detail),
    # http://127.0.0.1:8000/help
    url(r'^help$', views.help_menu),
    # http://127.0.0.1:8000/publish
    url(r'^publish$', views.publish),
    # http://127.0.0.1:8000/reg_dev
    url(r'^reg_dev$', views.reg_dev, name="reg_dev"),
    # # http://127.0.0.1:8000/login
    # url(r'^login$', views.login),
    # # http://127.0.0.1:8000/user
    # url(r'^user$', views.user),
    # http://127.0.0.1:8000/help/guide1
    url(r'^help/guide1$', views.guide1),
    # http://127.0.0.1:8000/help/guide2
    url(r'^help/guide2$', views.guide2),
    # http://127.0.0.1:8000/collection
    url(r'^collection/$', views.collection, name='collection'),

]
