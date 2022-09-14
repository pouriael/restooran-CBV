
from urllib import response
from django.shortcuts import redirect, render,reverse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from random import randint
import ghasedakpack
from django.db.models import Q,Max,Min,Sum
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_bytes ,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView,FormView
from order.models import *
from cart.models import *

from django.views import View

class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

email_generator = EmailToken()

class accounts(View):
    http_method_names = ['get','options']

    def get(self,request):
        return render(request,'home/home.html')

    def options(self,request,*args,**kwargs): 
        response = super().options(request,*args,**kwargs)
        response.headers['host'] = 'local host'
        response.headers['user'] = request.user
        return response

    def http_method_not_allowed(self, request, *args, **kwargs):
        super().http_method_not_allowed(request,*args,**kwargs)
        return render(request,"accounts/not_method.html")

class user_register(FormView):
    form_class = UserregisterForm
    template_name ='accounts/register.html' 

    def get_success_url(self,) :
        return reverse('home:home')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['form'] = UserregisterForm()
        return context

    def form_valid(self,form):
        self._user_register(form.cleaned_data)
        return super().form_valid(form)

    def _user_register(self,data):
        user = User.objects.create_user(username=data['user_name'], email=data['email'],first_name=data['first_name'],
                                    last_name=data['last_name'],password=data['password_2'])
        user.is_active = False
        user.save()
        domain = get_current_site(self.request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.id)) 
        url  = reverse('accounts:active',kwargs ={'uidb64':uidb64,'token':email_generator.make_token(user)})
        link = 'http://'+domain+ url
        email = EmailMessage(
            'active user',
            link,
            'test<pouriael2002@gmail.com>',
            [data["email"]]
        )
        email.send(fail_silently=False)
        messages.warning(self.request,"please wait for activate ...",'warning')
        return redirect("home:home")

class address(FormView):
    form_class = Address
    template_name ='accounts/address.html' 

    def get_success_url(self,) :
        return reverse('home:home')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['form'] = Address()
        return context

    def form_valid(self,form):
        self._user_register(form.cleaned_data)
        return super().form_valid(form)


def kifpool(request):
    if request.method == "POST":
        return render(request,'order/kifpool.html')
    else:
        form = KifPoolForm()
        context = {'form':form}
        return render(request,'accounts/kifpool.html',context)

class user_login(FormView):
    form_class = UserloginForm
    template_name ='accounts/login.html' 

    def get_success_url(self,) :
        if self.request.user.is_authenticated:
            return reverse('home:home')
        else:
            return reverse('accounts:login')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['form'] = UserloginForm()
        return context

    def form_valid(self,form):
        self._user_login(form.cleaned_data)
        return super().form_valid(form)

    def _user_login(self,data):
        remember = data['remember']
        try:
            user = authenticate(self.request,username =User.objects.get(email=data["user"]), password = data['password'])
        except:
            user = authenticate(self.request,username=data['user'], password = data['password'])
        if user is not None:
            login(self.request,user)
            if not remember:
                self.request.session.set_expiry(0)
            else:
                self.request.session.set_expiry(172800)
            messages.success(self.request,"welcome to my website",'success')
            return redirect("home:home")
        else:
            messages.error(self.request,"your login has error","danger")
            return redirect("accounts:login")


def user_logout(request):
    logout(request)
    messages.success(request,"success logout","success")
    return redirect("home:home")

class RegisterEmial(View):
    def get(self,request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
        return redirect('accounts:login')

class user_profile(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['Profile'] = formprofile.objects.get(user_id = self.request.user.id)
        return context

class coupon(TemplateView):
    template_name = 'accounts/coupon.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['coupon'] = CouponProfile.objects.filter(dastresi__id = kwargs['id'])
        return context

@login_required(login_url="accounts:login")
def user_update(request):
    #nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    Profile = formprofile.objects.get(user_id = request.user.id)
    #if request.user.is_authenticated:
    #    compare = Compare.objects.filter(user_id = request.user.id)
    #    
    #else:
    #    compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
    #category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        user_form = User_updateform(request.POST,instance=request.user)
        profile_form = Profile_updateform(request.POST,request.FILES,instance=request.user.formprofile)
        if profile_form and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"update completed","success")
            return redirect("accounts:profile")
    else:
        user_form = User_updateform(instance=request.user)
        profile_form = Profile_updateform(instance = request.user.formprofile)
    context = {"user_form":user_form,"profile_form":profile_form,'Profile':Profile}
    return render (request,"accounts/update.html",context)


def user_change_password(request):
    nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    category = Category.objects.all()
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,"password changed","success")
        else:
            messages.error(request,"password is not changed","danger")
    else:
        form  = PasswordChangeForm(request.user)
    context = {"form":form,'nums':nums,'category':category}
    return render(request,"accounts/change.html",context)


class user_login_phone(FormView):
    form_class = PhoneForm
    template_name ='accounts/login_phone.html' 

    def get_success_url(self,) :
        return reverse('accounts:verify')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['form'] = PhoneForm()
        return context

    def form_valid(self,form):
        self._login_phone(form.cleaned_data)
        return super().form_valid(form)

    def _login_phone(self,data):
        global random_code,phone
        phone =data["phone"]
        random_code = randint(100,1000)
        sms = ghasedakpack.Ghasedak("Your APIKEY")
        sms.send({'message':random_code, 'receptor' : phone, 'linenumber': '3000xxxxx' })
        return redirect("accounts:verify")


class verify(FormView):
    form_class = CodeForm
    template_name ='accounts/code.html' 

    def get_success_url(self,) :
        return reverse('accounts:verify')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['form'] = CodeForm()
        return context

    def form_valid(self,form):
        self._verify_code(form.cleaned_data)
        return super().form_valid(form)

    def _verify_code(self,data):
        if random_code == data["code"]:
            profile = formprofile.objects.get(phone = phone)
            user = User.objects.get(profile_id = profile.id)
            login(self.request,user)
            messages.success(self.request,f"welcome {user}","success")
        else:
            messages.error(self.request,"your code is wrong",'danger')

class favourite(TemplateView):
    template_name = 'accounts/favourite.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nums'] = Cart.objects.filter(user_id =self.request.user.id ).aggregate(sum=Sum('quantity'))['sum']
        context['category'] = Category.objects.all()
        context['product'] = self.request.user.fa_user.all()
        return context

#def history(request):
    #nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    #category = Category.objects.filter(sub_cat = False)
    #data = ItemOrder.objects.filter(user_id = request.user.id)
    #return render(request,'accounts/history.html',{'data':data,'category':category,'compare':compare,'nums':nums})

#def product_view(request):
    #nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    #
    #category = Category.objects.filter(sub_cat = False)
    #product = Product.objects.filter(view = request.user.id)
    #return render(request,'accounts/view.html',{'product':product,'category':category,'compare':compare,'nums':nums})
    
class ResetPassword(auth_views.PasswordResetView):
    template_name = "accounts/reset.html"
    success_url = reverse_lazy("accounts:reset_done")
    email_template_name = "accounts/link.html"

class DonePassword(auth_views.PasswordResetDoneView):
    template_name = "accounts/done.html"

class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = "accounts/confirm.html"
    success_url = reverse_lazy("accounts:complete")

class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'

