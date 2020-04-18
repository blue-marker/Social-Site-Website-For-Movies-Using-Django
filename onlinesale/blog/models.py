from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

from django.urls import reverse

from django.db.models.signals import pre_save,post_save
from .utils import create_slug
from .utils import get_read_time

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    content = models.TextField()
    image = models.ImageField(null=True,blank=True,width_field='width_field',height_field='height_field',upload_to="post_pics")
    width_field = models.IntegerField(default=300)
    height_field = models.IntegerField(default=200)
    date_posted = models.DateTimeField(default=timezone.now)
    # we can also pass the follow parameter : 
    # auto_now     :  Automatically set the field to now every time the object is saved.
    # auto_now_add :  Automatically set the field to now when the object is first created

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_time = models.TimeField(null=True,blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):  # this is used by the CreateView & UpdateView
    # instead of this we can also use 'success_url' or 'get_success_url' in CreateView Or UpdateView
    # after creating a new object out of this model,
    # the 'get_absolute_url' method routes back to this path
        return reverse('blog-home')
        # the reverse returns a full path as a string
        #  reverse('blog-home',kwargs={"id":self.id})



def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        instance.save()

    # if instance.content:
    #     read_time = get_read_time(instance.content)
    #     instance.read_time = read_time
    #     instance.save()
    
pre_save.connect(pre_save_post_receiver,sender=Post)

# def post_save_post_receiver(sender,instance,*args,**kwargs):

#     if instance.content:
#         read_time = get_read_time(instance.content)
#         instance.read_time = read_time
#         instance.save()

# post_save.connect(post_save_post_receiver,sender=Post)