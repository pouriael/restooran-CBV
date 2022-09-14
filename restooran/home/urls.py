from django.urls import path
from . import views

app_name = "home"

urlpatterns=[
    path('',views.home.as_view(), name="home"),
    path('product/',views.product,name= "product"),
    path('product_shobe/<int:id>',views.product_shobe.as_view(),name= "product_shobe"),
    path('shobe/<int:id>',views.shobe.as_view(),name= "shobe"),
    path("category/<slug>/<int:id>/",views.product,name= "category"),
    #path('like/<int:id>/',views.product_like,name="product_like"),
    #path('unlike/<int:id>/',views.product_unlike,name="product_unlike"),
    #path('comment/<int:id>/',views.product_comment,name="product_comment"),
    #path('reply/<int:id>/<int:comment_id>/',views.product_reply,name="product_reply"),
    #path('comment_like/<int:id>',views.comment_like,name="comment_like"),
    path('search/',views.product_search.as_view(),name='product_search'),
    #path('favourite/<int:id>',views.favourite_product,name='favourite'),
    path('contact/',views.contact.as_view(),name='contact'),
    path('aboutus/',views.aboutus.as_view(),name='aboutus'),
    
]


