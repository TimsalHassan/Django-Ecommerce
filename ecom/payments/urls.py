from django.urls import path
from . import views 

urlpatterns = [
    path('checkout_payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout_complete/', views.checkout_complete, name='checkout_complete'),
]