from django.shortcuts import render

from django.views.generic import ListView

from products.models import Product

# Create your views here.
class SearchProductListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs): 

        context = super(SearchProductListView, self).get_context_data()
        # above we are getting the inherited class's (ListView's) context
        # in the above context we have got 'object_list'
        # in addition to which we are defining 'query' in the context dict below

        context['query'] = self.request.GET.get('q')
        #we get the value of 'q' which is the searched word

        return context

    def get_queryset(self, *args, **kwargs):
        
        #here we can use walrus operator, which is new in python 3.8 
        if self.request.GET.get('q', None):
            qs = Product.objects.search(self.request.GET.get('q')) #we get the value of 'q' which is the searched word
            # this contains a list of all products containing the searched word
            # search is a QuerySet function which we have redefined 
            # to our requirement in products.models
        else:
            qs = Product.objects.all()
            # this contains a list of all products

        return qs
        # a list of object is returned 
        # which will be rendered accordingly in 'products/list.html'