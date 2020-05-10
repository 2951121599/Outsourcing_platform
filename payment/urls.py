from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/payment/jump
    url(r'^jump$', views.JumpView),
    # http://127.0.0.1:8000/payment/result
    url(r'^result$', views.ResultView)
]
