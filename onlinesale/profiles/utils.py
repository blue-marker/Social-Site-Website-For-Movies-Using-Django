import random, string
from django.utils.text import slugify



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_slug(instance,new_slug=None):

    if new_slug is not None:
        slug = new_slug
    elif instance.slug is not None:
        slug = slugify(instance.slug)
    else:
        slug = slugify(instance.user.full_name)
 
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exclude(id=instance.id).exists()
    
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug,randstr=random_string_generator(size=4))
        # if the slug already exists, we are generating a new one
        return create_slug(instance,new_slug=new_slug)
    
    return slug