from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),      
    path('order_details/', views.order_details, name='order_details'),  
    path('order_info/', views.order_info, name='order_info'),
]
