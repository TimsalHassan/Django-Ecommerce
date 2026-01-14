from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Category, Brand

# Create your views here.

def category_product(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_product.html', {'products': products, 'category': category})


def category_summary(request):
    return render(request, 'category_summary.html', {})

# def brand_category(request, slug):
#     brand = get_object_or_404(Brand, slug=slug)
#     products = Product.objects.filter(brand=brand, logo__isnull=False)[:7]
#     return render(request, 'brand_category.html', {'products': products, 'brand': brand})

def brand_product(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True)
    return render(request, 'brand_product.html', {'brand': brand,'products': products})

    
def product(request):
    return render(request, 'product.html')

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product_detail.html', {'product': product})

