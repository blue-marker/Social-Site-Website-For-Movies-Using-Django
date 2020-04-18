from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView

from .forms import UserUpdateForm,ProfileUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required

from django.views.generic import DetailView

class ProfileView(DetailView):
    model = Profile
    template_name = 'profiles/profile.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'profile'



# @login_required
# def profile(request,slug):

#     u_form = UserUpdateForm(instance=request.user)
#     p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#     	}

#     return	render(request,'profiles/profile.html', context)


@login_required
def profile_update(request,slug):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile:profile',slug=slug)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    	}

    return	render(request,'profiles/profile_form.html', context)


# class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Profile
#     fields = ['title', 'content']

    
#     # template_name = profile/profile_form.html                #<app>/<model>_form.html
#     # def form_valid(self, form): # overriding the default function in Update view
#     #     form.instance.author = self.request.user
#     #     return super().form_valid(form)

#     def test_func(self): 
#         profile = self.get_object()
#         if self.request.user == profile.user:
#             return True
#         return False