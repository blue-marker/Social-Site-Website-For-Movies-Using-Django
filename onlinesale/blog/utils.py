import random, string
from django.utils.text import slugify

import datetime
import math
import re

from django.utils.html import strip_tags


def count_words(html_string):
    # html_string = '''<h1>This is a title</h1>'''
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+',word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    read_time = str(datetime.timedelta(minutes=read_time_min))

    return read_time


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_slug(instance,new_slug=None):

    if new_slug is not None:
        slug = new_slug
    elif instance.slug is not None:
        slug = slugify(instance.slug)
    else:
        slug = slugify(instance.title)
 
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exclude(id=instance.id).exists()
    
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug,randstr=random_string_generator(size=4))
        # if the slug already exists, we are generating a new one
        return create_slug(instance,new_slug=new_slug)
    
    return slug
