from django.urls import path
from . import views 


urlpatterns = [
    path('product/', views.product, name='product'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('brand_summary/', views.brand_summary, name='brand_summary'),
    path('category_product/<slug:slug>/', views.category_product, name='category_product'),
    path('brand_product/<slug:slug>/', views.brand_product, name='brand_product'),
]