# Docker Setup Notes

## Docker Permission Issue

If you encounter permission errors when running Docker commands, you have two options:

### Option 1: Add User to Docker Group (Recommended)

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Log out and log back in for changes to take effect
# Or run this command to apply changes immediately:
newgrp docker

# Verify it works
docker ps
```

### Option 2: Use sudo

```bash
# Run all docker commands with sudo
sudo docker compose up --build -d
sudo docker compose exec web python manage.py migrate
```

## Quick Start Commands

Once Docker permissions are fixed:

```bash
# Build and start all services
docker compose up --build -d

# Wait for services to be ready (check logs)
docker compose logs -f

# Once you see "Database available!" and server started, press Ctrl+C

# Create test data
docker compose exec web python scripts/create_test_data.py

# Run tests
docker compose exec web pytest

# View logs
docker compose logs -f web

# Stop services
docker compose down
```

## Using Make Commands

If you have `make` installed:

```bash
make build          # Build containers
make up             # Start services
make logs           # View logs
make test-data      # Create test data
make test           # Run tests
make down           # Stop services
```

## Troubleshooting

### Services won't start
```bash
# Check what's running
docker compose ps

# Check logs
docker compose logs

# Restart services
docker compose restart
```

### Port already in use
Edit `docker-compose.yml` and change the port:
```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database connection issues
```bash
# Wait a bit longer for PostgreSQL to start
docker compose logs db

# Restart the web service
docker compose restart web
```

### Clean slate
```bash
# Remove everything and start fresh
docker compose down -v
docker compose up --build -d
```
