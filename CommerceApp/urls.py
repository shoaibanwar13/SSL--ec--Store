"""
URL configuration for shoaibCommerece project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from CommerceApp.views import frontpage, shop, signup,product,add_to_cart,checkout,contact,Thankyou,Reviews,feedback,cart,myaccount,edit_account,hx_menu_cart,update_cart,hx_cart_total,start_order,success,fail
from django.contrib.auth import views

urlpatterns = [
    path('',frontpage,name='frontpage'),
    path('shop/',shop,name='shop'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('product/<str:id>',product,name='product'),
    path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login_old/', views.LoginView.as_view(template_name='login.html'), name='login_old'),
    path('myaccount/', myaccount, name='myaccount'),
    path('edit_account/', edit_account, name='edit_account'),
    path('update_cart/<int:product_id>/<str:action>/', update_cart, name='update_cart'),
    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', hx_cart_total, name='hx_cart_total'),
    path('start_order/', start_order, name='start_order'),
    path('success/', success, name='success'),
    path('fail/', fail, name='fail'),
    path('contact/', contact, name='contact'),
    path('Thankyou/', Thankyou, name='Thankyou'),
    path('Review/', Reviews, name='Reviews'),
    path('feedback/', feedback, name='feedback'),
   
    path("password_reset/", views.PasswordResetView.as_view(template_name='reset_password.html'), name="password_reset"),
    path(
        "password_reset_done/",
        views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(template_name='password_set.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
        name="password_reset_complete",
    ),

    
   
]
