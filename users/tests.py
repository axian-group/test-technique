"""
Tests for the users app.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""
    
    def test_create_user_with_email(self):
        """Test creating a user with email."""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(
            email=email,
            password=password
        )
        
        assert user.email == email
        assert user.check_password(password)
        assert user.role == User.Role.READER
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'admin@example.com'
        password = 'testpass123'
        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        
        assert user.email == email
        assert user.is_superuser
        assert user.is_staff
        assert user.role == User.Role.ADMIN


@pytest.mark.django_db
class TestUserRegistrationAPI:
    """Test user registration API."""
    
    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        url = reverse('users:user-register')
        data = {
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'READER'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'newuser@example.com'
        assert 'password' not in response.data
    
    def test_register_user_invalid_email(self, api_client):
        """Test registration with invalid email."""
        url = reverse('users:user-register')
        data = {
            'email': 'invalid-email',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserAuthenticationAPI:
    """Test user authentication API."""
    
    def test_obtain_token_success(self, api_client, editor_user):
        """Test obtaining JWT token."""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'editor@example.com',
            'password': 'testpass123'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_obtain_token_invalid_credentials(self, api_client):
        """Test obtaining token with invalid credentials."""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
