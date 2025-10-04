from django.urls import path
from .views import (
    UserCreateView,
    UserRetrieveUpdateView,
    UserListView,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('me/', UserRetrieveUpdateView.as_view(), name='user-me'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserRetrieveUpdateView.as_view(), name='user-detail'),
]
