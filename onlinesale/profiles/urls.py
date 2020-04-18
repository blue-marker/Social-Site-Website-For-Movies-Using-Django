from django.urls import path
from .views import profile_update,ProfileView

urlpatterns = [
    # path('<slug:slug>/', profile, name='profile'),
    path('<slug:slug>/',ProfileView.as_view(), name='profile'),
    path('<slug:slug>/update/', profile_update, name='update'),
    
]