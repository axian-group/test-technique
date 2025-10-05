# API CRUD Articles - Django REST Framework + JWT

## Description

Cette API permet de gérer des articles avec un système d’authentification JWT et une gestion des rôles :
- Admin : peut créer, lire, mettre à jour et supprimer tous les articles.
- Editor : peut créer, lire et modifier uniquement ses propres articles.
- Reader : peut uniquement lire les articles.

---

## Technologies utilisées

- Django 5+
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL
- Docker / Docker Compose
- Pytest ou unittest

---

## Installation et exécution

### 1. Cloner le projet
```bash
git clone https://github.com/axian-group/test-technique
cd test-technique
