from django.contrib import admin
from .models import ShippingAddress, ShippingAddressFormModel
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(ShippingAddressFormModel)