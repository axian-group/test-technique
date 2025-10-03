from rest_framework import serializers
from .models import Article
from users.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""
    
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'content',
            'status',
            'author',
            'author_id',
            'created_at',
            'updated_at',
            'published_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'published_at')
    
    def create(self, validated_data):
        """Create article with the current user as author."""
        # Remove author_id if present, we'll use request.user
        validated_data.pop('author_id', None)
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class ArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for article list view."""
    
    author_email = serializers.EmailField(source='author.email', read_only=True)
    
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'status',
            'author_email',
            'created_at',
            'published_at'
        )
