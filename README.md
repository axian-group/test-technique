# 📚 Article Management API - Test Technique

## 🎯 Description du Projet

API REST complète de gestion d'articles développée avec Django 4.2, Django REST Framework, authentification JWT et architecture microservices.

### ✨ Fonctionnalités Implémentées

- **Authentification JWT** avec système de rôles (Admin/Editor/Reader)
- **CRUD Articles** avec gestion des statuts (draft/published/archived)
- **Cache Redis** pour optimisation des performances (15 min TTL)
- **Tests automatisés** (18 tests passent à 100%)
- **API documentée** avec exemples d'utilisation
- **Déploiement Docker** prêt pour la production

## 🚀 Démarrage Rapide

### Prérequis
- Docker et Docker Compose
- Git

### Installation

```bash
# 1. Cloner le repository
git clone <votre-repo-url>
cd test-technique

# 2. Configuration environnement
cp .env.example .env

# 3. Démarrer les services
sudo docker compose up --build -d

# 4. Créer des données de test
sudo docker compose exec web python manage.py create_test_data

# 5. Lancer les tests
sudo docker compose exec web pytest
```

### 🔗 URLs

- **API** : http://localhost:8000
- **Admin Django** : http://localhost:8000/admin
- **Health Check** : http://localhost:8000/health/

### 👤 Comptes de Test

| Rôle | Email | Mot de passe |
|------|-------|-------------|
| Admin | admin@example.com | admin123 |
| Editor | editor@example.com | editor123 |
| Reader | reader@example.com | reader123 |

## 📋 Structure du Repository

```
test-technique/
├── README.md (ce fichier)
├── REVIEW.md (analyse du code)
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
├── articles/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── tests.py
│   └── urls.py
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
├── deployment/
│   └── deployment-guide.md (guide de déploiement)
├── scripts/ (outils de développement)
├── *.md (documentation complète)
└── api_collection.json (Postman)
```

## 🧪 Tests

```bash
# Lancer tous les tests
sudo docker compose exec web pytest

# Avec coverage
sudo docker compose exec web pytest --cov=. --cov-report=html

# Résultat : 18 passed ✅
```

## 📚 Documentation

- **[QUICK_START.md](./QUICK_START.md)** - Démarrage en 3 minutes
- **[SETUP.md](./SETUP.md)** - Installation détaillée
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Référence API complète
- **[IMPLEMENTATION.md](./IMPLEMENTATION.md)** - Décisions techniques
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guide de déploiement complet
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Résumé du projet

## 🚀 Déploiement en Production

Voir le guide complet : **[deployment/deployment-guide.md](./deployment/deployment-guide.md)**

### Points Clés du Déploiement

- **Docker Compose** avec PostgreSQL + Redis + Django
- **Configuration Nginx** pour le reverse proxy
- **SSL/HTTPS** avec Let's Encrypt
- **Sauvegardes automatiques** de la base de données
- **Monitoring** et logs centralisés
- **Sécurité** renforcée (firewall, headers sécurisés)

## 🛠️ Outils de Développement

### Makefile (Recommandé)

```bash
make help        # Voir toutes les commandes
make up          # Démarrer les services
make test        # Lancer les tests
make logs        # Voir les logs
make down        # Arrêter proprement
```

### Commandes Docker Directes

```bash
sudo docker compose up --build -d    # Démarrer
sudo docker compose logs -f web      # Logs
sudo docker compose exec web python manage.py shell  # Shell Django
sudo docker compose down             # Arrêter
```

## 🔒 Sécurité

- **Authentification JWT** avec tokens sécurisés (60 min accès, 24h refresh)
- **Rôles granulaires** : Admin (tout), Editor (ses articles), Reader (lecture seule)
- **Variables d'environnement** pour la configuration sensible
- **Headers de sécurité** configurés (XSS, CSRF, etc.)

## 📊 Performance

- **Cache Redis** : Réponses rapides pour les listes d'articles
- **Pagination** : 10 éléments par page pour gérer les gros volumes
- **Base optimisée** : Index sur les colonnes fréquemment utilisées
- **Gunicorn** : Configuration multi-workers pour la production

## ✅ Checklist Réalisations

### Développement ✅
- [x] Authentification JWT complète
- [x] Système de rôles (Admin/Editor/Reader)
- [x] CRUD Articles avec permissions
- [x] Cache Redis implémenté
- [x] Tests unitaires (18/18 passent)
- [x] API documentée

### Infrastructure ✅
- [x] Docker + docker-compose fonctionnel
- [x] PostgreSQL + Redis configurés
- [x] Variables d'environnement
- [x] Guide de déploiement détaillé

### DevOps ✅
- [x] Makefile pour productivité
- [x] Configuration production (Nginx, SSL)
- [x] Sauvegardes automatiques
- [x] Monitoring intégré

## 🤝 Auteur

**Raoelinirina Safidy** - Développement complet de l'API

---

## 📞 Support

Pour toute question :

1. Consulter la documentation dans `*.md`
2. Vérifier les logs avec `sudo docker compose logs -f web`
3. Lancer les tests pour diagnostiquer : `sudo docker compose exec web pytest`
4. Consulter le guide de déploiement : `deployment/deployment-guide.md`

---

**⭐ Projet prêt pour évaluation !**
