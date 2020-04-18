from django.db import models

from products.models import Product
from orders.models import Order

from django.db.models.signals import m2m_changed,post_save,post_delete
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models.signals import post_save,pre_save

from decimal import Decimal


class WatchlistManager(models.Manager):
    def get_or_new(self, request):

        if request.user.is_authenticated:
            watchlist_obj = self.get_queryset().filter(user=request.user).first() or None

            if watchlist_obj is None:
                watchlist_obj = self.get_queryset().create(user=request.user)

            return watchlist_obj


class Watchlist(models.Model):
    user        = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField('products.Product',blank=True,null=True)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    objects = WatchlistManager() 


    def __str__(self):
        return str(self.user.full_name) +"'s_watchlist" 


def user_post_save_receiver(sender,instance,created,*args,**kwargs):

    if created:
        Watchlist.objects.create(user=instance)

post_save.connect(user_post_save_receiver, sender=User) 
