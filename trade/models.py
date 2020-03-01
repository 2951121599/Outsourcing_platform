from django.db import models
from user.models import User


# 项目分享
class Project(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, verbose_name="项目名称")
    link = models.URLField(max_length=100, default="", verbose_name="项目网址")
    desc = models.CharField(max_length=200, verbose_name="项目介绍")
    # like = models.IntegerField(default=0, verbose_name="点赞数")  点赞数存redis
    # 后台管理页面上传图片
    image_url = models.ImageField(upload_to='img', default="", verbose_name='图片路径')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = "trade_projects"
        verbose_name = '项目分享'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 用于记录点赞数量
class LikeNum(models.Model):
    project = models.OneToOneField(Project)
    like_num = models.IntegerField(default=0, verbose_name="点赞数")

    class Meta:
        db_table = "trade_likenum"
        verbose_name = '项目点赞数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project.title


# 点赞用户
class LikeUser(models.Model):
    like_user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    class Meta:
        db_table = "trade_likeuser"
        verbose_name = '项目点赞用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project.title
