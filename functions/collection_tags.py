# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  collection_tags.py
# 当前系统日期时间：2019/12/19，13:09 
from django import template
from django.contrib.contenttypes.models import ContentType
from outsource.models import Collection

register = template.Library()


@register.simple_tag(takes_context=True)
def get_collection_status(context):
    user = context['user']
    projects_id = context['projects_id']
    if Collection.objects.filter(projects_id=projects_id, user=user).exists():
        return 'active'
    else:
        return ""
