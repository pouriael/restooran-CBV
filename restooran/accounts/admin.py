from email.headerregistry import Address
from django.contrib import admin
from .models import CouponProfile, formprofile
from django_jalali.admin.filters import JDateFieldListFilter

class profile_admin(admin.ModelAdmin):
    list_display = ['user','phone','address']

admin.site.register(formprofile,profile_admin)

class coupon_admin(admin.ModelAdmin):
    list_display = ['code','start','end','discount','active']
    list_filter = (
        ('code',JDateFieldListFilter),
    )

admin.site.register(CouponProfile,coupon_admin)
