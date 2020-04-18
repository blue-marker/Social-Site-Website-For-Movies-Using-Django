from django.db import models

from django.urls import reverse
from .utils import unique_slug_generator
from django.db.models.signals import pre_save

from django.db.models import Q

from coments.models import Coment
from django.contrib.contenttypes.models import ContentType
# migrations - migrations are useful because it allows us to make changes
# to our database even after it's been created and has data in that
# so if we didn't have a way to run migrations we would have to run
# some complicated SQL code to update our database structure so that it didn't 
# mess with the current data but with migrations we can simply make whatever changes we
# need, run makemigrations and then run migrate and it will make all of the changes for us  

# Create your models here.
class ProductQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) | Q(price__iexact=query) | Q(tag__title__iexact=query) | Q(tags__title__iexact=query) | Q(director__iexact=query) | Q(actors__name__iexact=query) )

        return self.filter(lookups).distinct()

# A Q() object, like an F object, encapsulates a SQL expression in a Python object that can be used in database-related operations.

# In general, Q() objects make it possible to define and reuse conditions. This permits the construction of complex database queries using | (OR) and & (AND) operators; in particular, it is not otherwise possible to use OR in QuerySets.


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db) 

    #we have redefined the all function to return only active products
    def all(self):
        return self.get_queryset().active()
    
    # the core functionality of search is defined in the ProductQuerySet
    # 'query' is the parameter for the searched keyword
    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    title = models.CharField(max_length=50)
    imdb =  models.DecimalField(max_digits=2,decimal_places=1,null=True,blank=True)
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    # auto_now     :  Automatically set the field to now every time the object is saved.
    # auto_now_add :  Automatically set the field to now when the object is first created
    director = models.CharField(max_length=50)
    slug = models.SlugField(null=True,blank=True)
    rating =  models.DecimalField(max_digits=3,decimal_places=1,null=True,blank=True)
# A "slug" is a way of generating a valid URL, generally using data already obtained. For instance, a slug uses the title of an article to generate a URL.
# A slug field in Django is used to store and generate valid URLs for your dynamically created web pages.
# It's a descriptive part of the URL that is there to make it more human descriptive, but without necessarily being required by the web server - in What is a "slug" in Django? the slug is 'in-django-what-is-a-slug', but the slug is not used to determine the page served (on this site at least)
    image = models.ImageField(null=True, blank=True, upload_to="products")
    trailer_link= models.URLField(max_length=700,null=True,blank=True)
    actors= models.ManyToManyField('actors.Actor',blank=True)
    # for this field to work Pillow file need to be imported
# note: Pillow module is generally used to play with images in python
    # the image will get uploaded to folder named 'products' in the MEDIA_ROOT
    # specified in the settings.py

    price = models.DecimalField(default=10, max_digits=10, decimal_places=2)
    tags = models.ManyToManyField('tags.Tag',blank=True)
# This sort of reference, called a lazy relationship, can be useful when resolving circular import dependencies between two applications.
    quantity = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(null=True)
    active = models.BooleanField(default=True)
    createdDate = models.DateField(auto_now_add=True)
    updatedDate = models.DateField(auto_now=True)

    objects = ProductManager()
    

    def __str__(self):
        return self.title
    
    def get_abs_url(self):
        return reverse('product:details',kwargs={"slug":self.slug})
# If you need to use something similar to the url template tag in your code, Django provides the following function i.e reverse
# If no match can be made, reverse() raises a NoReverseMatch exception.
# this method provides a dynamic way of accessing the url of the specific product
# through 'slug id' which is also a unique identifier

# when this method of particular product object is called it renders the 'ProductDetailView'
# the kwargs is passed to path function 
# this kwargs above overrides the '<slug:slug>' in the url pattern 

    @property
    def comments(self):
        instance = self
        qs = Coment.objects.filter_by_instance(instance)

        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)

        return content_type

    
    def get_abs_url1(self):
        return reverse('product:details',kwargs={"pk":self.id})


def product_slug_pre_save_receiver(sender, instance, *args, **kwargs):

    instance.slug = unique_slug_generator(instance) 
    # Slug is a URL friendly short label for specific content. It only contain Letters, Numbers,Underscores or Hyphens. Slugs are commonly save with the respective content and it pass as a URL string.
    
    # unique slug value is returned and 
    # stored in the current instance of the product's slug field

pre_save.connect(product_slug_pre_save_receiver,sender=Product)
# pre_save is a trigger signal which is initiated just before the saving of the product values

# when the pre_save signal is triggered 
# 'pre_save.connect' calls the 'product_slug_pre_save_receiver' which is our created function
# which in turn generates the slug value in case it is not given 


# To refer to models defined in another application, you can explicitly specify a model with the full application label. For example, if the Manufacturer model above is defined in another application called production, you’d need to use:

# class Car(models.Model):
#     manufacturer = models.ForeignKey(
#         'production.Manufacturer',
#         on_delete=models.CASCADE,
#     )
# This sort of reference, called a lazy relationship, can be useful when resolving circular import dependencies between two applications.