from django.db import models

from django.urls import reverse
from .utils import unique_slug_generator_actor
from django.db.models.signals import pre_save

from django.db.models import Q


class ActorQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):     
        lookups = (Q(name__icontains=query) | Q(bio__icontains=query) | Q(rating__iexact=query) )
        return self.filter(lookups).distinct()



class ActorManager(models.Manager):
    def get_queryset(self):
        return ActorQuerySet(self.model,using=self._db) 

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().search(query)


class Actor(models.Model):
    name = models.CharField(max_length=50)
    rating =  models.DecimalField(max_digits=2,decimal_places=1,null=True,blank=True)
    image = models.ImageField(null=True, blank=True,upload_to="actors")
    bio = models.TextField(null=False,blank=False)
    slug = models.SlugField(null=True,blank=True)
    active = models.BooleanField(default=True)
    birthDate = models.DateField(auto_now=False, auto_now_add=False)
    deathDate = models.DateField(null=True,blank=True,auto_now=False, auto_now_add=False)

    objects = ActorManager()

    def __str__(self):
        return self.name
    
    def get_abs_url(self):
        return reverse('actor:details',kwargs={"slug":self.slug})
    
    # def get_abs_url1(self):
    #     return reverse('product:details',kwargs={"pk":self.id})


def actor_slug_pre_save_receiver(sender, instance, *args, **kwargs):

    instance.slug = unique_slug_generator_actor(instance) 

pre_save.connect(actor_slug_pre_save_receiver,sender=Actor)
