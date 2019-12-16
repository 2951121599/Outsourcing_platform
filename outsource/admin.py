from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(News)


class ProjectsAdmin(admin.ModelAdmin):
    list_display = (
        'project_name', 'kind', 'budget', 'language', 'cycles', 'project_desc', 'post_datetime', 'views', 'is_Active')
    list_editable = ('budget',)
    search_fields = ('project_name', 'kind')
    list_filter = ('project_name',)
    date_hierarchy = 'post_datetime'  # 基于日期的下拉导航
    fieldsets = (
        ('基本选项', {'fields': ('user', 'project_name', 'kind', 'budget', 'language', 'cycles', 'project_desc')}),
        ('高级选项', {'fields': ('views', 'is_Active')}),
    )


admin.site.register(Projects, ProjectsAdmin)
