from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

# class Order(models.Model):
#     # Foreign Key
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     shipping_address = models.TextField(max_length=15000)
#     amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
#     date_ordered = models.DateTimeField(auto_now_add=True)  

#     def __str__(self):
#         return f'Order - {str(self.id)}'   

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {str(self.id)}' 
 
    
class OrderItem(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'