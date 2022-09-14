
from datetime import datetime
from distutils.command.upload import upload
from itertools import product
from operator import truediv
from pickle import TRUE
from tkinter.tix import Tree
from turtle import tracer
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField 
from accounts.models import * 
from django.forms import BooleanField, ModelForm
from django.db.models import Avg
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50,verbose_name = 'اسم')
    slug = models.SlugField(null=True,blank=True,unique=True,allow_unicode=True,verbose_name = 'شناسه')
    image = models.ImageField(upload_to="category",null=True,blank=True,verbose_name = 'تصویر')

    def __str__(self) :
        return self.name

    def get_absolute_url(self):
        return reverse("home:category",args=[self.slug,self.id])


class Product(models.Model):
   
    category = models.ManyToManyField(Category,blank=True,verbose_name = 'دسته بندی')
    name = models.CharField(max_length=50,verbose_name = 'اسم')
    image = models.ImageField(upload_to ="product",verbose_name = 'تصویر')
    available = models.BooleanField(default=True,verbose_name = 'موجود است؟')
    unit_price = models.PositiveIntegerField(verbose_name = 'قیمت اصلی')
    discount = models.PositiveIntegerField(null=True,blank=True,verbose_name = 'درصد تخفیف')
    total_price = models.PositiveIntegerField(verbose_name = 'قیمت نهایی')
    information = RichTextUploadingField(blank=True,null=True,verbose_name = 'اطلاعات')
    like = models.ManyToManyField(User,related_name="product_like",blank=True)
    total_like = models.IntegerField(default=0,verbose_name = 'مجموع لایک ها')
    unlike = models.ManyToManyField(User,related_name="product_unlike",blank=True)
    total_unlike = models.IntegerField(default=0,verbose_name = 'مجموع آن لایک ها')
    favourite = models.ManyToManyField(User,blank=True,related_name="fa_user",verbose_name = 'علاقه مندی')
    total_favourite = models.PositiveIntegerField(default= 0)
    sell = models.PositiveIntegerField(default= 0)
    view = models.ManyToManyField(User,blank=True,related_name='product_view')
    num_view = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

   ## def average(self):
    #    data = Comment.objects.filter(is_reply = False,product=self).aggregate(avg =Avg('rate'))
    #    star = 0
    #    if data['avg'] is not None:
    #        star = round(data['avg'],1)
    #    return star

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.unit_price* self.discount)/100
            return int(self.unit_price - total)
        return self.total_price


class Gallery(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to = 'gallery/',blank=True)
    text = models.CharField(max_length=500,null=True,blank=True)
    
    def __str__(self) :
        return self.name


class Shahr(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'shahr/',blank=True)
   

    def __str__(self) :
        return self.name


class Shobe(models.Model):
    shahr = models.ForeignKey(Shahr,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'shobe/',blank=True)
    mahsool = models.ManyToManyField(Product,blank=True,related_name='sh')
    address = models.CharField(max_length=500,blank=True)
    phone = models.IntegerField(blank=True)
    start = models.TimeField() 
    end = models.TimeField()

    def __str__(self) :
        return self.name
