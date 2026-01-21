from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingAddressForm
from payments.models import ShippingAddressFormModel

# Create your views here.

def checkout_info(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    quantities = cart.get_quantities()
    totals = cart.cart_totals()
    if request.user.is_authenticated:
        #Check Out as Logged in user
        shipping_user = ShippingAddressFormModel.objects.get(user__id = request.user.id)
        # Shipping Form
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout_info.html', {"cart_items":cart_items, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # Cheak Out as Guest
        
        shipping_form = ShippingAddressForm(request.POST or None)
        return render(request, 'checkout_info.html', {"cart_items":cart_items, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

def manage_orders(request):
    return render(request, 'manage_orders.html')