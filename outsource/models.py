# -*- coding: utf-8 -*-
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


# 项目发布表
class PublishProject(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.IntegerField(verbose_name='项目类别')
    user_id = models.IntegerField(verbose_name="发包用户id")
    project_name = models.CharField(max_length=100, verbose_name="项目名称")
    post_datetime = models.DateTimeField(auto_now_add=True, verbose_name="发包时间")
    end_datetime = models.DateTimeField(auto_now=True, verbose_name="截止时间")
    skill = models.CharField(max_length=200, verbose_name="技能")
    cycles = models.IntegerField(verbose_name="开发周期")
    budget = models.CharField(max_length=20, verbose_name="预算")
    compete_state = models.BooleanField(default=0, verbose_name="竞标状态")
    # user = models.ForeignKey(User, verbose_name='用户')
    # category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类')
    # tag = models.ManyToManyField(Tag, verbose_name='标签')

    class Meta:
        db_table = "publish"
        verbose_name = "项目发布表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
