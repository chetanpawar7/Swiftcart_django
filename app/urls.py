"""
URL configuration for Swiftcart project.

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
from .import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.index,name='index'),
    path('store/',views.store,name='store'),
    path('mobile/',views.mobile,name='mobile'),
    path('electronics/',views.electronics,name='electronics'),
    path('fashion/',views.fashion,name='fashion'),
    path('appliance/',views.appliance,name='appliance'),
    path('about/',views.about,name='about'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('orders/',views.orders,name='orders'),
    path('customerlogin/',views.customerlogin,name='customerlogin'),
    path('customersignup/',views.customersignup,name='customersignup'),
    path('logout_view/',views.logout_view,name='logout_view'), 
    path('cart/',views.cart,name='cart'), 
    path('add_to_cart/<int:product_id>/', views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart,name='remove_from_cart'),
    
    # path('search_view/',views.search_view,name='search_view'), 
    path('search_prod/',views.search_prod,name='search_prod'), 
    path('checkout/',views.checkout,name='checkout'),
    path('payment_success/',views.payment_success,name='payment_success'),
    
]
