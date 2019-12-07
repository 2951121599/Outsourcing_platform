from django.conf.urls import url
from user import views

app_name = 'user'
urlpatterns = [
    url(r'^$', views.user, name='user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'),
    # # http://127.0.0.1:8000/user
    # url(r'^$', views.user),
    # # http://127.0.0.1:8000/index
    # url(r'^index$', views.index_view),
    # # http://127.0.0.1:8000/user/reg
    # url(r'^reg$', views.reg),
    # # http://127.0.0.1:8000/user/login
    # url(r'^login$', views.login_view, name="login"),
    # # http://127.0.0.1:8000/user/logout
    # url(r'^logout$', views.logout_view),

]
