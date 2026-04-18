"""
URL configuration for sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from sampleapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', admin.site.urls),
path('', views.index),
path('', views.index, name='collection'),
path('register/', views.users),
path('login/', views.login, name='login'),
path('adminhome/', views.adminhome),
path('userhome/', views.user),
path('Add_Product/', views.Add_Product),
path('cart/<int:d>', views.add_cart),
path('viewcart/', views.view_cart, name='viewcart'),
path('forms', views.normalform),
path('adminhome', views.adminhome),
path('logout', views.logout),
    
path('category', views.category, name='category'),
path('Manage_Product', views.Manage_Product),
path('delete/<int:d>', views.delete),
path('update/<int:d>', views.update),
path('delivery_boy_login', views.delivery_login, name='delivery_login'),
path('Sub_category', views.sub_category, name='sub_category'),
path('viewcart/increment/<int:d>/', views.increment, name='increment'),
path('viewcart/decrement/<int:d>/', views.decrement, name='decrement'),
path('order_summary/payment/<int:d>', views.payment, name='payment'),
path('payment/<int:d>', views.payment, name='payment'),
path('address/', views.address),
path('order_summary', views.order_sum),
path('success', views.order),
path('myorders', views.myorder),
path('rem/<int:d>/',views.rem),
path('wishlist/remo/<int:d>/', views.remo, name='remove_wishlist'),
path('wishlist/add/<int:d>/', views.wish, name='add_wishlist'),
path('wishlist/', views.wish_view, name='wishlist_view'),
    path('alert', views.alert),

path('booking', views.booking),
path('delivery_boy_register', views.delivery_reg),

path('delivery_home', views.delivery_home),
path('delivery_views',views.delivery_view),
path('reject/<int:a>',views.reject),
path('accept/<int:a>',views.accept),
path('choose/<int:a>',views.choose),
path('delivery_order',views.delivery_order),
path('product/', views.products, name='all_products'),
path('products/category/<int:category_id>/', views.products, name='category_products'),
path('products/product_detail/<int:pk>/', views.product_detail, name='product_detail'),
path('products/subcategory/<int:sub_id>/', views.products_by_sub, name='subcategory_products'),
path('sub_sub_category/<int:d>/', views.sub_sub_category, name='sub_sub_category'),
path('product/subsub/<int:d>/', views.product_by_subsub, name='product_by_subsub'),

path('products/subcategory/cart/<int:d>/', views.add_cart),
path('product/subsub/cart/<int:d>/', views.add_cart),
path('products/category/cart/<int:d>/', views.add_cart),
path('search/', views.search, name='search'),
path('order_history',views.history),
path('profile',views.profile),
path('delivery_orders',views.delivery_order),
path('forgot/', views.forgot_password, name='forgot_password'),
    path('delivered/<int:a>',views.delivered),
path('reset/<str:token>/', views.reset_password, name='reset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
