from django.shortcuts import render
from django.http import HttpResponse

from carts.models import Cart
from billing.models import BillingProfile
from .models import Order

from accounts.forms import SignInForm
from addresses.forms import AddressForm
from addresses.models import Address


# Create your views here.
def create_order(request):
    loginform = SignInForm()
    addressForm = AddressForm()
    context = {'loginform':loginform,'addressForm':addressForm}
    cart_obj = Cart.objects.new_or_get(request) #getting existing cart obj or creating a new one
    bill_obj = BillingProfile.objects.get_or_new(request) #getting existing cart obj or creating a new one

    if cart_obj and bill_obj: 
# if both cart_obj and bill_obj are created then either return existing order obj or create a new one
# hence if in case you click on the order button again it will just return the existing one
        order_obj = Order.objects.get_or_new(cart_obj, bill_obj)
        context['order_obj'] = order_obj
        add_list = Address.objects.filter(billing_profile=bill_obj)
# above we have obtained a query list of address objects from billing profile
# note : a billing profile can have many address objects
        context['addList']=add_list      

    return render(request,"orders/placeorder.html",context)
        # order_obj will display the order id since we
        # have redefined its __str__ to return order_id

# this is the finishing business logic for
# completion of order payment
def received_payment(request):
    print(request.POST) #the request.POST data contains json response from api

    orderid = request.POST.get("shopping_order_id") # this is hidden value which we have sent
    payid = request.POST.get("razorpay_payment_id") # this is the json response that we get from api

    # bill_obj = BillingProfile.objects.get_or_new(request)
    # cart_obj = Cart.objects.new_or_get(request)
    # order_obj = Order.objects.get_or_new(cart_obj, bill_obj)
    order_obj = Order.objects.filter(order_id=orderid).first()

    if order_obj:
        order_obj.razor_pay_id = payid
        order_obj.status = "paid"
        order_obj.cart.active = False 
# this is important because we don't want this cart to be reloaded in the current session after the payment
        order_obj.cart.save()
# also need to save cart object to save it's active state as 'False' in the database
# if this step is skipped, the session will reload the same session as the cart object is still active
        order_obj.save()
        print(order_obj.cart.active)

        del request.session['cart_id']
# this needs to be done after payment completion of order 
# so that the current session can be renewed
        context = {'orderid':orderid, 'payid':payid}
        
    return render(request, "orders/success.html", context)