from django.shortcuts import render,reverse
from urllib.parse import quote
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

from .utils import count_words,get_read_time

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']



class PostDetailView(DetailView):
    model = Post
    # here the name of the default template is <app>/<model>_detail.html
    # so we need not define it here and just need to create the 
    # template with the same name convention 

    # in case we are not using the default name then it needs to be defined here


    # def get_context_data(self,*args,**kwargs):
    #     context = super(PostDetailView,self).get_context_data(*args,**kwargs)
    #     post = self.get_object()
    #     print(get_read_time(post.content))
    #     context['share_string'] = quote(post.content)
    #     return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','image','content']
    #here the name of the default template is <app>/<model>_form.html
    # so we need not define it here and just need to create the 
    # template with the same name convention 
    
    # in case we are not using the default name then it needs to be defined here

    # get_absolute_url method from Post model takes care of the routing after the creation of post
    # instead we can also define here 'success_url' attribute of 'get_success_url' method in class

    # def get_success_url(self):
    #     return reverse('blog-home')

    def form_valid(self, form): # overriding the default function in Create view
        form.instance.author = self.request.user
        return super().form_valid(form) #calling the original function from the super class
        # i.e inherited class CreateView
        # inshort we are incorporating the cheanges and passing it to the original class


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','image','content']
    # just like in Create View
    # here the name of the default template is <app>/<model>_form.html
    # so we need not define it here and just need to create the 
    # template with the same name convention 
    # def get_success_url(self):
    #     return reverse('blog-home')

    # get_absolute_url method from Post model takes care of the routing after the updation of post
    # instead we can also define here 'success_url' attribute of 'get_success_url' method in class

    def form_valid(self, form): # overriding the default function in Update view
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): 
#this is the default function which will be executed by mixin class UserPassesTestMixin
# here we are just overriding this function to check the required condition
        post = self.get_object() #get the instance object of the model
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # success_url = '/' this is another alternative method for get_success_url
    
    # here we haven't used the 'get_absolute_url' of Post model, sice this post will be deleted
    # instead we define here the route after the deletion of the post by the 'get_success_url'
    # same can be achieved by defining the success_url 
    def get_success_url(self):
        return reverse('blog-home')


    # here the name of the default template is <app>/<model>_confirm_delete.html
    # so we need not define it here and just need to create the 
    # template with the same name convention 

    # in case we are not using the default name then it needs to be defined here

        
    def test_func(self):
        post = self.get_object() # in-built function to grab the object
        if self.request.user == post.author:
            return True
        return False
