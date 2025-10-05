from django.urls import path
from .views import ArticleListCreateView, ArticleRetrieveUpdateDestroyView

urlpatterns = [
    path('articles/', ArticleListCreateView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleRetrieveUpdateDestroyView.as_view(), name='article-detail'),
]
