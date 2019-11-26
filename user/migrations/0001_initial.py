# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-25 04:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=50, verbose_name='手机号')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('name', models.CharField(max_length=50, verbose_name='真实姓名')),
                ('description', models.TextField(max_length=300, verbose_name='个人描述')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
    ]