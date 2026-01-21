from django.shortcuts import render, get_object_or_404
from .cart import Cart
from products.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_items()
    quantities = cart.get_quantities()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, "quantities":quantities, "totals":totals})

def checkout_cart(request):
    cart = Cart(request)
    totals = cart.cart_totals()
    context = {
        'cart_items': cart.get_items(),
        'quantities': cart.get_quantities(),
        'totals': totals
    }
    if request.user.is_authenticated:
        #Check Out as Logged in user
        return render(request, 'checkout_cart.html', context)
    else:
        # Cheak Out as Guest
        return render(request, 'checkout_cart.html', context)


def cart_add(request):
    # Get the Cart
    cart = Cart(request)
    # Test for post
    if request.POST.get('action') == 'post':
        # Get the product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Lookup the product in the DB
        product = get_object_or_404(Product, id=product_id)
        # Add to cart
        cart.add(product=product, quantity=product_qty)
        # get the cart quantity
        cart_quantity = cart.__len__()

        # Return response
        # response = JsonResponse({'Product Name': Product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product added to the cart ...")
        return response
    

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        cart.update(
            product=request.POST.get('product_id'),
            quantity=request.POST.get('product_qty')
        )
        return JsonResponse({'status': 'ok'})

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        cart.delete(product=request.POST.get('product_id'))
        return JsonResponse({'status': 'ok'})
