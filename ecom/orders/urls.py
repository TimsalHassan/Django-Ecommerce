from django.urls import path
from . import views 

urlpatterns = [
    path('checkout_info/', views.checkout_info, name='checkout_info'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
]