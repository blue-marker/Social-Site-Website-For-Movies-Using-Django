from django.shortcuts import render, redirect

from .forms import AddressForm

from billing.models import BillingProfile
from orders.models import Order
from carts.models import Cart
from .models import Address

from django.utils.http import is_safe_url



# Create your views here.
def add_address(request):
    redirect_path = request.POST.get('next_url') or None
    form = AddressForm(request.POST or None)
#this is interesting:
# request.POST contains data which is inserted in form which is itself indirectly rendered from AddressForm func 
# and above we inputing the same data ( i.e data obtained from form which is contained in request.POST now) in AddressForm so as to validate our data defined in the AddressForm itself

    if form.is_valid():
        add_obj = form.save(commit=False)
# form.save will itself create a address obj and save it in the database by default (since it's a ModelForm and the data required to create addr obj has already in it)

# form.save(commit=False) will return a address obj without saving it in the database
# so that we can add billing profile data in the add obj and then
# permanently saved it in our database

        bill_obj = BillingProfile.objects.get_or_new(request)
        add_obj.billing_profile = bill_obj
        add_obj.save()
        add_address_to_order(request, add_obj)
# address created is added to the current order
        if redirect_path:
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)

    return redirect("home")


#as the name suggests this func is to add
#the add in order obj
def add_address_to_order(request, add_obj):
    cart_obj = Cart.objects.new_or_get(request)
    order_obj = Order.objects.get_or_new(cart_obj, add_obj.billing_profile)
    order_obj.address = add_obj
    order_obj.save()
#this function is called in above function

def attach_address(request):
# the request contains POST data from the selectAddress.html
# here we are collecting the add obj selected in the front end from the list of addresses
    redirect_path = request.POST.get('next_url') or None
    addid = request.POST.get('address')
    add_obj = Address.objects.filter(id=addid).first()
    add_address_to_order(request, add_obj)
# address selected is added to the current order

    if redirect_path:
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    
    return redirect("home")




# Every ModelForm also has a save() method. This method creates and saves a database object from the data bound to the form. A subclass of ModelForm can accept an existing model instance as the keyword argument instance; if this is supplied, save() will update that instance. If it’s not supplied, save() will create a new instance of the specified model:

# This save() method accepts an optional commit keyword argument, which accepts either True or False. If you call save() with commit=False, then it will return an object that hasn’t yet been saved to the database. In this case, it’s up to you to call save() on the resulting model instance. This is useful if you want to do custom processing on the object before saving it, or if you want to use one of the specialized model saving options. commit is True by default.