from django.conf.urls import url
from django.conf import settings
from . import views
from django.views.static import serve
from django.conf.urls.static import static

app_name = "outsource"
urlpatterns = [
    # 主页
    # http://127.0.0.1:8000/
    url(r'^$', views.index, name='index'),
    # http://127.0.0.1:8000/index/
    url(r'^index$', views.index),

    # 图片上传
    url(r'^media/(?P<path>.*)$', serve, {'media_root': settings.MEDIA_ROOT}),

    # 项目列表页
    # http://127.0.0.1:8000/projects
    url(r'^projects$', views.projects, name='projects'),

    # 项目详情页
    # http://127.0.0.1:8000/projects/detail/projects_id
    url(r'^projects/detail/(?P<projects_id>\d+)$', views.projects_detail, name='detail'),

    # 发包方详情页
    # http://127.0.0.1:8000/publisher/detail/publisher_id
    url(r'^publisher/detail/(\d+)$', views.publisher_detail, name='publisher_detail'),

    # 开发者列表页
    # http://127.0.0.1:8000/developers
    url(r'^developers$', views.developers, name='developers'),

    # 开发者搜索页
    # http://127.0.0.1:8000/search
    url(r'^search$', views.developers_search, name='developers_search'),

    # 开发者详情页
    # http://127.0.0.1:8000/developers/detail/developers_id
    url(r'^developers/detail/(\d+)$', views.developers_detail, name='developers_detail'),

    # 帮助页
    # http://127.0.0.1:8000/help
    url(r'^help$', views.help_menu, name='help'),

    # 项目发布页
    # http://127.0.0.1:8000/publish
    url(r'^publish$', views.publish, name='publish'),

    # 申请开发者页
    # http://127.0.0.1:8000/reg_dev
    url(r'^reg_dev$', views.reg_dev, name="reg_dev"),

    # 需求方帮助页
    # http://127.0.0.1:8000/help/guide1
    url(r'^help/guide1$', views.guide1, name='guide1'),

    # 开发者帮助页
    # http://127.0.0.1:8000/help/guide2
    url(r'^help/guide2$', views.guide2, name='guide2'),

    # 项目收藏
    # http://127.0.0.1:8000/collection
    url(r'^collection/$', views.collection, name='collection'),

    # 项目竞标
    # http://127.0.0.1:8000/jingbiao
    url(r'^jingbiao/$', views.jingbiao, name='jingbiao'),

    # 结束竞标
    # http://127.0.0.1:8000/zhongbiao/1
    url(r'^zhongbiao/(\d+)$', views.zhongbiao, name='zhongbiao'),

    # 确认开发者
    # http://127.0.0.1:8000/confirm
    url(r'^confirm$', views.confirm, name='confirm'),

    # PDF文件下载
    # http://127.0.0.1:8000/file_down
    url(r'^file_down$', views.file_down, name='file_down'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
