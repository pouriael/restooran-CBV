from django.contrib import admin
from .models import *


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user','product','quantity',"price"]

class Order_Admin(admin.ModelAdmin):
    list_display = ['user','f_name','l_name','email','create','address','paid','get_price','code']
    inlines = [ItemInline]


 
admin.site.register(ItemOrder)
admin.site.register(Order,Order_Admin)

class ErsalOrder_Admin(admin.ModelAdmin):
    list_display = ['ersal','hazine']

admin.site.register(ErsalOrder,ErsalOrder_Admin)