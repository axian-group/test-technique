# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Setup Environment
```bash
cp .env.example .env
```

### Step 2: Start Services
```bash
docker-compose up --build
```

Wait for the message: `Database available!` and the server to start.

### Step 3: Create Test Data (Optional)
In a new terminal:
```bash
docker-compose exec web python scripts/create_test_data.py
```

## 🎯 Test the API

### Get a Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"editor@example.com","password":"editor123"}'
```

Copy the `access` token from the response.

### Create an Article
```bash
curl -X POST http://localhost:8000/api/articles/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Article",
    "content": "This is my article content.",
    "status": "draft"
  }'
```

### List Articles
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/articles/
```

## 📚 Next Steps

- **Full API Documentation:** See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Detailed Setup:** See [SETUP.md](./SETUP.md)
- **Implementation Details:** See [IMPLEMENTATION.md](./IMPLEMENTATION.md)
- **Postman Collection:** Import `api_collection.json`

## 🧪 Run Tests
```bash
docker-compose exec web pytest
```

## 🛠️ Useful Commands

```bash
# View logs
docker-compose logs -f web

# Access Django shell
docker-compose exec web python manage.py shell

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

## 📝 Test Credentials

After running `create_test_data.py`:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Editor | editor@example.com | editor123 |
| Reader | reader@example.com | reader123 |

## 🌐 URLs

- **API Base:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Health Check:** http://localhost:8000/health/

## ❓ Troubleshooting

### Port already in use?
Edit `docker-compose.yml` and change the port mapping:
```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database connection error?
Wait a few seconds for PostgreSQL to fully start, then restart:
```bash
docker-compose restart web
```

### Need to reset everything?
```bash
docker-compose down -v
docker-compose up --build
```
