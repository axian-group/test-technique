from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='author'
    )

    class Meta:
        model = Article
        fields = ["id", "title", "content", "status", "author", "author_id", "created_at", "updated_at", "published_at"]
