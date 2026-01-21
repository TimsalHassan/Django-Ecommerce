from django.urls import path
from . import views 

urlpatterns = [
    path('checkout_payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout_complete/', views.checkout_complete, name='checkout_complete'),
    path('checkout/', views.create_checkout_session, name='stripe_checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
