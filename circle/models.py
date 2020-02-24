from django.db import models
from user.models import User


# 发帖
class Questions(models.Model):
    user = models.ForeignKey(User)  # 外键关联 用户表(一对多)
    title = models.CharField(max_length=100, verbose_name="发帖标题")
    content = models.CharField(max_length=500, verbose_name="发帖内容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = "questions"
        verbose_name = "发布新帖表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)


# 评论
class Comments(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Questions)
    comment = models.CharField(max_length=500, verbose_name="评论内容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "comments"
        verbose_name = "帖子评论表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.comment)
