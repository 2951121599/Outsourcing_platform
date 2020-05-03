from django.contrib import admin
from .models import *


class ProjectsAdmin(admin.ModelAdmin):
    list_display = (
        'project_name', 'kind', 'budget', 'language', 'cycles', 'post_datetime', 'is_Active')
    search_fields = ['project_name']
    list_filter = ['kind', 'language', 'budget', 'is_Active']
    # fieldsets = (
    #     ('基本选项', {'fields': ('user', 'project_name', 'kind', 'budget', 'language', 'cycles', 'project_desc')}),
    #     ('高级选项', {'fields': ('views', 'is_Active')}),
    # )
    list_per_page = 10


class DevelopersManager(admin.ModelAdmin):
    list_display = ['user', 'name', 'nickname', 'email', 'phone', 'work_status', 'work_direction', 'language_direction',
                    'score']
    list_filter = ['work_status', 'work_direction', 'language_direction', 'score']
    search_fields = ['name']
    list_per_page = 10


class CollectionManager(admin.ModelAdmin):
    list_display = ['user', 'projects_id']
    list_filter = ['user', 'projects_id']
    list_per_page = 10
    ordering = ['-user']


class JingbiaoManager(admin.ModelAdmin):
    list_display = ['project', 'user']
    list_filter = ['project', 'user']
    list_per_page = 10
    ordering = ['project']


class ConfirmManager(admin.ModelAdmin):
    list_display = ['project', 'user', 'developer']
    list_filter = ['project', 'user', 'developer']
    list_per_page = 10
    ordering = ['project']


admin.site.register(News)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Developers, DevelopersManager)
admin.site.register(Collection, CollectionManager)
admin.site.register(Jingbiao, JingbiaoManager)
admin.site.register(Confirm, ConfirmManager)
admin.site.register(LanguageChoice)
admin.site.register(KindChoice)
