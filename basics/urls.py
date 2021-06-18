from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index,name='home'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('gallery',views.gallery,name='gallery'),
    path('products',views.products,name='products'),
    path('cart',views.cart,name='cart'),
    path('signup',views.signupuser, name='signup'),
    path('login1', views.loginuser, name='login1'),
    path('logout',views.logoutuser,name="logoutuser"),
    path('search',views.searchfield,name="search"),
    path('addtocart',views.addtocart,name="addtocart"),
    path('userdetails',views.userdetails,name="userdetails"),
    path('checkout',views.checkout,name="checkout"),
    path("handlerequest", views.handlerequest, name="HandleRequest"),
    path('delete',views.delete,name="delete"),
    path('searches',views.aftersearch,name="aftersearch"),
    path('yourorders',views.yourorders,name='yourorders'),
   
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
