
#from home.models import *
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from phone_field import PhoneField
from django_jalali.db import models as jmodels
from django import forms
from location_field.forms.plain import PlainLocationField
from django_jalali.db import models as jmodels

class Address(forms.Form):
    city = forms.CharField()
    location = PlainLocationField(based_fields=['city'],
                                  initial='-22.2876834,-49.1607606')

class formprofile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,verbose_name = 'کاربر',)
    phone = PhoneField(null=True,blank=True,verbose_name = 'شماره همراه')
    address = models.CharField(max_length=50,null=True,blank=True,verbose_name = 'آدرس')
    profile_image = models.ImageField(upload_to = 'profile/',default="",null =True,blank=True,verbose_name = 'عکس پروفایل')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها '

    def __str__(self) :
        return self.user.username

class CouponProfile(models.Model):
    code = models.CharField(max_length=100,unique=True,verbose_name = 'کد تخفیف')
    active = models.BooleanField(default= False,verbose_name = 'آیا فعال است؟')
    start = jmodels.jDateTimeField(verbose_name = 'شروع')
    end = jmodels.jDateTimeField(verbose_name = 'پایان')
    discount = models.IntegerField(verbose_name = 'درصد تخفیف')
    dastresi = models.ManyToManyField(User,blank=True)



def profile_signals(sender,**kwargs):
    if kwargs["created"]:
        profile_user = formprofile(user = kwargs["instance"])
        profile_user.save() 

post_save.connect(profile_signals,sender= User)


