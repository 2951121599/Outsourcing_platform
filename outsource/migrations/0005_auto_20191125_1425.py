# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-25 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outsource', '0004_auto_20191125_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publishproject',
            name='compete_state',
        ),
        migrations.AlterField(
            model_name='publishproject',
            name='cycles',
            field=models.IntegerField(null=True, verbose_name='开发周期'),
        ),
    ]