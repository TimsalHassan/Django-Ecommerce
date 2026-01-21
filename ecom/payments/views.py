import stripe

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from cart.cart import Cart

from orders.models import Order, OrderItem
from .forms import PaymentForm

from products.models import Product

# Create your views here.
stripe.api_key = settings.STRIPE_API_SECRET_KEY


def checkout_payment(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty")
        return redirect('cart_summary')

    cart_items = cart.get_items()
    quantities = cart.get_quantities()
    totals = cart.cart_totals()

    # Save shipping info ONLY on POST
    if request.method == "POST":
        request.session['my_shipping'] = request.POST

    billing_form = PaymentForm()

    return render(request, 'checkout_payment.html', {'cart_items': cart_items, 'quantities': quantities, 'totals': totals, 'shipping_info': request.session.get('my_shipping'), 'Billing_form': billing_form})


def payment_success(request):
    return render(request, 'checkout_complete.html')

def create_checkout_session(request):
    cart = Cart(request)
    totals = cart.cart_totals()


    if len(cart) == 0:
        return redirect('cart_summary')

    request.session['checkout_cart'] = cart.cart

    request.session['checkout_totals'] = {
        'subtotal': float(totals['subtotal']),
        'discount': float(totals['discount']),
        'total': float(totals['total']),
    }
    line_items = []

    for item in cart.get_items():
        product = item['product']
        price = item['price']
        quantity = item['qty']

        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product.name},
                'unit_amount': int(price * 100),
            },
            'quantity': quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('checkout_complete')
        ),
        cancel_url=request.build_absolute_uri(
            reverse('payment_cancel')
        ),
    )

    return redirect(session.url, code=303)


    
def checkout_complete(request):
    cart_data = request.session.get('checkout_cart')
    totals = request.session.get('checkout_totals')
    shipping = request.session.get('my_shipping')

    if not cart_data or not totals or not shipping:
        messages.error(request, "Session expired")
        return redirect('home')

    # Create Order
    if request.user.is_authenticated:
        order = Order.objects.create(
            user=request.user,
            full_name=f"{shipping['first_name']} {shipping['last_name']}",
            email=shipping['email'],
            shipping_address=f"{shipping['primary_phone']}\n{shipping['city']}\n{shipping['state']}",
            amount_paid=totals['total']
        )
    else:
        order = Order.objects.create(
            full_name=f"{shipping['first_name']} {shipping['last_name']}",
            email=shipping['email'],
            shipping_address=f"{shipping['primary_phone']}\n{shipping['city']}\n{shipping['state']}",
            amount_paid=totals['total']
        )

    # Create Order Items
    for product_id, qty in cart_data.items():
        product = Product.objects.get(id=product_id)
        price = product.discount_price if product.is_discounted else product.price

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price=price
        )

    # Clear session
    for key in ['checkout_cart', 'checkout_totals', 'my_shipping', 'session_key']:
        if key in request.session:
            del request.session[key]

    messages.success(request, "Payment successful! Order placed.")
    return render(request, 'checkout_complete.html', {'order': order})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from products.models import Product
from orders.models import Order, OrderItem
import uuid

def checkout_complete(request):
    cart_data = request.session.get('checkout_cart')
    totals = request.session.get('checkout_totals')
    shipping = request.session.get('my_shipping')

    if not cart_data or not totals or not shipping:
        messages.error(request, "Session expired. Please try again.")
        return redirect('home')

    transaction_ref = f"REF-{uuid.uuid4().hex[:8].upper()}"
    auth_code = f"AUTH-{uuid.uuid4().hex[:6].upper()}"

    # Create Order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        full_name=f"{shipping['first_name']} {shipping['last_name']}",
        email=shipping['email'],
        shipping_address=(
            f"{shipping['primary_phone']}\n"
            f"{shipping['city']}\n"
            f"{shipping['state']}\n"
            f"{shipping.get('country', '')}"
        ),
        amount_paid=totals['total'],
        transaction_id=transaction_ref,
        created_at=timezone.now(),
    )

    # Create Order Items
    for product_id, qty in cart_data.items():
        product = get_object_or_404(Product, id=product_id)
        price = product.discount_price if product.is_discounted else product.price

        OrderItem.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order=order,
            product=product,
            quantity=qty,
            price=price
        )

    # Clear session
    for key in ['checkout_cart', 'checkout_totals', 'my_shipping', 'session_key']:
        request.session.pop(key, None)

    messages.success(request, "Payment successful! Order placed.")

    return render(request, 'checkout_complete.html', {
        'order': order,
        'order_items': order.orderitem_set.all(),  # CORRECT
        'transaction_ref': transaction_ref,
        'auth_code': auth_code,
    })



def payment_cancel(request):
    messages.error(request, "Payment failed or was canceled. Please try again.")
    return render(request, 'payment_cancel.html')
