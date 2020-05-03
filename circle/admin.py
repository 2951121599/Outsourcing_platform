from django.contrib import admin

from .models import Questions, Comments


# 定义模型管理器类
class QuestionsManager(admin.ModelAdmin):
    list_display = ['user', 'title', 'content', 'created_time']
    list_filter = ['user', 'title']
    search_fields = ['title', 'content']


class CommentsManager(admin.ModelAdmin):
    list_display = ['user', 'question', 'comment', 'created_time', 'updated_time']
    list_filter = ['user', 'question']
    list_editable = ['comment']
    search_fields = ['comment']
    list_per_page = 5


admin.site.register(Questions, QuestionsManager)
admin.site.register(Comments, CommentsManager)
