from django.shortcuts import render,reverse,redirect

from .models import Product
from profiles.models import ProfileRatings,Profile
# from carts.models import Cart

from django.views.generic import ListView, DetailView

from django.db.models import Q

from django.core.paginator import Paginator

from coments.models import Coment
from coments.forms import ComentForm
from django.contrib.contenttypes.models import ContentType

from django.views.generic.edit import FormMixin
# Mixin is a type of multiple inheritance which allows classes in Python to share methods between any class that inherits from that mixin. It is used when we want to implement a specific functionality in different classes.
# Whenever you use any Mixin in one of your class-based views then it acts like a pre-requisite.
# For example: If your view inherits LoginRequiredMixin, then the URL linked to the view can only be made available to the user only if he logins with his/her username and password. This is how mixins work.

from profiles.models import ProfileRatings

from watchlists.models import Watchlist

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.http import HttpResponseRedirect
# Create your views here.

genre_select = None
#global variable

def product_list(request):
    object_list = Product.objects.all()
    context = {'object_list':object_list}
    return render(request,'products/list.html', context)

class ProductListView(ListView):
    paginate_by = 6
    model = Product
    template_name = "products/list.html"
    ordering =['-release_date']
    # '-' means newest to oldest

    def get_context_data(self,*args,**kwargs):
        global genre_select
        context = super(ProductListView, self).get_context_data(*args,**kwargs)

        if self.request.GET.get('genre') and self.request.GET.get('sort'):
            # code for product list look up when both genre and sort is applied
            # i.e when sorting is applied on genres

            lookups = (Q(tag__title__iexact=self.request.GET.get('genre' or None)) | Q(tags__title__iexact=self.request.GET.get('genre' or None)))
            prodList = Product.objects.filter(lookups).distinct().order_by('-'+str(self.request.GET.get('sort')))
            # filters out distinct lookups by the order(- means newest to oldest )given in the sort value which we get by self.request.GET.get('sort')

            # pagination as done in generic view classes
            paginator,page,object_list,is_paginated = self.paginate_queryset(prodList,3)
            # stackoverflow - paginate_queryset
            # when this condition is satisfyed the pagination is changed from 6 to 3

            # paginator = Paginator(prodList,3)
            # page = self.request.GET.get('page',1)
            # context['product_list']=prodList[:3]
            # page_obj = paginator.page(page)
            context['object_list']=object_list
            context['page_obj']  = page  # current page no
            context['paginator'] = paginator #paginator object
            context['is_paginated'] = is_paginated # boolean value
            context['is_genre'] = True
            # print(context) 
            return context

        elif self.request.GET.get('genre'):
            # code for product list look up when only genre is selected ( without sorting applied )

            lookups = (Q(tag__title__iexact=self.request.GET.get('genre' or None)) | Q(tags__title__iexact=self.request.GET.get('genre' or None)))
            prodList=Product.objects.filter(lookups).distinct().order_by('-release_date')
            print(prodList)
            query_string = self.request.GET.urlencode()
            # gives query string eg. genre=Comedy
            # print(query_string)
            if '&' in query_string:
                genre_queryString,_ = query_string.split('&')
                _,genre_select = genre_queryString.split('=')
            else:
                _,genre_select = query_string.split('=') 
            # print(genre_select)

            paginator,page,object_list,is_paginated = self.paginate_queryset(prodList,3)
            # paginator = Paginator(prodList,3)
            # page = self.request.GET.get('page', 1)
            context['object_list']=object_list
            # context['product_list']=prodList[:3]
            # page_obj = paginator.page(page)
            context['page_obj']  = page
            context['paginator'] = paginator
            context['is_paginated'] = is_paginated
            context['is_genre'] = True
            # print(context)
            return context

        elif self.request.GET.get('sort'):
             # code for product list look up when only sort is selected 

            prodList=Product.objects.all().order_by('-'+str(self.request.GET.get('sort')))
            paginator,page,object_list,is_paginated = self.paginate_queryset(prodList,6)
            context['object_list']=object_list
            # context['product_list']=prodList[:3]
            # paginator = Paginator(prodList,3)
            # page = self.request.GET.get('page', 1)
            # page_obj = paginator.page(page)
            context['page_obj']   =  page
            context['paginator']  =  paginator 
            context['is_paginated'] =  is_paginated
            context['is_genre'] = False
            # print(context) 
            return context
  
        return context

