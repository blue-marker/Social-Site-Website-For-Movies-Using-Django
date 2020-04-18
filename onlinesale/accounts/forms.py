from django import forms
from django.forms import ValidationError
# from django.contrib.auth.models import User

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth import get_user_model
User = get_user_model()


#this is the sign in form to be rendered in fron-end
class SignInForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    pwd = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

#this is the sign up or registration form to be rendered in fron-end
class RegisterForm(forms.Form):
	email = forms.EmailField(label="",widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
	fullname = forms.CharField(label="",widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}))
	mobile = forms.IntegerField(label="",widget = forms.NumberInput(attrs={'class':'form-control','placeholder':'Mobile No'}))
	pwd = forms.CharField(label="",widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Password'}))
	cpwd = forms.CharField(label="",widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Password'}))
    
    #overwriting the clean function defined in class Form 
	def clean(self):
		if self.cleaned_data.get('pwd') != self.cleaned_data.get('cpwd'):
			raise ValidationError("Both passwords don't match ")
		return self.cleaned_data

	def clean_email(self):
		if User.objects.filter(email__exact = self.cleaned_data.get('email')).exists():
			raise ValidationError("Email already in use")
		return self.cleaned_data.get('Email')



#we are using this in admin file
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
# we are adding the password and it's confirmation field here in
# addition to the existing fields in user described in the list below
    class Meta:
        model = User
        fields = ('email', 'full_name', 'mobile')
        #including the existing fields in User model which we want to be rendered"

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

#below we are overwriting the save method from ModelForm class
    def save(self, commit=True,*args,**kwargs):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False,*args,**kwargs)
# here we are calling save method of parent class i.e ModelForm 
# we are passing arguement 'commit=False' into the method so that the object returned
# by the method is an unsaved user object (it will return any object of the class passed into the model in Meta)

#below we are adding the password into the user and then saving it into the database
        user.set_password(self.cleaned_data["password1"])
        # 'set_password' Sets the user’s password to the given raw string, taking care of the password hashing. Doesn’t save the User object.
        if commit:
            user.save()
        return user

#we are using this in admin file
class UserAdminChangeForm(forms.ModelForm):
    """ A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field. """
    
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'full_name', 'mobile','staff')
    
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]




		