# 🚀 Guide de Déploiement - Article Management API

## 📋 Vue d'ensemble

Ce guide détaille le déploiement en production de l'API de gestion d'articles développée avec Django 4.2, Django REST Framework, PostgreSQL et Redis.

## 🛠️ Prérequis

- Docker et Docker Compose
- Git
- Serveur Linux (Ubuntu/Debian recommandé)
- Domaine configuré (optionnel pour développement)

## 🚀 Déploiement Rapide

### 1. Clonage et Configuration

```bash
# Cloner le repository
git clone <votre-repo-url>
cd test-technique

# Copier la configuration d'environnement
cp .env.example .env

# Générer des clés sécurisées
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(50))"
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(50))"
```

### 2. Configuration de Production

Modifier le fichier `.env` :

```bash
# Django
SECRET_KEY=<votre-cle-secrete-generee>
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Base de données
DB_NAME=article_db_prod
DB_USER=article_user
DB_PASSWORD=<mot-de-passe-fort>
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET_KEY=<votre-cle-jwt-generee>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 3. Déploiement avec Docker Compose

```bash
# Construire et démarrer les services
sudo docker compose up --build -d

# Vérifier l'état des services
sudo docker compose ps

# Voir les logs
sudo docker compose logs -f web
```

### 4. Configuration de Production Supplémentaire

#### Nginx (Reverse Proxy)

Créer `/etc/nginx/sites-available/article-api` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /chemin/vers/test-technique/staticfiles/;
    }

    client_max_body_size 10M;
}
```

#### SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

## 🗄️ Gestion de la Base de Données

### Sauvegarde Automatique

Créer le script `/usr/local/bin/backup-db.sh` :

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="article_db_prod"

mkdir -p $BACKUP_DIR

sudo docker compose exec -T db pg_dump -U article_user $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Garder seulement les 7 derniers jours
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

### Restauration

```bash
gunzip -c /var/backups/postgres/backup_YYYYMMDD_HHMMSS.sql.gz | \
  sudo docker compose exec -T db psql -U article_user article_db_prod
```

## 🔒 Sécurité

### Configuration Django Sécurisée

Dans `config/settings.py` :

```python
# Sécurité production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://votre-domaine.com",
    "https://www.votre-domaine.com",
]
```

### Firewall

```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 📊 Monitoring et Maintenance

### Vérifications de Santé

```bash
# État des services
sudo docker compose ps

# Santé de l'application
curl https://votre-domaine.com/health/

# Connexion base de données
sudo docker compose exec db pg_isready -U article_user -d article_db_prod

# Connexion Redis
sudo docker compose exec redis redis-cli ping
```

### Logs

```bash
# Logs de l'application
sudo docker compose logs -f web

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Maintenance Régulière

```bash
# Mettre à jour les images
sudo docker compose pull
sudo docker compose up -d --build

# Nettoyer les anciennes images
sudo docker system prune -a

# Vérifier l'utilisation disque
df -h
sudo docker system df
```

## 🔧 Résolution de Problèmes

### Problèmes Courants

1. **Port déjà utilisé**
   ```bash
   # Changer le port dans docker-compose.yml
   ports:
     - "8001:8000"
   ```

2. **Erreur de connexion base de données**
   ```bash
   # Attendre que PostgreSQL démarre complètement
   sudo docker compose logs db
   sudo docker compose restart web
   ```

3. **Reset complet**
   ```bash
   sudo docker compose down -v
   sudo docker compose up --build -d
   ```

## 🚀 Mise à l'échelle

### Configuration Gunicorn Production

Modifier le `Dockerfile` :

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

### Load Balancing avec Nginx

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
        # ... autres configurations
    }
}
```

## 📈 Performance

### Optimisations Appliquées

- **Cache Redis** : 15 minutes TTL pour les listes d'articles
- **Pagination** : 10 articles par page
- **Base de données** : Index sur les colonnes fréquemment utilisées
- **Gunicorn** : Configuration multi-workers pour la production

### Monitoring Recommandé

- **Sentry** : Suivi des erreurs
- **Prometheus + Grafana** : Métriques système
- **ELK Stack** : Agrégation de logs

## ✅ Checklist de Déploiement

- [ ] Tests passent en local
- [ ] Variables d'environnement configurées
- [ ] Sauvegardes automatiques configurées
- [ ] Certificats SSL obtenus
- [ ] Domaine configuré
- [ ] Monitoring en place
- [ ] Firewall configuré
- [ ] Service Nginx fonctionnel
- [ ] Application répond sur le domaine
- [ ] Base de données sauvegardée

## 🎯 Conclusion

Cette API est conçue pour être déployée facilement en production avec une architecture scalable et sécurisée. Tous les composants sont containerisés et peuvent être orchestrés avec Docker Compose ou Kubernetes.

Pour toute question, se référer à la documentation complète dans le dossier racine du projet.
