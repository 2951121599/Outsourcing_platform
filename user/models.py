from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    phone = models.CharField(max_length=50, verbose_name='手机号')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    name = models.CharField(max_length=50, verbose_name='真实姓名')
    description = models.TextField(max_length=300, verbose_name='个人描述')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return "用户" + self.username
