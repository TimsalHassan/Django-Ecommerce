from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .forms import ProductReviewForm
from .models import Product, Category, Brand
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def search_results(request):
    query = request.GET.get('searched', '').strip()
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(Q(name__icontains=query) |Q(description__icontains=query))
        if not products.exists():
            messages.warning(request,f'No products found for "{query}"')
    total_results = products.count()      
    # Pagination (9 products per page)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': query,
        'page_obj': page_obj,
        'total_results':total_results,
    }
    return render(request, 'search_results.html', context)


def new_arrival(request):
    return render(request, 'new_arrival.html', {})


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

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    similar_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:6]
    
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductReviewForm()
    star_range = range(1, 6)

    return render(request, 'product_detail.html', {'product': product, 'star_range': star_range, 'form': form, 'similar_products': similar_products})



 

