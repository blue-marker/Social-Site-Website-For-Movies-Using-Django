from django.urls import path
from .views import create_order,received_payment

urlpatterns = [
    path("",create_order, name ="create"),
    path("payment",received_payment, name ="payment"),
]