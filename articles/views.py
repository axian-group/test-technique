from rest_framework import generics, status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Article
from .serializers import ArticleSerializer, ArticleListSerializer
from .permissions import ArticlePermission


class ArticleListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating articles.
    List view is cached for performance.
    """
    permission_classes = [ArticlePermission]
    
    def get_serializer_class(self):
        """Use different serializers for list and create."""
        if self.request.method == 'GET':
            return ArticleListSerializer
        return ArticleSerializer
    
    def get_queryset(self):
        """
        Return articles based on user role and filters.
        - Admin: All articles
        - Editor: All articles (can read all, modify own)
        - Reader: All articles (read-only)
        """
        queryset = Article.objects.select_related('author').all()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """List articles with caching."""
        # Create cache key based on query parameters and user
        status_filter = request.query_params.get('status', 'all')
        page = request.query_params.get('page', '1')
        cache_key = f'articles_list_{status_filter}_page_{page}'
        
        # Try to get from cache
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)
        
        # If not in cache, get from database
        response = super().list(request, *args, **kwargs)
        
        # Cache the response
        cache.set(cache_key, response.data, settings.CACHE_TTL)
        
        return response
    
    def perform_create(self, serializer):
        """Create article and invalidate cache."""
        serializer.save()
        # Invalidate cache when new article is created
        self._invalidate_cache()
    
    def _invalidate_cache(self):
        """Invalidate all article list cache."""
        # In production, use a more sophisticated cache invalidation strategy
        cache.delete_pattern('articles_list_*')


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific article.
    """
    queryset = Article.objects.select_related('author').all()
    serializer_class = ArticleSerializer
    permission_classes = [ArticlePermission]
    
    def perform_update(self, serializer):
        """Update article and invalidate cache."""
        serializer.save()
        self._invalidate_cache()
    
    def perform_destroy(self, instance):
        """Delete article and invalidate cache."""
        instance.delete()
        self._invalidate_cache()
    
    def _invalidate_cache(self):
        """Invalidate all article list cache."""
        cache.delete_pattern('articles_list_*')
