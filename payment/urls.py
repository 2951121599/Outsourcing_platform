from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/payment/jump
    url(r'^jump$', views.JumpView.as_view()),
    # http://127.0.0.1:8000/payment/result
    url(r'^result$', views.ResultView.as_view())
]