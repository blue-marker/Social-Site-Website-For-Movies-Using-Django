from django import forms
from django.forms import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_name','email','mobile']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','about_me']