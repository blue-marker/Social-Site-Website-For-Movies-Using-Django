from django.urls import path
from .views import add_address,attach_address

urlpatterns = [
    path("add/",add_address,name="add"),
    path("attach/",attach_address,name="attach"),
]