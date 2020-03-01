from django.contrib import admin
from .models import User

# Register your models here.
admin.site.site_header = "众包网站后台管理界面"
admin.site.site_title = "后台管理界面"
admin.site.register(User)
