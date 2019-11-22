from django.db import models


# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="项目名称")
    tag = models.CharField(max_length=20, verbose_name="标签")
    content = models.CharField(max_length=200, verbose_name="项目介绍")
    collection = models.IntegerField(verbose_name="收藏")
    comments = models.CharField(max_length=200, verbose_name="评论")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '项目交易'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
