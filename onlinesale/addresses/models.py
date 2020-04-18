from django.db import models

from billing.models import BillingProfile
from datetime import datetime 
# Create your models here.
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
#if the billing profile is deleted then the address will also be deleted
    address_to_name = models.CharField(max_length=120)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120,default='-',null=True, blank=True) 
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120,default='India')
    state           = models.CharField(max_length=120)
    pin_code        = models.CharField(max_length=120)

    timestamp       = models.DateTimeField(auto_now_add=True,blank=True)
    # this field is added to sort the address list according to recent ones
    # also note that add obj list has been sliced in the template to limit
    # only two address max
    class Meta:
        ordering = ['-timestamp',]

    def get_address(self):
# this function returns the address in a format we have defined  
        
        if self.address_line_2:
            add = self.address_to_name + "\n" + self.address_line_1 + ", \n" + self.address_line_2 + "\n" + self.country +"," + self.state + ", \n" + self.city+ "-"+ self.pin_code
        else:
            add = self.address_to_name + "\n" + self.address_line_1 + ", \n" + self.country +"," + self.state + ", \n" + self.city+ "-"+ self.pin_code 

        return add

      
    