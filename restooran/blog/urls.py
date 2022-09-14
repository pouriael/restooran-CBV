from django.urls import path 
from . import views

app_name= "blog"
urlpatterns = [

    path("",views.blog.as_view(),name="blog"),
    path('detail/<int:id>',views.detail.as_view(),name='detail'),
    path('dastebandi/<int:id>',views.dastebandi.as_view(),name='dastebandi'),
   
]
