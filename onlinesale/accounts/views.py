from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, SignInForm
# from django.contrib.auth.models import User

from django.utils.http import is_safe_url

from django.contrib.auth import get_user_model
User = get_user_model()



def signout_page(request):
    logout(request)
    return redirect("/")
#this redirects us to home url

def signin_page(request):
	signinform    = SignInForm(request.POST or None)
	redirect_path = request.POST.get('next' or None)
	
	context = {
        'signinform':signinform,
    }
	
	if signinform.is_valid():	
		user = authenticate(username=signinform.data.get('email'), password=signinform.data.get('pwd'))
# Use authenticate() to verify a set of credentials. It takes credentials as keyword arguments, username and password for the default case, checks them against each authentication backend, and returns a User object if the credentials are valid for a backend. If the credentials aren’t valid for any backend or if a backend raises PermissionDenied, it returns None. - from django doc
#note here we are passing the email info in username parameter of authenticate function
		if user:
# A backend authenticated the credentials
			login(request,user)

			if redirect_path is not None:
				if is_safe_url(redirect_path,request.get_host()):
					return redirect(redirect_path)
            #return redirect("/")
# get_host() Returns the originating host of the request using information from the HTTP_X_FORWARDED_HOST (if USE_X_FORWARDED_HOST is enabled) and HTTP_HOST headers, in that order
# Example: "127.0.0.1:8000"
			return redirect("home")
		else:
# No backend authenticated the credentials
			messages.error(request,f'Invalid Credentials')
			# context['errMsg'] = "Invalid Credentials"
	
	return render(request, "accounts/login.html", context)



def register_page(request):

	if request.method == "POST":
		form = RegisterForm(request.POST)
	else:
		form = RegisterForm() 
# the page is accessed at GET request hence the else part will be 
# rendered first by default

#when the submit button is hit, POST request is generated and 
#the first part of the condition is rendered i.e Registered form with data

      #OR we can do this , which does the same thing

    # form = RegisterForm(request.POST or None)

	context = {'form':form}
	
	if form.is_valid():
#for password clean_data will treat special characters as none
#hence we are using data
		email = form.data.get('email') 
# if cleaned_data method is used then @ is removed from the extracted value, 
# which in turn will contradict with the email field in User's class, thus giving a 'ValueError'

# we can use either 'cleaned_data' or 'data' method on form 
# to extract the raw values of html name from the front end (i.e register.html) 

# but if we use 'cleaned data' special charac gets erased 
# hence to avoid that case in emails and passwords we are using 'data' method which is safe

		fn = form.data.get('fullname')
		mobile = form.data.get('mobile')
		pwd = form.data.get('pwd')
		user = User.objects.create_user(email=email, password=pwd, full_name=fn, mobile=mobile)
		#saved user object is returned which we store it in user variable
	
# The primary attributes of the default user are: username, password, email, first_name, last_name
# The most direct way to create users is to use the included 'create_user()' helper function:

		if user:
			messages.success(request,f'User Has Been create Successfully You are now able to log in')
			# context['msg'] = "User Has Been create Successfully"
			context['form']= RegisterForm()
		else:
			messages.error(request,f'Something went wrong please try again')
			# context['msg'] = "Something went wrong please try again"

	return render(request,"accounts/register.html",context)

