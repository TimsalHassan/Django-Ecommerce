from .models import Category, Brand

def categories_processor(request):
    categories = Category.objects.filter(is_active=True)
    return {'categories': categories}

def brand_category_processor(request):
    brands = Brand.objects.filter(is_active=True)
    return {'brands': brands}