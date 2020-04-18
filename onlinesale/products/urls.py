from django.urls import path
from .views import product_list,ProductListView,ProductDetailView,update_rating

urlpatterns = [
    path("",product_list,name="fbv"),
    path("cbv/",ProductListView.as_view(),name="cbv"),
    path("<slug:slug>/",ProductDetailView.as_view(),name="details"),
    path("<slug:slug>/rating/",update_rating,name="update_rating"),
    # path("api/chart/data/<str:path>/",get_data,name="chart"),
    # path("genre/<str:genre>/",genre_list,name="genre"),
]
# note: this is not kwargs
# this just acts like an identifier to capture the kwargs
# this does two work: 
# displays the slug/pk in the url pattern and also 
# this value is passed as keyword arguement to class based view which
# in turn helps in rendering that selected product

# hence for generic DetailView class we need to pass either slug value or pk value 
# in order to select the product which needs to be rendered

    # path("<int:pk>/",ProductDetailView.as_view(),name="details")


# 'ProductListView' and 'ProductDetailView' are classes, not function, so we point the URL to the as_view() class method instead, which provides a function-like entry to class-based views
# Any arguments passed to as_view() will override attributes set on the class.

# In Class-based views, you have to call as_view() function so as to return a callable view that takes a request and returns a response. Its the main entry-point in request-response cycle in case of generic views.

# as_view is the function(class method) which will connect my MyView class with its url.

# Notes:

# To capture a value from the URL, use angle brackets.
# Captured values can optionally include a converter type. For example, use <int:name> to capture an integer parameter. If a converter isn’t included, any string, excluding a / character, is matched.
# There’s no need to add a leading slash, because every URL has that. For example, it’s articles, not /articles.


# Once one of the URL patterns matches, Django imports and calls the given view, which is a Python function (or a class-based view). The view gets passed the following arguments:

# An instance of HttpRequest.

# If the matched URL pattern contained no named groups, then the matches from the regular expression are provided as positional arguments.

# The keyword arguments are made up of any named parts matched by the path expression that are provided, overridden by any arguments specified in the optional kwargs argument to django.urls.path() or django.urls.re_path().

# for example here a request to /products/robin-williams/ would match the third entry in the list. 

# The indentifier '<slug:slug>/<int:pk>/<str:name>' (slug and int are converter type used to capture their respective type parameter) helps to identify the slug value or int value and pass that value in key as slug='robin-williams' or int=3 or name='varun' and pass it to class view 

#note : since here we are using generic class view , we can only use either pk or slug

# Django would call the class view as  ProductDetailViewviews.as_view(request, slug="robin-williams").