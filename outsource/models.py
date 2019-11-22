from django.db import models


# Create your models here.
# 用户信息表
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=50)
    email = models.EmailField('邮箱', max_length=50)
    phone = models.CharField('手机号', max_length=50)
    nickname = models.CharField('昵称', max_length=50)
    name = models.CharField('真实姓名', max_length=50)
    # sex = models.BooleanField('性别')
    description = models.TextField('个人描述', max_length=300)
