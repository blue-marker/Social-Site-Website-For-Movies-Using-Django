from django.shortcuts import render

from .models import Actor
from django.views.generic import ListView, DetailView

from django.db.models import Q
from django.core.paginator import Paginator

class ActorListView(ListView):
    paginate_by = 6
    model = Actor
    template_name = "actors/list.html"
    ordering =['rating']



    def get_context_data(self,*args,**kwargs):
        context = super(ActorListView, self).get_context_data(*args,**kwargs)

        if self.request.GET.get('rating') :
            lookups = (Q(rating__iexact=self.request.GET.get('rating' or None)))
            actorList=Actor.objects.filter(lookups).distinct().order_by('-'+str(self.request.GET.get('sort')))
            paginator,page,object_list,is_paginated = self.paginate_queryset(actorList,3)
            context['object_list']=object_list
            context['page_obj']  = page
            context['paginator'] = paginator
            context['is_paginated'] = is_paginated
            context['is_baka'] = True
            print(context) 
            return context
             
        return context

class ActorDetailView(DetailView):
    model = Actor
    template_name = "actors/detail.html" 
    








