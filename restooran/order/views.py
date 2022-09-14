
from math import prod
from django.shortcuts import redirect, render
from cart.models import *
from  order.models import *
from .forms import *
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from accounts.models import *
import requests
from django.db.models import Q,Max,Min,Sum
import json
from django.http import HttpResponse
import jdatetime
from django.utils.crypto import get_random_string
import ghasedakpack
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse,reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class etelaat(TemplateView):
    template_name = 'order/etelaat.html'

    def get_context_data(self, **kwargs):
        form = OrderForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

class order_detail(TemplateView):
    template_name = 'order/order.html'   

    def get_context_data(self, **kwargs)     :
        context = super().get_context_data(**kwargs)
        context['form'] = CouponForm()
        context['category'] = Category.objects.all()
        context['order'] = Order.objects.get(id = self.kwargs['order_id'])
        context['nums'] = Cart.objects.filter(user_id = self.request.user.id).aggregate(sum =Sum('quantity'))['sum']
        return context

class order_create(FormView):
    form_class = OrderForm

    
    def form_valid(self,form):
        self._create_order(form.cleaned_data)
        return super().form_valid(form)

    def _create_order(self,data):
        global x
        
        code = get_random_string(length=8)
        order = Order.objects.create(user_id = self.request.user.id,l_name = data['l_name'],email = data['email'],f_name = data['f_name'],
                                    address= data['address'],code = code,ersal=data['ersal'],information = data['information']  )
        cart = Cart.objects.filter(user_id = self.request.user.id)
        x = order.id
        for c in cart:
            ItemOrder.objects.create(order_id= order.id,user_id = self.request.user.id,product_id=c.product_id, quantity = c.quantity)
        return redirect('order:order_detail',order.id)
    
    def get_success_url(self):
        return reverse_lazy('order:order_detail',kwargs={'order_id':x})


class coupon_order(FormView):
    form_class = CouponForm
    
    
    def get_success_url(self,) :
        return reverse('order:order_detail',kwargs={'order_id':self.kwargs['order_id']})

    def form_valid(self,form):
        self._check_coupon(form.cleaned_data)
        return super().form_valid(form)

    def _check_coupon(self,data):
        time = jdatetime.datetime.now()
        try:
            coupon = CouponProfile.objects.get(code__iexact = data['code'],start__lte = time,end__gte = time,active=True)  
            messages.success(self.request,'coupon is success','success')
        except:
            messages.error(self.request,'code wrong','danger')
            return redirect("order:order_detail",self.kwargs['order_id'])
        order = Order.objects.get(id = self.kwargs['order_id'])
        order.discount = coupon.discount
        order.save()
        return redirect('order:order_detail',self.kwargs['order_id'])

# baad az etesal dargah baayd biay tanzim koni #####################################################################################

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/order:verify/'


def send_request(request,order_id,price):
    global amount
    amount = price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": request.user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request,order_id):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order = Order.objects.get(id = order_id)
                order.paid =True
                order.save()
                cart = ItemOrder.objects.filter(order_id = order_id)
                for c in cart:
                        product = Product.objects.get(id = c.product.id)
                        product.sell += c.quantity
                        product.save()
                        phone = f"0{request.user.profile.phone}"
                        code = order.code
                        sms = ghasedakpack.Ghasedak("Your APIKEY")
                        sms.send({'message':code, 'receptor' : phone, 'linenumber': '3000xxxxx' })
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')

##############################################################################################################################################

#if c.product.status == 'None':
#                        product = Product.objects.get(id = c.product.id)
#                        product.amount -= c.quantity
#                        product.save()
#                    else:
#                        variant = Variantproduct.objects.get(id = c.variant.id)
#                        variant.amount -= c.quantity
#                        variant.save()