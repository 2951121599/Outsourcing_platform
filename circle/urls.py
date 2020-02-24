from django.conf.urls import url
from . import views

app_name = "circle"
urlpatterns = [
    # http://127.0.0.1:8000/circle
    url(r'^$', views.index, name='index'),

    # 发表新帖
    # http://127.0.0.1:8000/circle/jie/add
    url(r'^jie/add$', views.add, name='add'),

    # 帖子(问题)详情页
    # http://127.0.0.1:8000/circle/jie/detail/question_id
    url(r'^jie/detail/(?P<question_id>\d+)$', views.question_detail, name='detail'),

    # 回复评论
    # http://127.0.0.1:8000/circle/jie/reply/
    url(r'^jie/reply$', views.reply, name='reply'),

    # http://127.0.0.1:8000/circle/user/home/user_id 用户首页
    url(r'^user/home/(?P<user_id>\d+)$', views.home, name='home'),
]
