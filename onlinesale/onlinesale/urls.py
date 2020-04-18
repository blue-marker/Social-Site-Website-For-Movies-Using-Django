"""onlinesale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home_page,about_page,contact_page
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register_page, signin_page, signout_page
from django.conf.urls import include
from search.views import SearchProductListView
from profiles.views import Profile
from products.views import get_data
urlpatterns = [
    path("product/", include(('products.urls','products'),namespace="product")),
    path("actor/", include(('actors.urls','actors'),namespace="actor")),
    path("cart/", include(('carts.urls', 'carts'), namespace="cart")),
    path("watchlist/", include(('watchlists.urls', 'watchlists'), namespace="watchlist")),
    path("coment/", include(('coments.urls', 'coments'), namespace="comment")),
    path("", include('blog.urls')),
    path('admin/', admin.site.urls),
    path("",home_page, name="home"),
    path("about/",about_page, name ="about"),
    path("profile/", include(('profiles.urls', 'profiles'), namespace="profile")),
    path("contact/",contact_page,name ="contact"),
    path("register/",register_page,name ="register"),
    path("signin/",signin_page,name ="signin"),
    path("signout/",signout_page,name ="signout"),
    path("search/", SearchProductListView.as_view(), name="search"),
    path("order/", include(('orders.urls','orders'),namespace="order")),
    path("addresses/", include(('addresses.urls','addresses'),namespace="address")),
    path("api/chart/data/<str:path>/",get_data,name="chart"),
]

# below is the code for serving files uploaded by a user during development
# since the below code is only for development we are allowing this code to
# execute only when debug mode is on

# here we are just routing the media and static files in our list of urls

if settings.DEBUG: 
    urlpatterns = urlpatterns + static(settings.STATIC_URL,
    document_root= settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT)

# so basically what we are doing is this:
# we are adding the path of static and media file in the urlpattern 
# only when we are the debug mode ( for production we will use different strategy )

# and we are doing this to route paths for the static and media files to be served


