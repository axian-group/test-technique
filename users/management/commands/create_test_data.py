"""
Django management command to create test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users and articles'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Create users
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'password': 'pbkdf2_sha256$600000$test',
                'role': User.Role.ADMIN,
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user: {admin.email}'))
        else:
            self.stdout.write(f'  Admin user already exists: {admin.email}')
        
        editor, created = User.objects.get_or_create(
            email='editor@example.com',
            defaults={
                'role': User.Role.EDITOR,
                'first_name': 'Editor',
                'last_name': 'User'
            }
        )
        if created:
            editor.set_password('editor123')
            editor.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created editor user: {editor.email}'))
        else:
            self.stdout.write(f'  Editor user already exists: {editor.email}')
        
        reader, created = User.objects.get_or_create(
            email='reader@example.com',
            defaults={
                'role': User.Role.READER,
                'first_name': 'Reader',
                'last_name': 'User'
            }
        )
        if created:
            reader.set_password('reader123')
            reader.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created reader user: {reader.email}'))
        else:
            self.stdout.write(f'  Reader user already exists: {reader.email}')
        
        # Create articles
        articles_data = [
            {
                'title': 'Getting Started with Django',
                'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.',
                'status': Article.Status.PUBLISHED,
                'author': editor
            },
            {
                'title': 'REST API Best Practices',
                'content': 'Building robust REST APIs requires careful consideration of design patterns, security, and performance.',
                'status': Article.Status.PUBLISHED,
                'author': editor
            },
            {
                'title': 'Docker for Beginners',
                'content': 'Docker is a containerization platform that simplifies application deployment and scaling.',
                'status': Article.Status.DRAFT,
                'author': editor
            },
            {
                'title': 'PostgreSQL Performance Tips',
                'content': 'Optimizing PostgreSQL queries can significantly improve your application performance.',
                'status': Article.Status.PUBLISHED,
                'author': admin
            },
            {
                'title': 'Redis Caching Strategies',
                'content': 'Implementing effective caching strategies with Redis can reduce database load and improve response times.',
                'status': Article.Status.ARCHIVED,
                'author': admin
            },
        ]
        
        for data in articles_data:
            article, created = Article.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created article: {article.title} ({article.status})'))
            else:
                self.stdout.write(f'  Article already exists: {article.title}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test data created successfully!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  Admin:  admin@example.com / admin123')
        self.stdout.write('  Editor: editor@example.com / editor123')
        self.stdout.write('  Reader: reader@example.com / reader123')
