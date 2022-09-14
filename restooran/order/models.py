from tabnanny import verbose
from home.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_jalali.db import models as jmodels
 
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = 'کاربر')
    email = models.EmailField(verbose_name = 'ایمیل')
    create = jmodels.jDateTimeField(auto_now_add=True,verbose_name = 'زمان ایجاد')
    discount = models.PositiveIntegerField(blank=True,null=True,verbose_name = 'درصد تخفیف')
    paid = models.BooleanField(default=False,verbose_name = 'آیا پرداخت شده است؟')
    f_name = models.CharField(max_length=50,verbose_name = 'نام')
    l_name = models.CharField(max_length=50,verbose_name = 'نام خانوادگی')
    address = models.CharField(max_length=500,verbose_name = 'آدرس')
    code = models.CharField(max_length=200,null=True)
    ersal = models.ForeignKey('ErsalOrder',on_delete=models.CASCADE,null=True,blank=True)
    information = models.TextField(null=True,blank=True,max_length=1000)

    class Meta:
        verbose_name = 'فرم سفارش'
        verbose_name_plural = 'فرم های سفارش'

    def __str__(self):
        return self.user.username 
    
    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price =(self.discount/100) * total
            return int(total - discount_price)
        return total

class ItemOrder(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_item",verbose_name = 'سفارش')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = 'کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = 'محصول')
    quantity = models.IntegerField(verbose_name = 'مقدار')
    

    class Meta:
        verbose_name = 'جزئیات سفارش'
        verbose_name_plural = 'جزئیات سفارشات'

    def __str__(self) :
        return self.user.username

   
    def price(self):
        return self.product.total_price * self.quantity

class ErsalOrder(models.Model):
    ersal = models.CharField(max_length=300)
    hazine = models.IntegerField(default=0)

    def __str__(self):
        return self.ersal

class OrderForm(ModelForm):
    ersal = forms.ModelChoiceField(queryset=ErsalOrder.objects.all())
    class Meta:
        model = Order 
        fields = ['email','f_name','l_name',"address",'information']
        
