from django.db import models

from billing.models import BillingProfile
from addresses.models import Address
# from carts.models import Cart

from django.db.models.signals import pre_save
from products.utils import unique_orderid_generator

from decimal import Decimal

ORDER_STATUS_CHOICES =(('created','Order is created'),('Packing','Is being made ready'),('Shipped','Product is shipped from the ware house'),('paid','You have paid for order'))

class OrderManager(models.Manager):
    
    def get_or_new(self, cart_obj, bill_obj):
        order_obj = self.get_queryset().filter(cart=cart_obj, billingProfile=bill_obj, status='created').first() or None
        if order_obj is None:
            order_obj = self.get_queryset().create(cart=cart_obj, billingProfile=bill_obj)
        
        if order_obj.order_total != cart_obj.total:
            order_obj.update_order(cart_obj)
# this condition is being checked inadvertently everytime we obtain the specific order obj
# hence getting updated everytime it is called

        return order_obj

#below 'Order' model contains three 'Foreign Keys'
class Order(models.Model):
    order_id       = models.CharField(max_length=120,blank=True)

    billingProfile = models.ForeignKey(BillingProfile,on_delete=models.PROTECT)
    #Order <-- BillingProfile - To define many to one relation with BillingProfile i.e
    # a billingProfile can have many orders - we use Foreign key field
    address        = models.ForeignKey(Address,null=True,blank=True,on_delete=models.CASCADE)
    cart           = models.ForeignKey('carts.Cart',on_delete=models.PROTECT)
    # This sort of reference, called a lazy relationship, can be useful when resolving circular import dependencies between two applications.

    status         = models.CharField(max_length=20,default='created',choices=ORDER_STATUS_CHOICES)
    order_total    = models.DecimalField(max_digits=8,decimal_places=2,default=0.0) 
    total          = models.DecimalField(max_digits=8,decimal_places=2,default=0.0) 

    razor_pay_id = models.CharField(max_length=120,null=True,blank=True)
# there should be some transaction detail on our side as well for reference
# hence we are including this parameter in our Order object
    
    objects = OrderManager()
    #defining our new 'model Manager' here

    def __str__(self):
        return self.order_id
    
    # this function dynamically updates our order total when 
    # when there is any removal or addition in the cart which intuen changes the cart.total 
    def update_order(self,cart_obj):
        if self.order_total != cart_obj.total:
            self.order_total = cart_obj.total
            self.total = round(self.order_total * Decimal(1.18),2)
            self.save() #saving the order

def orderid_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.order_id is None or instance.order_id=="":
        instance.order_id = unique_orderid_generator(instance)
    #random order id generated from the function defined in the utils.py of product

pre_save.connect(orderid_pre_save_receiver, sender=Order)
# calls before a model’s save() method is called.
