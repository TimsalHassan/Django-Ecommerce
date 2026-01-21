from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Brand (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    logo = models.ImageField(upload_to='uploads/brands/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_product', kwargs={'slug': self.slug})
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    category_img = models.ImageField(upload_to='uploads/categories/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category_product', kwargs={'slug': self.slug})

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)  # short description
    price = models.DecimalField(max_digits=6, default=0, decimal_places=2)
    
    # Optional product properties
    color = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=20, blank=True, null=True)

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

    warranty_years = models.PositiveIntegerField(default=0)
    warranty_info = models.CharField(max_length=200, blank=True, null=True)  # e.g., Local Manufacturer Warranty

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class ProductDescription(models.Model):
    product = models.ForeignKey('Product', related_name='descriptions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # e.g., "3D Touch"
    desc = models.TextField()           # e.g., description text
    image = models.ImageField(upload_to='uploads/product_descriptions/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.title}"

class ProductAdditionalInfo(models.Model):
    product = models.ForeignKey('Product', related_name='additional_info', on_delete=models.CASCADE)
    field = models.CharField(max_length=100)  # e.g., "Display"
    value = models.TextField()                # e.g., "Retina HD display with 3D Touch"

    def __str__(self):
        return f"{self.product.name} - {self.field}"

class ProductReview(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)       # Reviewer Name
    title = models.CharField(max_length=200)      # Review Title
    message = models.TextField()                  # Review Body
    rating = models.PositiveSmallIntegerField(default=0)       # 1-5 rating
    created_at = models.DateTimeField(auto_now_add=True)

    def avatar_url(self):
        if self.user and hasattr(self.user, 'profile') and self.user.profile.avatar:
            return self.user.profile.avatar.url
        # fallback image
        return "/static/img/user-1.png"

    def __str__(self):
        return f"{self.product.name} - {self.title} ({self.rating}/5)"
