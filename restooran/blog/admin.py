from django.contrib import admin
from .models import *
import admin_thumbnails


class Blog_Admin(admin.ModelAdmin):
    list_display = ("name","create","update",)
    list_filter = ('create',)
admin.site.register(Blog,Blog_Admin)