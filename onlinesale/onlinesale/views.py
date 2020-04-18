from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    context={'head':'Home Page',
    'content':'Welcome to Itvedant Education Private Limited'}
    return render(request,"home.html",context)

def about_page(request):
    context={'head':'About Page'}
    context['content']="""
    What is Django?
Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. Built by experienced developers, Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It is free and open source, has a thriving and active community, great documentation, and many options for free and paid-for support. 
Django uses a component-based “shared-nothing” architecture (each part of the architecture is independent of the others, and can hence be replaced or changed if needed). Having a clear separation between the different parts means that it can scale for increased traffic by adding hardware at any level: caching servers, database servers, or application servers. Some of the busiest sites have successfully scaled Django to meet their demands (e.g. Instagram and Disqus, to name just two).
Maintainable
Django has continued to grow and improve, from its first milestone release (1.0) in September 2008 through to the recently-released version 2.0 (2017). Each release has added new functionality and bug fixes, ranging from support for new types of databases, template engines, and caching, through to the addition of "generic" view functions and classes (which reduce the amount of code that developers have to write for a number of programming tasks).
      """
    return render(request,"home.html",context) 


def contact_page(request):
    context={'head':'Contact Page',
    'content':'You can contact us on mobile No:-9769421923,9819611983'}
    return render(request,"home.html",context)