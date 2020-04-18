import random, string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator_actor(instance,new_slug=None):

    if new_slug is not None: # 'new_slug' is none on first call
        slug = new_slug
    elif instance.slug is not None:
        slug = slugify(instance.slug)
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exclude(id=instance.id).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug,randstr=random_string_generator(size=4))
     
        return unique_slug_generator_actor(instance,new_slug=new_slug)
    
    return slug
