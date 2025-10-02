# Test Technique - Backend & DevOps Developer

## 📋 Contexte

Nous cherchons à évaluer vos compétences en **développement backend** et en **DevOps**, avec un focus particulier sur :

* La conception et l’implémentation d’APIs REST
* L’infrastructure et le déploiement (Docker, PostgreSQL, Redis)
* Les bonnes pratiques de code, de sécurité et de tests

👉 Le langage/framework imposé est **Python (Django + Django REST Framework)**.
Même si ce n’est pas votre stack principale, l’objectif est d’évaluer votre **capacité d’adaptation** et vos réflexes d’architecture et de déploiement.

**Deadline :** 72 heures à partir de la réception de ce test
**Livraison :** Via ce repository GitHub

---

## 🎯 Partie 1 : Développement

### Objectif

Créer une API REST pour un système de gestion de contenu d'articles avec authentification et permissions.

### Fonctionnalités attendues

#### 1. Authentification & Permissions

* Système d'authentification JWT
* 3 types d'utilisateurs : Admin, Editor, Reader
* Permissions :
  * Admin : CRUD complet sur articles et utilisateurs
  * Editor : CRUD sur ses propres articles, lecture des autres
  * Reader : lecture seule

#### 2. API Endpoints Articles
* `POST /api/articles/` - Créer un article
* `GET /api/articles/` - Liste paginée (10 par page)
* `GET /api/articles/{id}/` - Détail d'un article
* `PUT /api/articles/{id}/` - Modifier un article
* `DELETE /api/articles/{id}/` - Supprimer un article
* `GET /api/articles/?status=published` - Filtrer par statut

#### 3. Modèle Article

```python
{
    "id": integer,
    "title": string (max 200 chars),
    "content": text,
    "status": choice ["draft", "published", "archived"],
    "author": foreign_key (User),
    "created_at": datetime,
    "updated_at": datetime,
    "published_at": datetime (nullable)
}
```

#### 4. Aspects Infrastructure

* **Docker** : Dockerfile + docker-compose.yml
  * Service Django
  * Service PostgreSQL
  * Service Redis (pour le cache)
* **Cache** : Implémenter un système de cache pour la liste des articles
* **Environment variables** : Configuration via .env
* **Tests** : Au moins 5 tests unitaires couvrant les cas critiques

#### 5. Documentation
* README.md avec :
  * Instructions d'installation
  * Guide de déploiement
  * Liste des endpoints avec exemples
* Collection Postman ou fichier curl pour tester l'API

### Stack technique imposée
* **Backend** : Django 4.x + Django REST Framework
* **Base de données** : PostgreSQL
* **Cache** : Redis
* **Containerisation** : Docker + docker-compose
---

## 🔍 Partie 2 : Code Review (1h)
### Instructions
Analyser le code fourni dans le dossier `/code-review/` et créer un fichier `REVIEW.md` avec :
1. **Problèmes identifiés** (bugs, failles de sécurité, mauvaises pratiques)
2. **Améliorations suggérées** (performance, maintenabilité, architecture)
3. **Refactoring proposé** pour au moins UN des problèmes majeurs

### Ce qu'on évalue
* Capacité à identifier les problèmes critiques
* Connaissance des bonnes pratiques Django/Python
* Approche pédagogique (comment vous expliquez vos remarques)
* Vision architecture et sécurité
---

## 📦 Structure attendue du repository

```
test-technique/
├── README.md (votre documentation)
├── REVIEW.md (votre analyse du code)
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
└── deployment/
    └── deployment-guide.md (votre guide de déploiement)
```

---

## 🎯 Critères d'évaluation

### Code Quality (25%)

* Clean code et lisibilité
* Respect des conventions Python/Django (PEP 8)
* Structure du projet
* Gestion des erreurs

### Fonctionnalités (20%)

* Tous les endpoints fonctionnent
* Authentification et permissions correctes
* Validations appropriées

### Infrastructure & DevOps (35%)

* Docker fonctionnel
* Configuration environnement
* Guide de déploiement clair
* Cache bien implémenté
* Bonus : CI/CD ou automatisation

### Tests & Documentation (15%)

* Tests pertinents
* Documentation claire
* Commentaires utiles

### Code Review (5%)

* Pertinence des remarques
* Vision globale

---

## 🚀 Livraison

1. **Commitez régulièrement** (on regarde votre démarche)
2. **Créez une Pull Request** quand vous avez terminé
3. **Le projet doit démarrer avec** : `docker-compose up`
4. **Préparez des credentials de test** dans le README

---

## ❓ Questions
Si vous avez des questions de clarification, ouvrez une **Issue** sur ce repository. Nous répondrons dans les 24h.

---

## 📝 Notes importantes
* **Pas de copier-coller** de projets existants (on vérifie)
* **La qualité prime sur la quantité** - un code simple et bien fait vaut mieux qu'un code complexe mal organisé
* **N'hésitez pas à justifier vos choix** dans le README ou en commentaires
* **Branche dédiée** travailler sur une branche dédiée à votre nom (ex: feature/votre-nom) et d’ouvrir une Pull Request vers main une fois le test terminé

---

Bon courage ! 🚀
