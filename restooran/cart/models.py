from dataclasses import field
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from home.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = 'کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = 'محصول',)
    quantity = models.PositiveIntegerField(verbose_name = 'مقدار')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self) :
        return self.user.username

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class CartDelForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']