from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart, ProductAmount


def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    context = {'cart_obj':cart_obj}
    return render(request,'carts/list.html',context)

#this function is the business logic for button in cart
def update_cart(request):
    cart_obj = Cart.objects.new_or_get(request) #get the new or existing cart object

    # this function in view is only for 'POST' method
    # i.e on button click in ProductDetail
    # the same condition is checked below

    if request.method == 'POST':
        #extracting details
        prodid = request.POST.get('prodid')    
        prodquant = int(request.POST.get('prodquant'))
# we converted the prod quant into 'int' data type so that
# we can use it to update in the respective product stock quant

        # we have passed the prodid value through request.'POST' object
        # hence we can get its value
        
        if prodid:
            prod_obj = Product.objects.filter(id=prodid).first()

# if the prodquant entered by the user is greater than the quantity in stock for that product
# then redirect to the same page
            if prodquant > prod_obj.quantity:
                return redirect( prod_obj.get_abs_url() )    

            #prod_obj is that instance of the 'Product' that we add in cart object
         
            if prod_obj in cart_obj.products.all():
                #remove:
                #if the product is listed in existing cart object then remove it

                # cart_obj.products.remove(prod_obj)
                prod_quant_obj = ProductAmount.objects.filter(product__id= prod_obj.id,cart__id=cart_obj.id).first()
                #retrieving the prod amount

                Product.objects.filter(id=prod_obj.id).update( quantity=prod_obj.quantity + prod_quant_obj.amount ) 
                #updating the product stock

                prod_quant_obj.delete()  
                #deleting the 'ProductAmount' object and thus deleting from the cart       

            else:
                #add:
                #if the product doesn't exist in existing cart object then add it
                # cart_obj.products.add(prod_obj)

                Product.objects.filter( id=prodid ).update( quantity=prod_obj.quantity - prodquant )
                #updating the product stock 

                instance = ProductAmount(cart=cart_obj,product=prod_obj)
                #creating a new unsaved 'ProductAmount' object

                #adding the amt and then saving it in the database
                if prodquant is not 0:
                    instance.amount = prodquant
                    instance.save()
                else:
                    #the default in amount field is '1'
                    instance.save()

    return redirect('cart:list')
    #redirect to the 'carts/list.html' page after addition or removal



    # The invisible "through" model that Django uses to make many-to-many relationships work requires the primary keys for the source model and the target model. A primary key doesn't exist until a model instance is saved, so that's why both instances have to exist before they can be related. (You can't add spinach to your pizza if you haven't bought spinach yet, and you can't add spinach to your pizza if you haven't even started rolling out the crust yet either.)
