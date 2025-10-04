# Setup & Installation Guide

This guide will help you set up and run the Article Management API on your local machine.

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)
- Postman or curl (for testing the API)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd test-technique
```

### 2. Create Environment File

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and update the values if needed. The default values should work for local development:

```env
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 3. Build and Start Services

```bash
docker-compose up --build
```

This will:
- Build the Django application container
- Start PostgreSQL database
- Start Redis cache
- Run database migrations
- Start the development server on port 8000

### 4. Create a Superuser (Optional)

In a new terminal, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### 5. Access the Application

- **API Base URL:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Health Check:** http://localhost:8000/health/

## Running Tests

### Run all tests:

```bash
docker-compose exec web pytest
```

### Run tests with coverage:

```bash
docker-compose exec web pytest --cov=. --cov-report=html
```

### Run specific test file:

```bash
docker-compose exec web pytest articles/tests.py
```

## API Testing

### Option 1: Using Postman

1. Import the `api_collection.json` file into Postman
2. Set the `base_url` variable to `http://localhost:8000`
3. Follow the authentication flow:
   - Register a user
   - Obtain a token
   - Copy the access token to the `access_token` variable
   - Test other endpoints

### Option 2: Using curl

#### Register a user:
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "editor@example.com",
    "password": "testpass123",
    "first_name": "John",
    "last_name": "Editor",
    "role": "EDITOR"
  }'
```

#### Obtain token:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "editor@example.com",
    "password": "testpass123"
  }'
```

#### Create an article (replace TOKEN with your access token):
```bash
curl -X POST http://localhost:8000/api/articles/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "content": "This is the content of my article.",
    "status": "draft"
  }'
```

#### List articles:
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/articles/
```

## Development Workflow

### View Logs

```bash
docker-compose logs -f web
```

### Access Django Shell

```bash
docker-compose exec web python manage.py shell
```

### Create Migrations

```bash
docker-compose exec web python manage.py makemigrations
```

### Apply Migrations

```bash
docker-compose exec web python manage.py migrate
```

### Collect Static Files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## Stopping the Application

```bash
docker-compose down
```

To remove volumes (database data):

```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If port 8000, 5432, or 6379 is already in use, you can change the ports in `docker-compose.yml`:

```yaml
services:
  web:
    ports:
      - "8001:8000"  # Change 8001 to any available port
```

### Database Connection Issues

If you see database connection errors:

1. Ensure PostgreSQL container is running:
   ```bash
   docker-compose ps
   ```

2. Check database logs:
   ```bash
   docker-compose logs db
   ```

3. Restart services:
   ```bash
   docker-compose restart
   ```

### Cache Issues

To clear Redis cache:

```bash
docker-compose exec redis redis-cli FLUSHALL
```

### Permission Denied Errors

On Linux, you might need to fix file permissions:

```bash
sudo chown -R $USER:$USER .
```

## Production Deployment

For production deployment:

1. **Update `.env` file:**
   - Set `DEBUG=False`
   - Use a strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` with your domain
   - Use strong database passwords

2. **Use a production-grade WSGI server:**
   The Dockerfile already includes Gunicorn

3. **Set up HTTPS:**
   Use a reverse proxy like Nginx with SSL certificates

4. **Configure database backups:**
   Set up regular PostgreSQL backups

5. **Monitor logs and errors:**
   Use tools like Sentry for error tracking

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)
- [API Documentation](./API_DOCUMENTATION.md)
