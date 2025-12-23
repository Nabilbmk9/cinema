# 🎬 Cinema — Test technique Django

Application Django permettant de gérer des films, des auteurs et des spectateurs, avec une interface d'administration complète, une API REST sécurisée par JWT et une intégration de données externes via l'API de **The Movie Database (TMDb)**.

Ce projet a été réalisé dans le cadre d'un test technique.

---

## 🧱 Stack technique

- Python ≥ 3.12
- Django ≥ 4.2
- Django REST Framework ≥ 3.15
- PostgreSQL
- Docker & Docker Compose
- JWT (djangorestframework-simplejwt)

---

## 🚀 Installation et lancement

### Prérequis

- Docker
- Docker Compose

### Cloner le dépôt
```bash
git clone <repo_url>
cd cinema
```

### Variables d'environnement

Créer un fichier `.env` à partir de l'exemple fourni :
```bash
cp .env.example .env
```

Renseigner au minimum :
```env
TMDB_API_KEY=your_tmdb_api_key
```

### Démarrer les services
```bash
docker compose up --build -d
```

### Appliquer les migrations
```bash
docker compose run --rm web python src/manage.py migrate
```

### Créer un superutilisateur
```bash
docker compose run --rm web python src/manage.py createsuperuser
```

---

## 🛠 Interface d'administration

Accessible à l'adresse suivante :
```
http://localhost:8000/admin/
```

### Fonctionnalités

- **CRUD complet** sur films, auteurs et spectateurs
- **Filtres avancés** :
  - films par statut, évaluation, date de création
  - auteurs ayant au moins un film
- **Pages de détail enrichies** :
  - auteur : liste des films associés
  - film : auteurs + notations
  - spectateur : favoris en inline

---

## 🔐 Authentification (JWT)

### Inscription spectateur
```http
POST /api/auth/register/
```

### Connexion
```http
POST /api/token/
```

### Déconnexion
```http
POST /api/auth/logout/
```

---

## 🎥 API Films & Auteurs (lecture publique)

Endpoints accessibles sans authentification :
```http
GET /api/movies/
GET /api/movies/?status=PUBLISHED
GET /api/movies/?source=ADMIN
GET /api/movies/?source=TMDB

GET /api/authors/
GET /api/authors/?source=ADMIN
GET /api/authors/?source=TMDB
```

---

## 👤 Actions spectateur (JWT requis)

Endpoints protégés :

### Ajouter un film en favori
```http
POST /api/me/favorites/
```

### Retirer un favori
```http
DELETE /api/me/favorites/{movie_id}/
```

### Lister ses favoris
```http
GET /api/me/favorites/
```

### Noter un film
```http
POST /api/me/ratings/movies/
```

### Noter un auteur
```http
POST /api/me/ratings/authors/
```

---

## 🌐 Intégration TMDb

L'import des films et auteurs se fait via une commande Django dédiée.

### Commande d'import
```bash
docker compose run --rm web python src/manage.py import_tmdb --pages 1
```

### Fonctionnalités

- import des films populaires
- import des auteurs liés aux films
- import idempotent (basé sur `tmdb_id`)
- gestion des doublons
- attribution automatique :
  - `source=TMDB`
  - `role=AUTHOR` pour les auteurs
- logs clairs en sortie de commande

---

## 🧠 Choix d'architecture

Les décisions techniques importantes sont documentées dans :
```
docs/decisions.md
```

Incluant notamment :

- stratégie d'authentification (User unique + rôles)
- modélisation auteurs / spectateurs
- gestion de la source des données (ADMIN / TMDB)
- intégration TMDb
- choix liés à l'admin et à l'API

---

## 🧪 Tests

Les fonctionnalités clés (authentification, permissions, actions spectateur, import TMDb) ont été validées via des tests manuels à l'aide de requêtes HTTP.

Une stratégie de tests automatisés (pytest / DRF) peut être ajoutée.

---

## 📄 Licence

Ce projet est fourni dans le cadre d'un test technique.