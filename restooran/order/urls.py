from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "order"

urlpatterns = [
    path('etelaat/',views.etelaat.as_view(),name='etelaat'),
    path('<int:order_id>',views.order_detail.as_view(),name='order_detail'),
    path('create/',views.order_create.as_view(),name="order_create"),
    path('coupon/<int:order_id>/',login_required(views.coupon_order.as_view()),name='coupon'),
    path('request/<int:order_id>/<int:price>/',views.send_request,name='request'),
    path('verify/',views.verify,name='verify'),
]