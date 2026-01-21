from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .models import Profile
from orders.forms import ShippingAddressForm
from cart.cart import Cart
from payments.models import ShippingAddress, ShippingAddressFormModel
from payments.forms import ShippingForm

import json

# Create your views here.

def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current's USer Shipping Info
        shipping_user = ShippingAddressFormModel.objects.get(user__id = request.user.id)
        # Original User Form
        form = UserInfoForm(request.POST or None, instance= current_user)
        # User's Shipping Form
        shipping_form = ShippingAddressForm(request.POST or None, instance= shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # Save original Form
            form.save()
            # Save Shipping Form
            shipping_form.save()
            messages.success(request, ("Your Info Has Been Updated ..."))
            return redirect('home')    
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request,("You must Be Logged In To Access That Page!!"))
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, ("Your Password has been updated ... "))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                        messages.error(request, error)
                        return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
          messages.success(request, ("You must be logged in to view that page ..."))
          return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance= current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("User Has Been Updated ..."))
            return redirect('home')    
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request,("You must Be Logged In To Access That Page!!"))
        return redirect('home')


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
              form.save()
              username = form.cleaned_data['username']
              password = form.cleaned_data['password1']
              # Log in User
              user = authenticate(username= username, password= password)
              login(request, user)
              messages.success(request, ('User created Successfully. Please Fill Out the User Info Below ...'))
              return redirect('update_info')
        else:
              print(form.errors)
              messages.success(request, ('Whoops!There was a problem Registering, please try again...'))
              return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # do some shopping cart Stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to Dictionary using Json
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictinary to our session
                # Get the cart
                cart = Cart(request)
                # Loop through the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)

            messages.success(request, ('You have successfully logged in.'))
            return redirect('home')
        else:
            messages.warning(request, ('Invalid username or password'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.info(request, ('You have been logged out.'))
    return redirect('home')