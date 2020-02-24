from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "trade"
urlpatterns = [
    # http://127.0.0.1:8000/trade
    url(r'^$', views.index, name='index'),

    # http://127.0.0.1:8000/trade/like
    url(r'^like', views.like, name='like'),

    # http://127.0.0.1:8000/trade/push
    url(r'^push', views.push, name='push'),

    # http://127.0.0.1:8000/trade/mine
    url(r'^mine', views.mine, name='mine'),

    # http://127.0.0.1:8000/trade/require
    url(r'^require', views.require, name='require'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
