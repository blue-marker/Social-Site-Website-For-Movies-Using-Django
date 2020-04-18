from django.urls import path
from .views import update_watchlist, watchlist_home

urlpatterns = [
    path("list/", watchlist_home, name="list"),
    path("update/", update_watchlist, name="update"),
]
