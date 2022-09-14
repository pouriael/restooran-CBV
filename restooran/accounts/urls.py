from django.urls import path 
from . import views
from django.contrib.auth.decorators import login_required
app_name= "accounts"
urlpatterns = [
    path('',views.accounts.as_view(),name="accounts"),
    path("register/",views.user_register.as_view(),name="register"),
    path('kifpool/',views.kifpool,name='kifpool'),
    path("login/",views.user_login.as_view() ,name="login"),
    path("logout/",views.user_logout,name="logout" ),
    path("profile/",login_required(views.user_profile.as_view()),name="profile"),
    path("update/",views.user_update,name = "update"),
    path("change_password/",views.user_change_password,name= "change_password"),
    path("login_phone/",views.user_login_phone.as_view(),name="login_phone"),
    path("verify/",views.verify.as_view(),name= "verify"),
    path("active/<uidb64>/<token>/",views.RegisterEmial.as_view(),name='active'),
    path("reset/",views.ResetPassword.as_view(),name='reset'),
    path("reset/done/",views.DonePassword.as_view(),name='reset_done'),
    path("confirm/<uidb64>/<token>/",views.ConfirmPassword.as_view(),name='password_reset_confirm'),
    path("confirm/done/",views.Complete.as_view(),name='complete'),
    path('favourite/',views.favourite.as_view(),name='favourite'),
    path('address/',views.address.as_view(),name='address'),
    path('coupon/<int:id>',login_required(views.coupon.as_view()),name='coupon')
    #path('history/',views.history,name='history'),
    #path('view/',views.product_view,name='product_view'),
    

]