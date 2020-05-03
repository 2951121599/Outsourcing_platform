from django.contrib import admin
from .models import *


# Register your models here.

class ProjectManager(admin.ModelAdmin):
    list_display = ['user', 'title', 'link', 'desc', 'add_time']
    list_display_links = ['title', 'link']
    list_filter = ['title']
    search_fields = ['title', 'desc']
    list_per_page = 10


class LikeNumManager(admin.ModelAdmin):
    list_display = ['project', 'like_num']
    list_display_links = ['project']
    list_filter = ['project']
    search_fields = ['project']
    list_per_page = 10


class LikeUserManager(admin.ModelAdmin):
    list_display = ['project', 'like_user']
    list_display_links = ['project']
    list_filter = ['project']
    search_fields = ['project']
    list_per_page = 10
    ordering = ('project',)


admin.site.register(Project, ProjectManager)
admin.site.register(LikeNum, LikeNumManager)
admin.site.register(LikeUser, LikeUserManager)
