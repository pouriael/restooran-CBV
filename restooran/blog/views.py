from multiprocessing import context
from django.shortcuts import redirect, render ,get_object_or_404
from .models import *
from home.models import *
from django.views.generic import TemplateView

class blog(TemplateView):
    template_name = 'blog/blog.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.all()
        return context


class detail(TemplateView):
    template_name = 'blog/detail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog,id = kwargs['id'])
        context['blog_all'] = Blog.objects.all()
        context['create'] = Blog.objects.all().order_by('-create')[:5]
        context['bazdid'] = sorted(context['blog_all'],key= lambda t: t.total_asli(),reverse=True)
        context['similar'] = context['blog'].tags.similar_objects()
        context['tag'] = Blog.tags.all()
        if self.request.user.is_authenticated:
            context['blog'].views.add(self.request.user)
        else:
            context['blog'].total += 1
            context['blog'].save()
        context['views'] = context['blog'].total_asli()
        return context

class dastebandi(TemplateView):
    template_name = 'blog/dastebandi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Blog.tags.get(id =kwargs['id'])
        context['blog'] = Blog.objects.filter(tags = context['tag'])
        return context

