"""
Tests for the articles app.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Article

User = get_user_model()


@pytest.mark.django_db
class TestArticleModel:
    """Test Article model."""
    
    def test_create_article(self, editor_user):
        """Test creating an article."""
        article = Article.objects.create(
            title='Test Article',
            content='Test content',
            status=Article.Status.DRAFT,
            author=editor_user
        )
        
        assert article.title == 'Test Article'
        assert article.content == 'Test content'
        assert article.status == Article.Status.DRAFT
        assert article.author == editor_user
        assert article.published_at is None
    
    def test_article_published_at_auto_set(self, editor_user):
        """Test that published_at is set automatically when status is published."""
        article = Article.objects.create(
            title='Test Article',
            content='Test content',
            status=Article.Status.PUBLISHED,
            author=editor_user
        )
        
        assert article.published_at is not None


@pytest.mark.django_db
class TestArticleListAPI:
    """Test article list API endpoint."""
    
    def test_list_articles_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot list articles."""
        url = reverse('articles:article-list-create')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_articles_authenticated(self, api_client, editor_user):
        """Test listing articles as authenticated user."""
        # Create test articles
        Article.objects.create(
            title='Article 1',
            content='Content 1',
            status=Article.Status.PUBLISHED,
            author=editor_user
        )
        Article.objects.create(
            title='Article 2',
            content='Content 2',
            status=Article.Status.DRAFT,
            author=editor_user
        )
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('articles:article-list-create')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_filter_articles_by_status(self, api_client, editor_user):
        """Test filtering articles by status."""
        Article.objects.create(
            title='Published Article',
            content='Content',
            status=Article.Status.PUBLISHED,
            author=editor_user
        )
        Article.objects.create(
            title='Draft Article',
            content='Content',
            status=Article.Status.DRAFT,
            author=editor_user
        )
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('articles:article-list-create')
        response = api_client.get(url, {'status': 'published'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Published Article'


@pytest.mark.django_db
class TestArticleCreateAPI:
    """Test article creation API endpoint."""
    
    def test_create_article_as_editor(self, api_client, editor_user):
        """Test that editors can create articles."""
        api_client.force_authenticate(user=editor_user)
        url = reverse('articles:article-list-create')
        
        data = {
            'title': 'New Article',
            'content': 'Article content',
            'status': 'draft'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Article'
        assert response.data['author']['email'] == editor_user.email
    
    def test_create_article_as_reader(self, api_client, reader_user):
        """Test that readers cannot create articles."""
        api_client.force_authenticate(user=reader_user)
        url = reverse('articles:article-list-create')
        
        data = {
            'title': 'New Article',
            'content': 'Article content',
            'status': 'draft'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestArticleUpdateAPI:
    """Test article update API endpoint."""
    
    def test_editor_can_update_own_article(self, api_client, editor_user):
        """Test that editors can update their own articles."""
        article = Article.objects.create(
            title='Original Title',
            content='Original content',
            status=Article.Status.DRAFT,
            author=editor_user
        )
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('articles:article-detail', kwargs={'pk': article.pk})
        
        data = {
            'title': 'Updated Title',
            'content': 'Updated content',
            'status': 'published'
        }
        
        response = api_client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
    
    def test_editor_cannot_update_others_article(self, api_client, editor_user, admin_user):
        """Test that editors cannot update articles by other users."""
        article = Article.objects.create(
            title='Admin Article',
            content='Content',
            status=Article.Status.DRAFT,
            author=admin_user
        )
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('articles:article-detail', kwargs={'pk': article.pk})
        
        data = {
            'title': 'Hacked Title',
            'content': 'Hacked content',
            'status': 'published'
        }
        
        response = api_client.put(url, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_admin_can_update_any_article(self, api_client, admin_user, editor_user):
        """Test that admins can update any article."""
        article = Article.objects.create(
            title='Editor Article',
            content='Content',
            status=Article.Status.DRAFT,
            author=editor_user
        )
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('articles:article-detail', kwargs={'pk': article.pk})
        
        data = {
            'title': 'Admin Updated',
            'content': 'Admin content',
            'status': 'published'
        }
        
        response = api_client.put(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Admin Updated'


@pytest.mark.django_db
class TestArticleDeleteAPI:
    """Test article deletion API endpoint."""
    
    def test_editor_can_delete_own_article(self, api_client, editor_user):
        """Test that editors can delete their own articles."""
        article = Article.objects.create(
            title='To Delete',
            content='Content',
            status=Article.Status.DRAFT,
            author=editor_user
        )
        
        api_client.force_authenticate(user=editor_user)
        url = reverse('articles:article-detail', kwargs={'pk': article.pk})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Article.objects.filter(pk=article.pk).exists()
    
    def test_reader_cannot_delete_article(self, api_client, reader_user, editor_user):
        """Test that readers cannot delete articles."""
        article = Article.objects.create(
            title='Article',
            content='Content',
            status=Article.Status.PUBLISHED,
            author=editor_user
        )
        
        api_client.force_authenticate(user=reader_user)
        url = reverse('articles:article-detail', kwargs={'pk': article.pk})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Article.objects.filter(pk=article.pk).exists()
