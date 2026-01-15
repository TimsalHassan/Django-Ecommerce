from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Category, Brand
from django.core.paginator import Paginator

# Create your views here.

def category_product(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_product.html', {'products': products, 'category': category})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})

def brand_summary(request):
    brands = Brand.objects.all()
    return render(request, 'brand_summary.html', {"brands":brands})

# def brand_category(request, slug):
#     brand = get_object_or_404(Brand, slug=slug)
#     products = Product.objects.filter(brand=brand, logo__isnull=False)[:7]
#     return render(request, 'brand_category.html', {'products': products, 'brand': brand})

def brand_product(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True)
    return render(request, 'brand_product.html', {'brand': brand,'products': products})

    
def product(request):
    product_list = Product.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(product_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': page_obj,     
        'page_obj': page_obj
    }
    return render(request, 'product.html', context)

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product_detail.html', {'product': product})

