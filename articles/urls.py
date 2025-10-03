from django.urls import path
from .views import (
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
)

app_name = 'articles'

urlpatterns = [
    path('', ArticleListCreateView.as_view(), name='article-list-create'),
    path('<int:pk>/', ArticleRetrieveUpdateDestroyView.as_view(), name='article-detail'),
]
