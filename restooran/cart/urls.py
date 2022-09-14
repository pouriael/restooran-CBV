from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('',views.cart_detail.as_view(),name ='cart_detail'),
    path('add/<int:id>/',views.add_cart.as_view(),name="add_cart"),
    path('del/<int:id>/',views.del_cart,name="del_cart"),
    path('remove/<int:id>/',views.remove_cart,name="remove_cart"),
    path('remove_single/<int:id>/',views.remove_single,name="remove_single"),
    path('add_single/<int:id>/',views.add_single,name="add_single"),
    #path('compare/<int:id>/',views.compare,name="compare"),
    #path('compare_remove/<int:id>/',views.compare_remove,name='compare_remove'),
    #path('show/',views.show,name="show"),
    #path('compare_filter/',views.compare_filter,name='compare_filter')
]