# Docker Deployment Guide

## Prerequisites
- Docker installed
- Docker Compose installed

## Quick Start

### 1. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and update the SECRET_KEY and passwords
```

### 2. Build and Start Containers
```bash
docker-compose up -d --build
```

### 3. Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

### 4. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Seed Data (Optional)
```bash
docker-compose exec web python manage.py seed_quizzes
docker-compose exec web python manage.py seed_revisions
```

## Access the Application
- **Application**: http://localhost
- **Admin Panel**: http://localhost/admin

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ This will delete your database)
```bash
docker-compose down -v
```

### Restart a Service
```bash
docker-compose restart web
```

### Execute Django Commands
```bash
docker-compose exec web python manage.py <command>
```

### Access Database
```bash
docker-compose exec db psql -U calculus_user -d calculus_db
```

### Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## Production Deployment

### Important Security Steps

1. **Change SECRET_KEY**: Generate a new secret key
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Update Passwords**: Change all default passwords in `.env`

3. **Update ALLOWED_HOSTS**: Add your domain name

4. **Enable HTTPS**: Consider using Let's Encrypt with Certbot

5. **Update Nginx**: Configure SSL certificates in nginx.conf

### Backup Database
```bash
docker-compose exec db pg_dump -U calculus_user calculus_db > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker-compose exec -T db psql -U calculus_user -d calculus_db
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs web
```

### Database connection errors
- Check that the `db` service is healthy
- Verify DATABASE_URL in .env matches postgres credentials

### Static files not loading
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

### Permission errors
```bash
docker-compose exec web chown -R nobody:nogroup /app/staticfiles
```

## File Structure
```
test_platform/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── nginx/
│   └── nginx.conf
├── manage.py
└── (your Django app files)
```
