from django.urls import path
from .views import (
    comment_thread,
)

urlpatterns = [
    path('<int:id>/', comment_thread, name='thread'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]