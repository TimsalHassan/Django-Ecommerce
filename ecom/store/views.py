from django.shortcuts import get_object_or_404, render
from products.models import Product, Category, Brand
from django.views.generic import TemplateView
# Create your views here.
# def home(request):
#     trending_products = Product.objects.filter(is_trending=True)[:6]
#     featured_products = Product.objects.filter(is_featured=True)[:3]
#     promotional_products = Product.objects.filter(is_promotional=True)

#     return render(request, 'index.html', {
#         'trending_products': trending_products,
#         'featured_products': featured_products,
#         'promotional_products': promotional_products
#     })
def home(request):
    # First active category
    category = Category.objects.filter(is_active=True).first()
    if category:
        category_products = category.products.filter(is_active=True)[:6]
    else:
        category_products = Product.objects.none()  # empty queryset if no category

    # Mobile phones category products
    mobile_category = Category.objects.filter(slug='mobile-phones', is_active=True).first()
    if mobile_category:
        mobile_products = mobile_category.products.filter(is_active=True)[:6]
        mobile_brands = Brand.objects.filter(
            products__category=mobile_category,
            is_active=True
        ).distinct()
    else:
        mobile_products = Product.objects.none()
        mobile_brands = Brand.objects.none()

    # Tablets category products
    tablet_category = Category.objects.filter(slug='tablets', is_active=True).first()

    if tablet_category:
        tablet_products = tablet_category.products.filter(is_active=True)[:6]
        tablet_brands = Brand.objects.filter(
            products__category=tablet_category,
            is_active=True
        ).distinct()
    else:
        tablet_products = Product.objects.none()
        tablet_brands = Brand.objects.none()

    # Trending products (first 6)
    trending_products = Product.objects.filter(is_trending=True, is_active=True)[:6]
    # Featured products (first 3)
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:3]
    # Promotional products (all active)
    promotional_products = Product.objects.filter(is_promotional=True, is_active=True)

    return render(request, 'index.html', {
        
        'category_products': category_products,
        'trending_products': trending_products,
        'featured_products': featured_products,
        'promotional_products': promotional_products,
        'mobile_category': mobile_category,
        'mobile_products': mobile_products,
        'mobile_brands': mobile_brands,
        'tablet_category': tablet_category,
        'tablet_products': tablet_products,
        'tablet_brands': tablet_brands,
    })


def category_list(request):
    return render(request, 'category_list.html')

def index_inverse(request):
    return render(request, 'index_inverse_header.html',{})

def about_us(request):
    return render(request, 'about_us.html')

# def faq(request):
#     return render(request, 'faq.html')
class FAQView(TemplateView):
    template_name = 'faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'FAQ'
        return context
    
class ContactUsView(TemplateView):
    template_name = 'contact_us.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ContactUs'
        return context

class AboutUsView(TemplateView):
    template_name = 'about_us.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'AboutUs'
        return context

# def contact_us(request):
#     return render(request, 'contact_us.html')

# def search_results(request):
#     return render(request, 'search_results.html')

def my_account(request):
    return render(request, 'my_account.html')
    