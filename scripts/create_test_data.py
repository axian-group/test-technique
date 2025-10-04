"""
Script to create test data for the application.
Run with: docker-compose exec web python scripts/create_test_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()

def create_test_data():
    """Create test users and articles."""
    
    # Create users
    admin = User.objects.create_user(
        email='admin@example.com',
        password='admin123',
        role=User.Role.ADMIN,
        first_name='Admin',
        last_name='User'
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f'✓ Created admin user: {admin.email}')
    
    editor = User.objects.create_user(
        email='editor@example.com',
        password='editor123',
        role=User.Role.EDITOR,
        first_name='Editor',
        last_name='User'
    )
    print(f'✓ Created editor user: {editor.email}')
    
    reader = User.objects.create_user(
        email='reader@example.com',
        password='reader123',
        role=User.Role.READER,
        first_name='Reader',
        last_name='User'
    )
    print(f'✓ Created reader user: {reader.email}')
    
    # Create articles
    articles_data = [
        {
            'title': 'Getting Started with Django',
            'content': 'Django is a high-level Python web framework...',
            'status': Article.Status.PUBLISHED,
            'author': editor
        },
        {
            'title': 'REST API Best Practices',
            'content': 'Building robust REST APIs requires...',
            'status': Article.Status.PUBLISHED,
            'author': editor
        },
        {
            'title': 'Docker for Beginners',
            'content': 'Docker is a containerization platform...',
            'status': Article.Status.DRAFT,
            'author': editor
        },
        {
            'title': 'PostgreSQL Performance Tips',
            'content': 'Optimizing PostgreSQL queries...',
            'status': Article.Status.PUBLISHED,
            'author': admin
        },
        {
            'title': 'Redis Caching Strategies',
            'content': 'Implementing effective caching...',
            'status': Article.Status.ARCHIVED,
            'author': admin
        },
    ]
    
    for data in articles_data:
        article = Article.objects.create(**data)
        print(f'✓ Created article: {article.title} ({article.status})')
    
    print('\n✅ Test data created successfully!')
    print('\nTest credentials:')
    print('  Admin:  admin@example.com / admin123')
    print('  Editor: editor@example.com / editor123')
    print('  Reader: reader@example.com / reader123')

if __name__ == '__main__':
    create_test_data()
