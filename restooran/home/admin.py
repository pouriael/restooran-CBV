from django.contrib import admin
from .models import *
import admin_thumbnails

class Category_Admin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {
        'slug':("name",)
    }
admin.site.register(Category,Category_Admin)

class Product_Admin(admin.ModelAdmin):
    list_display = ['name','available','unit_price','discount','total_price']
    list_filter = ('available',)
    raw_id_fields = ('category',)
   
admin.site.register(Product,Product_Admin)
admin.site.register(Gallery)
admin.site.register(Shahr)
admin.site.register(Shobe)