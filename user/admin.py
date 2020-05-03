from django.contrib import admin
from .models import User

# Register your models here.
admin.site.site_header = "众包网站后台管理界面"
admin.site.site_title = "后台管理界面"


class UserManager(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'nickname', 'name', 'description', 'created_time',
                    'updated_time']
    list_filter = ['username', 'nickname', 'name']
    search_fields = ['username', 'nickname', 'name']
    list_per_page = 10


admin.site.register(User, UserManager)
