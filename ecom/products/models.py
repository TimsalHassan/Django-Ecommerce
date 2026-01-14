from django.db import models
from django.urls import reverse

# Create your models here.
class Brand (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    logo = models.ImageField(upload_to='uploads/brands/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    category_img = models.ImageField(upload_to='uploads/categories/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, default=0, decimal_places=2)

    slider_image = models.ImageField(upload_to='uploads/slider/', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    stock = models.PositiveIntegerField(default=0)

    is_discounted = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=2, default=0, decimal_places=0)  # percentage discount
    discount_price = models.DecimalField(max_digits=6, default=0, decimal_places=2)

    is_active = models.BooleanField(default=True)
    is_promotional = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    THEME_CHOICES = [
        ('bg-black-darker', 'Black Darker'),
        ('bg-blue', 'Blue'),
        ('bg-silver', 'Silver'),
        ('bg-black', 'Black'),
    ]
    promotion_theme = models.CharField(max_length=50, blank=True, null=True, choices=THEME_CHOICES)
    promotion_size = models.CharField(max_length=20, default='regular', choices=[('large', 'Large'), ('regular', 'Regular')])

    warranty_years = models.PositiveIntegerField(default=0)  # 1, 2, 3 years
    warranty_info = models.CharField(max_length=200, blank=True, null=True)  # "Local Manufacturer Warranty"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

