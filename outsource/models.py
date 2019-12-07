# -*- coding: utf-8 -*-
from django.db import models
from user.models import User
from outsource.enums import *


# Create your models here.
# 主页新闻列表页
class News(models.Model):
    news_title = models.CharField(max_length=50, verbose_name="新闻标题")
    news_tip = models.CharField(max_length=100, verbose_name="文章摘要")
    image_url = models.ImageField(upload_to='news/%Y/%m', verbose_name='图片路径')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '新闻列表页'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.news_title


class ProjectsManager(models.Manager):
    # sort = 'new' 按照创建时间排序
    # sort = 'hot' 按照关注度排序
    # sort = 'price' 按照价格进行排序
    # sort = 'default' 默认排序
    # sort = 'kind' 按照类别分类 (未做)
    def get_projects_by_type(self, kind, limit=None, sort='default'):
        if sort == 'new':
            order_by = ('-post_datetime',)
        elif sort == 'budget':
            order_by = ('budget',)
        elif sort == 'hot':
            order_by = ('-views',)
        else:
            order_by = ('-pk',)
            # 按照primary_key降序排列
        # 查询结果
        projects_li = self.filter(kind=kind).order_by(*order_by)
        # 查看结果集的限制
        if limit:
            projects_li = projects_li[:limit]
            print(projects_li)
        return projects_li

    def get_projects_by_id(self, projects_id):
        try:
            projects = self.get(id=projects_id)
        except self.model.DoesNotExist:
            projects = None
        return projects


# 项目(发布)表
class Projects(models.Model):
    # class_id = models.IntegerField(verbose_name='项目类别')
    # PROJECTS_TYPE = (
    #     (u'APP', u'APP'),
    #     (u'桌面应用', u'桌面应用'),
    #     (u'管理系统', u'管理系统'),
    #     (u'PC网站', u'PC网站'),
    #     (u'UI设计', u'UI设计'),
    #     (u'微信开发', u'微信开发'),
    #     (u'游戏开发', u'游戏开发'),
    #     (u'其它分类', u'其它分类'),
    # )

    # LANGUAGE_TYPE = (
    #     ('Python', 'Python'),  # 前面是展示在前端界面的内容,后面的是真正存在数据库中的
    #     ('C', 'C'),
    #     ('C++', 'C++'),
    #     ('C#', 'C#'),
    #     ('Java', 'Java'),
    #     ('Android', 'Android'),
    # )
    projects_type_choices = ((k, v) for k, v in PROJECTS_TYPE.items())
    develop_language_choices = ((k, v) for k, v in DEVELOP_LANGUAGE.items())
    user = models.ForeignKey(User)  # 外键关联 用户表(一对多)
    project_name = models.CharField(max_length=100, verbose_name="项目名称")
    kind = models.SmallIntegerField(choices=projects_type_choices, default=OTHER, verbose_name="项目类别")
    budget = models.CharField(max_length=20, verbose_name="预算", null=True)
    # language = models.CharField(max_length=100, choices=PROJECTS_TYPE, default="other", verbose_name="开发语言")
    language = models.SmallIntegerField(choices=develop_language_choices, default=Other, verbose_name="开发语言")
    cycles = models.IntegerField(verbose_name="开发周期", null=True)
    project_desc = models.TextField(max_length=300, default="项目描述", verbose_name="项目描述")
    post_datetime = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    views = models.IntegerField(default=0, verbose_name='浏览数量')
    is_Active = models.BooleanField(default=True, verbose_name="项目状态")  # 默认True代表发布状态 False代表已成功接单

    # category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类')
    # tag = models.ManyToManyField(Tag, verbose_name='标签')
    objects = ProjectsManager()

    class Meta:
        db_table = "projects"
        verbose_name = "项目表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.project_name)


class KindChoice(models.Model):
    kind_name = models.CharField(max_length=30, default="其它分类", verbose_name='项目类别')

    class Meta:
        db_table = "kind_choice"
        verbose_name = "项目类别选择表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str("%s" % self.kind_name)


class LanguageChoice(models.Model):
    language_name = models.CharField(max_length=30, default="暂无", verbose_name='开发语言')

    class Meta:
        db_table = "language_choice"
        verbose_name = "开发语言选择表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str("%s" % self.language_name)


class PublishProject(models.Model):
    user = models.ForeignKey(User)  # 外键关联 用户表(一对多)
    project_name = models.CharField(max_length=100, null=False, verbose_name="项目名称")
    kind = models.CharField(max_length=100, default=OTHER, verbose_name="项目类别")
    budget = models.CharField(max_length=20, blank=True, null=True, verbose_name="预算")
    language = models.CharField(max_length=100, default=Other, verbose_name="开发语言")
    cycles = models.IntegerField(verbose_name="开发周期", blank=True, null=True)
    project_desc = models.TextField(max_length=500, default="项目描述", verbose_name="项目描述")
    post_datetime = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        db_table = "publish_project"
        verbose_name = "发布项目表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.project_name)
