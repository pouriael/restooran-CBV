from django.shortcuts import get_object_or_404, redirect, render
from requests import session
from home.models import *
from .models import *
from django.contrib import messages
#from order.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import *
from django.contrib.auth.models import User

from django.views.generic import RedirectView,TemplateView
from django.views import View

class add_cart(View):

    @method_decorator(login_required)
    def post(self, request,*args, **kwargs):
        product = Product.objects.get(id=kwargs['id'])
        data = Cart.objects.filter(user_id = request.user.id,product_id=kwargs['id'])
        if data:
            check = 'yes'
        else: 
            check = 'no'
            form = CartForm(request.POST)
            var_id = request.POST.get('select')
            if form.is_valid():
                info = form.cleaned_data['quantity'] 
                if check == 'yes':
                    shop = Cart.objects.get(product_id = kwargs['id'],user_id =request.user.id)
                    messages.success(request,"product add to basketshop","success")
                    shop.quantity +=info
                    shop.save()
                else:
                    Cart.objects.create(user_id=request.user.id,product_id=kwargs['id'],quantity = info)
            return redirect('home:product')


@login_required(login_url="accounts:login")
def del_cart(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    
    data = Cart.objects.filter(user_id = request.user.id,product_id=id)
    if data:
        check = 'yes'
    else:
        check = 'no'
    if request.method == 'POST':
        form = CartDelForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity'] 
            if check == 'yes':
                    shop = Cart.objects.get(product_id = id,user_id =request.user.id)
                    messages.success(request,"product delete at basketshop","success")
                    shop.quantity -=info
                    shop.save()
            else:
                Cart.objects.create(user_id=request.user.id,product_id=id,quantity = info)
        return redirect(url)

class cart_detail(TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['Profile'] =  formprofile.objects.get(user_id = self.request.user.id)
        context['category'] = Category.objects.all()
        context['cart'] = Cart.objects.filter(user_id = self.request.user.id)
        total = 0
        user = self.request.user
        for p in context['cart']:
            if p.quantity<1:
                p.delete()
            total += p.quantity * p.product.total_price 
        context['total'] = total
        context['user'] = user
        return context 

def remove_cart(request,id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.get(id = id).delete()
    return redirect(url)

def remove_single(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get( id = id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)

def add_single(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id = id )
    cart.quantity +=1
    cart.save()
    return redirect(url)