from django.shortcuts import render, redirect

from products.models import Product
from .models import Watchlist


def watchlist_home(request):
    watchlist_obj = Watchlist.objects.get_or_new(request)
    context = {'watchlist_obj':watchlist_obj}
    return render(request,'watchlists/list.html',context)

#this function is the business logic for button in cart
def update_watchlist(request):
    watchlist_obj = Watchlist.objects.get_or_new(request) #get the new or existing cart object

    if request.method == 'POST':
        #extracting details
        prodid = request.POST.get('prodid')   
   
        if prodid:
            prod_obj = Product.objects.filter(id=prodid).first()

            # if prodquant > prod_obj.quantity:
            #     return redirect( prod_obj.get_abs_url() )    
         
            if prod_obj in watchlist_obj.products.all():
                watchlist_obj.products.remove(prod_obj)
            else:
                watchlist_obj.products.add(prod_obj)

    return redirect('watchlist:list')
