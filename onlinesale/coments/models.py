from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.urls import reverse

class ComentManager(models.Manager):

    def all(self):
        qs = super().filter(parent=None)
        return qs

    def filter_by_instance(self,instance):
        # content_type = ContentType.objects.get_for_model(Product)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ComentManager,self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        #Coments.object
        
        return qs


class Coment(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    # parent attribute are for those coments which are actually replies
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ComentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.user.full_name)

    def children(self):#replies
        return Coment.objects.filter(parent=self)
        #returns all the reply objects which that comment as parent

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    #this property return the boolean value for whether the comment is parent or not
    
    def get_absolute_url(self):
        return reverse("comment:thread",kwargs={'id':self.id})