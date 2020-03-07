from django.conf.urls import url
from user import views

app_name = 'user'
urlpatterns = [
    url(r'^$', views.user, name='user'),
    url(r'^collection/$', views.collection, name='collection'),
    url(r'^user_change/$', views.user_change, name='user_change'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^my_publish/$', views.my_publish, name='my_publish'),
    url(r'^my_develop/$', views.my_develop, name='my_develop'),
    url(r'^my_jingbiao/$', views.my_jingbiao, name='my_jingbiao'),
]
