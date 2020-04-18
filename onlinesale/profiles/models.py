from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()
from products.models import Product
from PIL import Image

from django.urls import reverse

from.utils import create_slug
from django.db.models.signals import pre_save

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    product = models.ManyToManyField('products.Product',through='ProfileRatings',blank=True)
    slug = models.SlugField(null=True,blank=True)
    blogs = models.ManyToManyField('blog.Post',blank=True)
    # should be OneToMany
    about_me = models.TextField(null=True,blank=True)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.full_name} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):  
        return reverse('profile:profile',kwargs={'slug':self.slug})


class ProfileRatingsManager(models.Manager):
    
    def get_or_new(self,profile,product,rating):

        profil_rate_obj = self.get_queryset().filter(profile=profile, product=product).first() or None

        if profil_rate_obj is None:
            profil_rate_obj = self.get_queryset().create(profile=profile, product=product,rating=rating)
        else:
            # profil_rate_obj = self.get_queryset().create(profile=profile, product=product,rating=rating)
            profil_rate_obj.rating = rating
            profil_rate_obj.save()
                     
        return profil_rate_obj  

#this is the class which creates the through model
class ProfileRatings(models.Model): #this is our through model
    profile = models.ForeignKey(Profile, related_name='profile_ratings', on_delete=models.CASCADE, null=True)

    product = models.ForeignKey('products.Product', related_name='profile_ratings', on_delete=models.SET_NULL, null=True, blank=True)

    rating  =  models.DecimalField(max_digits=3,decimal_places=1,default=0)


    objects = ProfileRatingsManager()


    def __str__(self):
        return str(self.profile.user.full_name) +"_"+str(self.product.title) +"_"+ 'rating'



def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        instance.save()

pre_save.connect(pre_save_post_receiver,sender=Profile)