import random, string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    # this returns a random generated string consisting of alphabets and digits of size 10

    # s =''
    # for i in range(size):
    #     s = s+random.choice(chars)
    # return s

def unique_orderid_generator(instance, new_orderid=None):
    if new_orderid is not None:
        orderid = new_orderid
    else:
        orderid = random_string_generator().upper()
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=orderid).exclude(id=instance.id).exists()

    if qs_exists:
        new_orderid = "{}{}".format(orderid, random_string_generator(size=2))
        return unique_orderid_generator(instance, new_orderid)
        
    return orderid


def unique_slug_generator(instance,new_slug=None):
    # 'new_slug' value is passed during recursion otherwise it is None by default on first call
    """
    this is for django project and it assumes your instance
    has a model with a slug field and a title character (char) field.  
    """
    # it goes to first condition when it is on recursion
    # otherwise goes to second or third condition based on whether
    # the user has entered any slug value or not

    if new_slug is not None: # 'new_slug' is none on first call
    # during recursive call it has some values
        slug = new_slug

    elif instance.slug is not None:
        slug = slugify(instance.slug)
    # this condition is satisfied when user has given some input in slug field
    else:
        slug = slugify(instance.title)
    # if the user hasn't given any input then by default this condition is satisfied
    # where the title of the product name is slugified

    # Note : slugify function converts text in small letters and spaces into hypen

    Klass = instance.__class__
    # instance is an object of the particular class which have been passed as an arguement
    # here what we are doing is creating a 'class' out of the 'object'

    qs_exists = Klass.objects.filter(slug=slug).exclude(id=instance.id).exists()

    #the above checks whether other products (excluding itself) has same slug value or not

    # if the above returns 'True' then random string generator function is called to add
    # more ambiguity to existing slugified name
    #and then the same function is called again to again check the duplicacy of the new slug

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug,randstr=random_string_generator(size=4))
        # if the slug already exists, we are generating a new one
        return unique_slug_generator(instance,new_slug=new_slug)
    
    return slug
