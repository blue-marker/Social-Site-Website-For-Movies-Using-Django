from django.db import models

# Create your models here.
# from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save

from django.contrib.auth import get_user_model
User = get_user_model()

import razorpay
client = razorpay.Client(auth=("rzp_test_fPP6gYO5CQ8U9T","155kzEd1EhdDGGlKquoImRdt"))


class BillingProfileManager(models.Manager):

    def get_or_new(self, request):

        if request.user.is_authenticated:
            bill_obj = self.get_queryset().filter(user=request.user).first() or None
            # if the query returns a bill object then it is stored in the variable
            # and if it returns nothing i.e blank, None is stored in the variable 

            #e.g
            # >>> a=''
            # >>> a or None
            # >>> print(a or None) --> None

            # >>> a='water'
            # >>> print(a or None) --> water

            # if the user is authenticated then we get the bill obj but in case 
            # the bill obj wasn't created (which may not happen because a billing profile is created at the time of user creation ) the second condition takes care of it i.e creates a new one 

            # note: a billing profile is created only once, a user may update it later

            if bill_obj is None:
                bill_obj = self.get_queryset().create(user=request.user, email=request.user.email)

            return bill_obj

class BillingProfile(models.Model):
    user   = models.OneToOneField(User, null=True,
    blank=True, on_delete=models.CASCADE)
    email  = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    customerid = models.CharField(max_length=100,null=True,blank=True)
    #this customer id is created using razorpay by providing some customer data
    
    objects = BillingProfileManager()
    # defining the our new model Manager here

    def __str__(self):
        return str(self.user) + "-" + self.email

# a post signal function for creating a billing profile 
# everytime a new user is created
def user_post_save_receiver(sender,instance,created,*args,**kwargs):
# created - A boolean; True if a new record was created.
# this is a argument passed in post_save signal

# this is just like a double check condition so that 
# a billing profile isn't created while updating the user 

# created is 'True' only once during the creation and
# 'False' in other cases such as while updation and saving  
    if created:
        BillingProfile.objects.create(user=instance,email=instance.email)
        #remember instance is an object of class just newly created 
    
#the above function will be activated every time after save  
post_save.connect(user_post_save_receiver, sender=User) 
#Like pre_save, but sent at the end of the save() method.


def customer_billingprofile_post_save_receiver(sender,instance,*args,**kwargs):

    #this condition will be 'True' only for the first time while creating
    if not instance.customerid:
#client is an object defined above
#we get the json response from the query we have created 
        data = client.customer.create(data={
            "name"    : instance.user.full_name,
            "email"   : instance.email,
            "contact" : instance.user.mobile,})
        print(data)
        instance.customerid = data.get('id') 
        
        #remember instance is an object of class just created 

#the above function will be activated every time before save  
pre_save.connect(customer_billingprofile_post_save_receiver, sender=BillingProfile) 

# To receive a signal, register a receiver function using the Signal.connect() method. The receiver function is called when the signal is sent. All of the signal’s receiver functions are called one at a time, in the order they were registered.

# sent before or after a model’s save() method is called.

# sender: is the model class that just had an instance created.
# instance : The actual instance of the model that’s just been created.

# for e.g if a user object is created ,'User' is the model passed in the sender 
# and the user object just created is the 'instance' 
# and the function passed i.e 'user_post_save_receiver' is the receiver function
# which does something the signal is triggered 


# if the sender is not defined then the receiver function is called 
# every time any model object is created hence it is necessary to define at 
# which oject creation the post_save receiver function should be triggered


#create trigger user_post_save_receiver
#after insert ON user
#begin 
# insert into billing profile

#before insert
#after insert
#before update
#after update

#pre_save
#post_save

# created = True - insert
# Fasle - Update



