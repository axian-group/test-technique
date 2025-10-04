# Article Management API - Implementation Documentation

## 📋 Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Features Implemented](#features-implemented)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)

## Overview

This is a complete REST API implementation for an article management system built with Django 4.2 and Django REST Framework. The system includes JWT authentication, role-based permissions, Redis caching, and comprehensive test coverage.

### Tech Stack
- **Backend:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL 13
- **Cache:** Redis 6
- **Authentication:** JWT (Simple JWT)
- **Containerization:** Docker + Docker Compose
- **Testing:** Pytest + Factory Boy

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone and navigate to the project:**
```bash
cd test-technique
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Build and start services:**
```bash
docker-compose up --build
```

4. **Create test data (optional):**
```bash
docker-compose exec web python scripts/create_test_data.py
```

The API will be available at `http://localhost:8000`

### Test Credentials

After running the test data script:
- **Admin:** admin@example.com / admin123
- **Editor:** editor@example.com / editor123
- **Reader:** reader@example.com / reader123

## Architecture

### Project Structure
```
test-technique/
├── config/                 # Django project configuration
│   ├── settings.py        # Main settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── users/                  # User management app
│   ├── models.py          # Custom User model with roles
│   ├── serializers.py     # User serializers
│   ├── views.py           # User views
│   ├── urls.py            # User URL patterns
│   ├── admin.py           # Admin configuration
│   ├── tests.py           # User tests
│   └── management/        # Management commands
│       └── commands/
│           └── wait_for_db.py
├── articles/               # Article management app
│   ├── models.py          # Article model
│   ├── serializers.py     # Article serializers
│   ├── views.py           # Article views with caching
│   ├── permissions.py     # Custom permissions
│   ├── urls.py            # Article URL patterns
│   ├── admin.py           # Admin configuration
│   └── tests.py           # Article tests
├── scripts/                # Utility scripts
│   └── create_test_data.py
├── docker-compose.yml      # Docker services configuration
├── Dockerfile              # Application container
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── conftest.py             # Pytest fixtures
├── Makefile                # Convenient commands
├── .env.example            # Environment variables template
├── .dockerignore           # Docker ignore file
├── API_DOCUMENTATION.md    # Detailed API documentation
└── SETUP.md                # Setup and installation guide
```

### Database Schema

#### User Model
- `id`: Primary key
- `email`: Unique email (used for authentication)
- `password`: Hashed password
- `first_name`: User's first name
- `last_name`: User's last name
- `role`: User role (ADMIN, EDITOR, READER)
- `is_active`: Account status
- `is_staff`: Staff status
- `is_superuser`: Superuser status
- `date_joined`: Registration date
- `last_login`: Last login timestamp

#### Article Model
- `id`: Primary key
- `title`: Article title (max 200 chars)
- `content`: Article content (text)
- `status`: Publication status (draft, published, archived)
- `author`: Foreign key to User
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `published_at`: Publication timestamp (nullable)

## Features Implemented

### ✅ Authentication & Authorization
- JWT-based authentication using `djangorestframework-simplejwt`
- Three user roles: Admin, Editor, Reader
- Custom permission classes for role-based access control
- Token refresh mechanism
- Secure password hashing

### ✅ User Management
- Custom User model with email as username
- User registration endpoint
- User profile management
- Admin user list view

### ✅ Article Management
- Full CRUD operations on articles
- Pagination (10 items per page)
- Status filtering (draft, published, archived)
- Automatic `published_at` timestamp on status change
- Author assignment on creation

### ✅ Permissions System

| Action | Admin | Editor | Reader |
|--------|-------|--------|--------|
| Create Article | ✅ | ✅ | ❌ |
| Read All Articles | ✅ | ✅ | ✅ |
| Update Own Article | ✅ | ✅ | ❌ |
| Update Any Article | ✅ | ❌ | ❌ |
| Delete Own Article | ✅ | ✅ | ❌ |
| Delete Any Article | ✅ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |

### ✅ Caching
- Redis-based caching for article list endpoint
- 15-minute cache TTL
- Automatic cache invalidation on create/update/delete
- Cache keys include query parameters for accurate caching

### ✅ Infrastructure
- Docker containerization
- Docker Compose orchestration
- PostgreSQL database with health checks
- Redis cache with health checks
- Environment-based configuration
- Database connection retry logic

### ✅ Testing
- Comprehensive test suite using pytest
- 15+ test cases covering:
  - User model and authentication
  - Article CRUD operations
  - Permission enforcement
  - Status filtering
  - Role-based access control
- Test fixtures for different user roles
- Factory pattern for test data

