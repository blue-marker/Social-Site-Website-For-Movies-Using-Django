from django import template
register = template.Library()

@register.simple_tag
def relative_url(urlencode=None):
    # the urlencode contains the query string the current get request url
    # e.g 'next=1&value=3'
    if 'sort' in urlencode:
        querystring = urlencode.split('&') # list containg key-values
        sort_key_values = list(filter(lambda p: p.split('=')[0] == 'sort', querystring))
        # this checks for the sort key-values
        # print(f)
        key,value = sort_key_values[0].split('=')
        url = value 

        return value