class ProductDetailView(FormMixin,DetailView):
    model = Product
    template_name = "products/detail.html"
    form_class =  ComentForm

    
    def get_success_url(self):
        return reverse('product:details', kwargs={'slug': self.object.slug})
    
# 'object' key is set by default in the context returned by the DetailView
#  hence 'object' variable must be used to render in template in detail.html

    def get_context_data(self, *args, **kwargs):
        prod_obj = self.object #current model instance
        # comments = Coment.objects.filter_by_instance(prod_obj)
        comments = prod_obj.comments 
        initial_data = {"content_type": prod_obj.get_content_type,"object_id": prod_obj.id}  
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        
# here we are accessing the 'get_context_data' method of the super class/ parent class
# i.e DetailView to return the context dict 

        # cart_obj = Cart.objects.new_or_get(self.request)
        watchlist_obj = Watchlist.objects.get_or_new(self.request) or None
        #a new cart is created or existing is loaded

        # context['in_cart'] = context['object'] in cart_obj.products.all() #True or False
        

        # this condition makes sure that even user who are 
        # not authenticated are able to see the product detail page 
        # without this condition the product detail page would throw
        # an error for unauthenticated users 
        if watchlist_obj:
        # context['object'] gives the particular product object that we are viewing
        # so basically we are checking whether that particular object which we
        # are viewing is in watchlist or not i.e 'in_watchlist' is True or False and....
            context['in_watchlist'] = context['object'] in watchlist_obj.products.all() or None
            #...accordingly the 'in_watchlist' value is set 
            context['profile_rating'] = self.object.profile_ratings.filter(profile_id=self.request.user.profile.id).first() or None

        # this 'in_cart' key is important to pass 
        # so that we can change the button icon accordingly depending upon whether 
        # the product object is in cart or not

        context['comments']= comments
        context['comment_form'] = ComentForm(initial=initial_data)
        
        #context['profile_rating'] = self.object.profile_ratings.filter(profile_id=self.request.user.profile.id).first() or None
        
        " Below code is for Rating logic "

        product_rating_all = ProfileRatings.objects.filter(product=self.object).all() or None
        # list of all the ProfileRatings objects pertaining to that product object
        total=0
        
        #calculating the total rating from all the ProductRating objects
        if product_rating_all:
            for prod_rate in product_rating_all:
                total += prod_rate.rating

        all_rating_count = ProfileRatings.objects.filter(product=self.object).all().count() or None
        
        if all_rating_count:
            avg_rate = float('%.2f'%float(total/all_rating_count))
            # to get only value upto two decimal point
        else:
            avg_rate = None

        context['avg_rate']=avg_rate

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  
        form = self.get_form()
        # get_form() function is from FormMixin

        print("form valid",form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            _,c_type = form.data.get("content_type").split('|')
            print(c_type.strip())
            content_type = ContentType.objects.get(model=c_type.strip())
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None
            
            if parent_id:
                parent_qs = Coment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()
            new_comment, created = Coment.objects.get_or_create(user=self.request.user,content_type=content_type,object_id=obj_id,content=content_data,parent=parent_obj)
    
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
       



# def genre_list(request,genre):
#     lookups = (Q(tag__title__iexact=genre))
#     if request.GET.get('sort'):
#         genre_list = Product.objects.filter(lookups).order_by('-'+str(request.GET.get('sort'))).distinct()
#     else:
#         genre_list = Product.objects.filter(lookups).distinct()
#     print(genre_list)
#     paginator = Paginator(genre_list,3)
#     page = request.GET.get('page', 1)
#     page_obj = paginator.page(page)
#     context = {'object_list':genre_list}
#     context['page_obj']=page_obj
#     # context['paginator']=paginator
#     context['is_baka'] = True
#     context['is_paginated'] = False
    
    # return render(request,'products/list.html', context)

def get_genre(request):
    global genre_select
    # if 'sort' in request.GET.urlencode():
    # # request.get_full_path() 
    # if 'genre' in request.get_full_path():
        # j = request.GET.urlencode()
        # print(j)
        # l,b = j.split('&')
        # i,g = l.split('=')
        # mon = str(g)
        # print(g)
    return {'get_genre':genre_select}


def update_rating(request,slug):
    rating = request.POST.get('rating')
    print(rating)
    Product.objects.filter(slug=slug).update(rating=rating)
    obj = Product.objects.filter(slug=slug).first()
    profile = Profile.objects.get(user=request.user)
    print(profile)
    ProfileRatings.objects.get_or_new(profile=profile,product=obj,rating=rating)
 
    url = obj.get_abs_url()


    return redirect(url)


 
def get_data(request,*args,**kwargs):
    one=0
    two=0
    three=0
    four=0
    five=0
    six=0
    seven=0
    eight=0
    nine=0
    ten=0
    # print(request.get_full_path())
    full_path = request.get_full_path()
    # eg. '/api/chart/data/joker/'
    path_lst = full_path.strip('/').split('/')
    # full_path.strip('/') : 'api/chart/data/joker'
    # full_path.strip('/').split('/') : ['api', 'chart', 'data', 'joker']

    product_slug = path_lst[-1] #'joker'
    # print(product_slug)
    prod_obj = Product.objects.get(slug=product_slug)
    profile_rating_obj = ProfileRatings.objects.filter(product=prod_obj)
    print(profile_rating_obj)
    for rate in profile_rating_obj:
        if rate.rating == 1:
            one +=1
        elif rate.rating == 2:
            two += 1
        elif rate.rating == 3:
            three += 1
        elif rate.rating == 4:
            four += 1
        elif rate.rating == 5:
            five += 1
        elif rate.rating == 6:
            six += 1
        elif rate.rating == 7:
            seven += 1
        elif rate.rating == 8:
            eight += 1
        elif rate.rating == 9:
            nine += 1
        elif rate.rating == 10:
            ten += 1
    # print(one,two,three,four,five,six,seven,eight,nine,ten)
    labels = ['10','9','8','7','6','5','4','3','2','1']
    default_items = [ten,nine,eight,seven,six,five,four,three,two,one]
    data = {
        "labels":labels,
        "default":default_items
    }

    return JsonResponse(data)



# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []
 
#     def get(self,request,format=None):
#         one=0
#         two=0
#         three=0
#         four=0
#         five=0
#         six=0
#         seven=0
#         eight=0
#         nine=0
#         ten=0
#         print(request.get_full_path())
#         full_path = request.get_full_path()
#         path_lst = full_path.strip('/').split('/')
#         product_slug = path_lst[-1]
#         print(product_slug)
#         prod_obj = Product.objects.get(slug=product_slug)
#         profile_rating_obj = ProfileRatings.objects.filter(product=prod_obj)
#         print(profile_rating_obj)
#         for rate in profile_rating_obj:
#             if rate.rating == 1:
#                 one +=1
#             elif rate.rating == 2:
#                 two += 1
#             elif rate.rating == 3:
#                 three += 1
#             elif rate.rating == 4:
#                 four += 1
#             elif rate.rating == 5:
#                 five += 1
#             elif rate.rating == 6:
#                 six += 1
#             elif rate.rating == 7:
#                 seven += 1
#             elif rate.rating == 8:
#                 eight += 1
#             elif rate.rating == 9:
#                 nine += 1
#             elif rate.rating == 10:
#                 ten += 1
#         print(one,two,three,four,five,six,seven,eight,nine,ten)
#         labels = ['10','9','8','7','6','5','4','3','2','1']
#         default_items = [ten,nine,eight,seven,six,five,four,three,two,one]
#         data = {
#             "labels":labels,
#             "default":default_items
#         }

#         return Response(data)








