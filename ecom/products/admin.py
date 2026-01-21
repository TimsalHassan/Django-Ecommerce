from django.contrib import admin
from .models import Category, Brand, Product, ProductDescription, ProductFeature, ProductAdditionalInfo, ProductReview

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductFeature)
admin.site.register(ProductDescription)
admin.site.register(ProductReview)
admin.site.register(ProductAdditionalInfo)