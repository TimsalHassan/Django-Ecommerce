from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields= ['created_at']
    fields = ['user', 'full_name', 'email', 'shipping_address', 'amount_paid', 'created_at', 'transaction_id']
    inlines = [OrderItemInline]

# Un-register the original Order
admin.site.unregister(Order)
# Re-register Order Model
admin.site.register(Order, OrderAdmin)