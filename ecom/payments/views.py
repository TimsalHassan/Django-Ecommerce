from django.contrib import messages
from django.shortcuts import redirect, render
from cart.cart import Cart

from orders.models import Order, OrderItem
from .forms import PaymentForm

# Create your views here.

def checkout_payment(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_items = cart.get_items()
        quantities = cart.get_quantities()
        totals = cart.cart_totals()

        #Create a session with the shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check if the user is logged in
        if request.user.is_authenticated:
            # Get the Billing Form
            Billing_form = PaymentForm()
            # User logged in
            return render(request, 'checkout_payment.html', {'cart_items': cart_items, 'quantities':quantities, 'totals': totals, "shipping_info":request.POST, "Billing_form":Billing_form })
        else:
            # Get the Billing Form
            Billing_form = PaymentForm()
            # Not logged in
            return render(request, 'checkout_payment.html', {'cart_items': cart_items, 'quantities':quantities, 'totals': totals, "shipping_info":request.POST, "Billing_form":Billing_form })

        # shipping_form = request.POST
    else:
        messages.success(request,"Access Denied!!")
        return redirect('home')
    # return render(request, 'checkout_payment.html')

def checkout_complete(request):
    if request.POST:
        cart = Cart(request)
        cart_items = cart.get_items()
        quantities = cart.get_quantities()
        totals = cart.cart_totals()

        # Get the billing info from the last page 
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get('my_shipping')
        print(my_shipping)
        # Gather the Order info
        first_name = my_shipping['first_name']
        last_name = my_shipping['last_name']
        email = my_shipping['email']
        # Create shipping address from session info
        shipping_address = f"{my_shipping['primary_phone']}\n{my_shipping['area_code']}\n{my_shipping['city']}\n{my_shipping['state']}\n{my_shipping['zip_code']}\n{my_shipping['country']}"
        amount_paid = totals['total']

        # Create the Order
        if request.user.is_authenticated:
            # Logged in user
            # Create Order
            user = request.user
            create_order = Order(user=user, full_name=f"{first_name} {last_name}", email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            # Add Order Items
            # Get the Order ID
            order_id = create_order.id
            # GET the Product ID
            for item in cart_items:
                product = item['product']
                product_id = product.id  
                price = item['price']
                quantity = item['qty']
                # Get the Quantity
                # for key, value in quantities.items():
                #     if key == str(product.id):
                #         # Create Order Item
                create_order_item = OrderItem(user= user, order_id= order_id, product_id= product_id, quantity= quantity, price= price)
                create_order_item.save()

            # Delete the cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    # Delete the cart session
                    del request.session[key]

            messages.success(request,"Order Placed!")
            return redirect('checkout_complete')

        else:
            # Not logged in user
            # Create Order
            user = request.user
            create_order = Order(full_name=f"{first_name} {last_name}", email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            # Add Order Items
            # Get the Order ID
            order_id = create_order.id
            # GET the Product ID
            for item in cart_items:
                product = item['product']
                product_id = product.id  
                price = item['price']
                quantity = item['qty']
                # Get the Quantity
                # for key, value in quantities.items():
                #     if key == str(product.id):
                # Create Order Item
                create_order_item = OrderItem(order_id =order_id, product_id=product_id, quantity=quantity, price=price)
                create_order_item.save()

            # Delete the cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    # Delete the cart session
                    del request.session[key]

            messages.success(request,"Order Placed!")
            return redirect('checkout_complete')

    else:
        messages.success(request,"Access Denied!!")
        return redirect('home')


