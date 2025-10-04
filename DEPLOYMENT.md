# Deployment Guide

This guide covers deploying the Article Management API to production environments.

## Table of Contents
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Database Setup](#database-setup)
- [Production Best Practices](#production-best-practices)
- [Monitoring & Maintenance](#monitoring--maintenance)

## Pre-Deployment Checklist

Before deploying to production, ensure:

- [ ] All tests pass locally
- [ ] Environment variables configured
- [ ] Database backups configured
- [ ] SSL certificates obtained
- [ ] Domain name configured
- [ ] Monitoring tools set up
- [ ] Error tracking configured

## Environment Configuration

### 1. Create Production .env File

```bash
# Django Configuration
SECRET_KEY=<generate-strong-random-key-here>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_NAME=article_db_prod
DB_USER=article_user
DB_PASSWORD=<strong-password-here>
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# JWT Configuration
JWT_SECRET_KEY=<another-strong-random-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 2. Generate Strong Secret Keys

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## Docker Deployment

### Option 1: Docker Compose (Simple Deployment)

#### 1. Prepare the Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
```

#### 2. Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd test-technique

# Create .env file
nano .env
# (paste production configuration)

# Build and start services
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

#### 3. Set Up Nginx Reverse Proxy

Create `/etc/nginx/sites-available/article-api`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/test-technique/staticfiles/;
    }

    client_max_body_size 10M;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/article-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

### Option 2: Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
    expose:
      - 8000
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: always

  db:
    image: postgres:13-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env
    restart: always

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data
    restart: always

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - /etc/letsencrypt:/etc/letsencrypt
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  redis_data:
  static_volume:
```

Deploy with:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## Database Setup

### PostgreSQL Configuration

#### 1. Create Database and User

```sql
-- Connect to PostgreSQL
sudo -u postgres psql

-- Create database
CREATE DATABASE article_db_prod;

-- Create user
CREATE USER article_user WITH PASSWORD 'strong_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE article_db_prod TO article_user;

-- Exit
\q
```

#### 2. Configure Backups

Create backup script `/usr/local/bin/backup-db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="article_db_prod"

mkdir -p $BACKUP_DIR

docker-compose exec -T db pg_dump -U article_user $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

Make executable and add to cron:

```bash
chmod +x /usr/local/bin/backup-db.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-db.sh
```

#### 3. Restore from Backup

```bash
gunzip -c /var/backups/postgres/backup_YYYYMMDD_HHMMSS.sql.gz | \
  docker-compose exec -T db psql -U article_user article_db_prod
```

## Production Best Practices

### 1. Security

#### Update Django Settings

```python
# config/settings.py

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True
```

#### Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Performance

#### Gunicorn Configuration

Update Dockerfile CMD:

```dockerfile
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--threads", "2", \
     "--worker-class", "gthread", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
```

#### Database Connection Pooling

Add to `requirements.txt`:

```
psycopg2-binary==2.9.6
django-db-connection-pool==1.2.4
```

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10,
        }
    }
}
```

#### Redis Configuration

For production Redis, consider:

```yaml
redis:
  image: redis:6-alpine
  command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
  volumes:
    - redis_data:/data
```

### 3. Logging

#### Configure Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

## Monitoring & Maintenance

### 1. Health Checks

Set up monitoring for:

```bash
# Application health
curl https://yourdomain.com/health/

# Database connection
docker-compose exec db pg_isready

# Redis connection
docker-compose exec redis redis-cli ping
```

### 2. Log Monitoring

```bash
# View application logs
docker-compose logs -f web

# View database logs
docker-compose logs -f db

# View Redis logs
docker-compose logs -f redis

# View Nginx logs
docker-compose logs -f nginx
```

### 3. Performance Monitoring

Consider integrating:

- **Sentry** for error tracking
- **New Relic** or **DataDog** for APM
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation

### 4. Regular Maintenance

```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Clean up old images
docker system prune -a

# Check disk usage
df -h
docker system df

# Monitor resource usage
docker stats
```

### 5. Scaling

#### Horizontal Scaling

Update `docker-compose.prod.yml`:

```yaml
services:
  web:
    deploy:
      replicas: 3
    # ... rest of config
```

#### Load Balancing

Configure Nginx for load balancing:

```nginx
upstream django_app {
    least_conn;
    server web1:8000;
    server web2:8000;
    server web3:8000;
}

server {
    location / {
        proxy_pass http://django_app;
        # ... rest of config
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t

# Verify file permissions
ls -la /path/to/staticfiles/
```

#### 2. Database Connection Errors

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec web python manage.py dbshell
```

#### 3. High Memory Usage

```bash
# Check container stats
docker stats

# Restart services
docker-compose restart

# Increase memory limits in docker-compose.yml
```

#### 4. SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run

# Check certificate status
sudo certbot certificates
```

## Rollback Procedure

If deployment fails:

```bash
# 1. Stop new version
docker-compose down

# 2. Restore database backup
gunzip -c backup.sql.gz | docker-compose exec -T db psql -U user dbname

# 3. Checkout previous version
git checkout <previous-commit>

# 4. Rebuild and start
docker-compose up -d --build

# 5. Verify
curl https://yourdomain.com/health/
```

## Continuous Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /path/to/test-technique
            git pull origin main
            docker-compose down
            docker-compose up -d --build
            docker-compose exec -T web python manage.py migrate
            docker-compose exec -T web python manage.py collectstatic --noinput
```

## Summary

This deployment guide covers:

- ✅ Environment configuration
- ✅ Docker deployment options
- ✅ Database setup and backups
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Monitoring and maintenance
- ✅ Troubleshooting
- ✅ Rollback procedures
- ✅ CI/CD integration

For questions or issues, refer to the main documentation or open an issue.
