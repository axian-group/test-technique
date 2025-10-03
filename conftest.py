"""
Pytest configuration and fixtures.
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    return User.objects.create_user(
        email='admin@example.com',
        password='testpass123',
        role=User.Role.ADMIN,
        first_name='Admin',
        last_name='User'
    )


@pytest.fixture
def editor_user(db):
    """Create and return an editor user."""
    return User.objects.create_user(
        email='editor@example.com',
        password='testpass123',
        role=User.Role.EDITOR,
        first_name='Editor',
        last_name='User'
    )


@pytest.fixture
def reader_user(db):
    """Create and return a reader user."""
    return User.objects.create_user(
        email='reader@example.com',
        password='testpass123',
        role=User.Role.READER,
        first_name='Reader',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(api_client, editor_user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=editor_user)
    return api_client
