
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render ,get_object_or_404
from .models import *
from django.contrib import messages
from accounts.models import *
from .forms import *
from django.db.models import Q,Max,Min,Sum
from cart.models import *
from django.core.paginator import Paginator
from urllib.parse import urlencode
from blog.models import *
from django.views.generic import TemplateView ,FormView
from django.views import View

class home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['gallery'] = Gallery.objects.all()
        context['create_b'] = Blog.objects.all().order_by('-create')[:5]
        context['shahr'] = Shahr.objects.all()
        return context

class shobe(TemplateView):
    template_name = 'home/shobe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shobe'] = Shobe.objects.filter(shahr_id = kwargs['id'])
        return context

class product_shobe(TemplateView):
    template_name = 'home/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shobe'] = Shobe.objects.get(id = kwargs['id'])
        context['cart'] = Cart.objects.filter(user_id = self.request.user.id)
        context['products'] = context['shobe'].mahsool.all()
        return context
    
def product(request,slug=None,id=None):
    cart = Cart.objects.filter(user_id = request.user.id)
    products= Product.objects.all()
    page_obj = products
    category = Category.objects.all()
    data = request.GET.copy()
    if slug and id:
        data = get_object_or_404(Category,slug =slug,id=id)
        page_obj = products.filter(category = data)
        data = request.GET.copy()
    form  = SearchForm()
    if 'search' in request.GET:
        form  = SearchForm(request.GET)
        if form.is_valid():
            info = form.cleaned_data['search']
            page_obj = products.filter(Q(name__contains = info))
            data = request.GET.copy()
    context ={"products":page_obj,"category":category,'cart':cart}

    return render(request,"home/product.html",context)

class contact(TemplateView):
    template_name = 'home/contact.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context
    
    def post(self,request):
        category = Category.objects.all()
        subject = self.request.POST['subject']
        email = self.request.POST['email']
        msg = self.request.POST['message']
        body = subject + '\n' + email + '\n' + msg
        form = EmailMessage(
            'contact form', 
            body,
            'test',
            ('pouriael2002@gmail.com',),
        )
        form.send(fail_silently = False)
        return render(request,'home/contact.html',context={'category':category})


class aboutus(TemplateView):
    template_name = 'home/aboutus.html'



class product_search(FormView):
    form_class = SearchForm
    success_url = 'home/product.html'

    def form_valid(self,form):
        self._search_filter(form.cleaned_data)
        return super().form_valid(form)

    def _search_filter(self,data):
        form = SearchForm(self.request.POST)
        products = Product.objects.all()
        if data.isdigit():
            products = products.filter(Q(discount__exact = data)| Q(unit_price__exact = data))
        else:
            products = products.filter(Q(name__contains = data))
        return render(self.request,"home/product.html",{"products":products,'form':form})