### ✅ Documentation
- Detailed API documentation
- Setup and installation guide
- Postman collection for API testing
- Inline code comments
- Type hints where applicable

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

### Users
- `POST /api/users/register/` - Register new user
- `GET /api/users/me/` - Get current user profile
- `GET /api/users/` - List all users (Admin only)
- `GET /api/users/{id}/` - Get user by ID (Admin only)

### Articles
- `GET /api/articles/` - List articles (paginated, cached)
- `GET /api/articles/?status=published` - Filter by status
- `POST /api/articles/` - Create article
- `GET /api/articles/{id}/` - Get article detail
- `PUT /api/articles/{id}/` - Update article
- `DELETE /api/articles/{id}/` - Delete article

### Health Check
- `GET /health/` - Service health check

For detailed API documentation with examples, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## Testing

### Run All Tests
```bash
make test
# or
docker-compose exec web pytest
```

### Run with Coverage
```bash
make test-coverage
# or
docker-compose exec web pytest --cov=. --cov-report=html
```

### Run Specific Tests
```bash
docker-compose exec web pytest articles/tests.py
docker-compose exec web pytest users/tests.py
```

### Test Coverage
The test suite covers:
- ✅ User model creation and validation
- ✅ User authentication (JWT)
- ✅ Article model and auto-timestamps
- ✅ Article list and filtering
- ✅ Article creation with permissions
- ✅ Article update with ownership checks
- ✅ Article deletion with permissions
- ✅ Permission enforcement for all roles

## Deployment

### Development
```bash
docker-compose up
```

### Production Considerations

1. **Environment Variables:**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`
   - Use secure database passwords

2. **Database:**
   - Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
   - Set up regular backups
   - Configure connection pooling

3. **Cache:**
   - Use managed Redis service (AWS ElastiCache, Redis Cloud)
   - Configure persistence if needed

4. **Web Server:**
   - Use Gunicorn (already configured)
   - Set up Nginx as reverse proxy
   - Configure SSL/TLS certificates

5. **Static Files:**
   - Collect static files: `python manage.py collectstatic`
   - Serve via CDN or Nginx

6. **Monitoring:**
   - Set up error tracking (Sentry)
   - Configure logging
   - Monitor performance metrics

7. **Security:**
   - Enable HTTPS only
   - Configure CORS properly
   - Set security headers
   - Regular security updates

### Deployment Commands

```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Useful Commands

The project includes a Makefile for convenience:

```bash
make help              # Show available commands
make build             # Build Docker containers
make up                # Start services
make down              # Stop services
make logs              # View logs
make shell             # Access Django shell
make test              # Run tests
make migrate           # Run migrations
make makemigrations    # Create migrations
make createsuperuser   # Create superuser
make test-data         # Create test data
make clean             # Remove containers and volumes
```

## Design Decisions

### 1. Custom User Model
- Used email as the primary identifier instead of username
- More modern and user-friendly approach
- Easier for users to remember

### 2. Role-Based Permissions
- Implemented custom permission class for fine-grained control
- Separates concerns between authentication and authorization
- Easy to extend with new roles

### 3. Caching Strategy
- Cache at the view level for flexibility
- Include query parameters in cache key
- Automatic invalidation on data changes
- 15-minute TTL balances freshness and performance

### 4. Testing Approach
- Used pytest for better fixtures and parametrization
- Separated fixtures in conftest.py for reusability
- Focused on critical paths and edge cases

### 5. Docker Setup
- Multi-service architecture for scalability
- Health checks for reliability
- Volume persistence for data
- Environment-based configuration

## Security Features

- ✅ JWT token-based authentication
- ✅ Password hashing with Django's default hasher
- ✅ CORS configuration
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection (Django templates)
- ✅ CSRF protection
- ✅ Environment variable configuration
- ✅ Non-root user in Docker container

## Performance Optimizations

- ✅ Redis caching for frequently accessed data
- ✅ Database indexing on frequently queried fields
- ✅ `select_related` for foreign key optimization
- ✅ Pagination to limit response size
- ✅ Lightweight serializers for list views

## Future Enhancements

- [ ] Elasticsearch for full-text search
- [ ] Celery for background tasks
- [ ] WebSocket support for real-time updates
- [ ] Rate limiting
- [ ] API versioning
- [ ] GraphQL endpoint
- [ ] File upload for article images
- [ ] Article tags and categories
- [ ] Comment system
- [ ] Email notifications

## Support

For issues or questions:
1. Check the [SETUP.md](./SETUP.md) guide
2. Review the [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
3. Check Docker logs: `docker-compose logs`
4. Open an issue on the repository

## License

This project is part of a technical assessment.
