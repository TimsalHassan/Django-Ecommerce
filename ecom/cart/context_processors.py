from .cart import Cart

# Create context processor so that cart is available on every page
def cart(request):
    
    # Return the default cart from our cart
    return {'cart': Cart(request)}