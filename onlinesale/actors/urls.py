from django.urls import path
from .views import ActorListView,ActorDetailView

urlpatterns = [
    path("",ActorListView.as_view(),name="lists"),
    path("<slug:slug>/",ActorDetailView.as_view(),name="details"),

]