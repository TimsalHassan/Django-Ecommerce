from users.models import Profile
from products.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get Requests
        self.request = request
        # Get the current if it exists
        cart = self.session.get('session_key')
        # if the user is new, no session key exists. Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Make sure the cart is available on every page of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in User
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '4':3} to {"3":1, "4":3}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile model
            current_user.update(old_cart= str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in User
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '4':3} to {"3":1, "4":3}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile model
            current_user.update(old_cart= str(carty))

    def __len__(self):
        return len(self.cart)
    
    def cart_total(self):
        # Get Product IDs
        products_ids = self.cart.keys()
        # Lookup those keys in our product database model
        products = Product.objects.filter(id__in= products_ids)
        # Get quantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            # convert key into string so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_discounted:
                        total = total + (product.discount_price * value)
                    else:
                        total = total + (product.price * value)
        return total
    
    def cart_totals(self):
        subtotal = 0
        discount = 0
        total = 0

        for item in self.get_items():
            qty = item['qty']
            price = item['product'].price
            discounted_price = item['price']
            subtotal += price * qty
            discount += (price - discounted_price) * qty
            total += discounted_price * qty

        return {
            'subtotal': subtotal,
            'discount': discount,
            'total': total
        }
    
    def get_items(self):
        items = []
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            qty = self.cart[str(product.id)]

            if product.is_discounted:
                price = product.discount_price
            else:
                price = product.price
            items.append({
                'product': product,
                'qty': qty,
                'price': price,
                'total': price * qty
            })
        return items

    def get_quantities(self):
        quant = self.cart
        return quant
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get cart
        ourcart = self.cart
        # update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        # Deal with logged in User
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '4':3} to {"3":1, "4":3}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile model
            current_user.update(old_cart= str(carty))
            
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        # Delete from Dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        # Deal with logged in User
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '4':3} to {"3":1, "4":3}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the profile model
            current_user.update(old_cart= str(carty))