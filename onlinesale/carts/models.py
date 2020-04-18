from django.db import models
# from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order

from django.db.models.signals import m2m_changed,post_save,post_delete
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

from decimal import Decimal


#Remember that the 'Cart' object maintained through session
#hence a 'Cart' comes with a session by default

class CartManager(models.Manager):

# this below function either loads already existing
# cart from the session or creates a new cart and load it in the session app 
    def new_or_get(self, request):  
        # session is an inbuilt app, in fact its a Middleware 
        # which is included in setting.py of django 

        # here the cart is maintained in the session for the quick accessibility 

 
        cartid = request.session.get('cart_id', None)
        # a session maintains a key-value pair 

# 1 -  now instead of running a query to get cart obj
#      we can simply pass in request to get the current cart object
# 2 -  for e.g without session we may had to pass this query to get current cart obj:
#      Cart.objects.get(user=request.user)
# 3 -  but now instead we can simply run this query : Cart.objects.new_or_get(request)
# 4 -  it maintains this key-value in its memory temporarily until the user logs out

        # a session works as a reminder to load the object the user had been working on or simply helps in creating a new one indirectly

        if cartid is not None: #if it is not empty then load it 
            cart_obj = Cart.objects.filter(id=cartid).first()
            #id value is passed here which we get through current session

        elif request.user.is_authenticated:     
            cart_obj = Cart.objects.filter(user=request.user,active=True).first() or None
            # get only the active carts
            # i.e ignore the ones (inactive) for which payment has been done

            if cart_obj is None:
                cart_obj = Cart.objects.create(user=request.user)
            
            request.session['cart_id'] = cart_obj.id
            #above code checks whether the authenticated user has already a existing cart in database
            #if yes then it loads the existing cart in the current session otherwise
            # creates a new cart and then load it in current session 
            #here we are also passing user value since it is authenicated
           
            #a new session is created which stores new cart id values with user authenticated

        else:
            cart_obj = Cart.objects.create()
            #this is possible since we have passes 'null=True' in user Foreign key 
            #note here we are not passing user value since it is not authenticated
            #and hence this cart will be different from the one created with user login

            #we are just giving user an option to include products in a cart EVEN WHEN NOT LOGGED IN 
            request.session['cart_id'] = cart_obj.id
            # a new session is created which stores new cart id values
            # so when the user logs in, the same session for cart is maintained through out
            # irrespective of whether that user has already a cart in database 

        return cart_obj

class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # here we have also given 'null=True' so that a cart object be created even when the user is not logged in
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product,through='ProductAmount',blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    # 'auto_now_add' means created only once during the first creation
    
    objects = CartManager() 
    # redefining the models.Manager 

    def __str__(self):
        return str(self.id)

class ProductAmount(models.Model): #this is our through model
    cart       = models.ForeignKey(Cart, related_name='no_of_products', on_delete=models.CASCADE, null=True)

    product    = models.ForeignKey(Product, related_name='no_of_products', on_delete=models.SET_NULL, null=True, blank=True)

    amount     = models.IntegerField(default=1)

""" 
ManyToMany : 
A Cart has many products which is 'OneToMany' Relation

but since there will be multiple users and 
hence many 'Carts' which in turn conatins many 'Products'

this will give us 'ManyToMany' Relation 
- wherein a 'Cart' contains many 'Products' and a 'Product'
  can be contained in many 'Carts'

"""
# @receiver(m2m_changed, sender=Cart.products.through)
# @receiver(post_save,sender=ProductAmount)
@receiver([post_save, post_delete], sender=ProductAmount)
def products_m2m_changed_receiver(sender, instance, *args, **kwargs):
    
# instance.subtotal value is recalculated (looped through all the products)
# everytime a product is added or removed from the cart
# since it is recalculated through looping all the products
# it is initiated to 0 value with change to cart so that previous values are not again totaled 

    cart_inst = instance.cart   
#  this is an instance of 'ProductAmount' model 
#  we are accessing cart instance through 'ProductAmount'
    cart_inst.subtotal = Decimal(0)

    # print(cart_inst)
    for prod in cart_inst.products.all():
        prod_amt = prod.no_of_products.get(cart=cart_inst) #this is the ProductAmount instance
# above we are getting the specific 'ProductAmount' object
# first filtered through that specific product and then cart

        # print(prod_amt.amount)
        cart_inst.subtotal += prod.price * prod_amt.amount 
        # prod_amt.amount = its the amount specific to that product in the current cart 
    if cart_inst.subtotal < Decimal(500):
        cart_inst.total = cart_inst.subtotal + Decimal(80)
    else:
        cart_inst.total = cart_inst.subtotal
        
    cart_inst.save()

#below is the alternative method
# post_save.connect(products_m2m_changed_receiver, sender=ProductAmount)

# 'products_m2m_changed_receiver' is the function that we created for
# m2m_changed trigger signal hence for that function to actually execute
#when the signal is triggered we are using
#m2m_changed.connect()

#instance is like a alias name from triggers in dbms - research it
