## Décision — Auth personnalisée (Auteur / Spectateur)

### Choix retenu
Un seul modèle `User` basé sur `AbstractUser` avec un champ `role` :
- `AUTHOR`
- `SPECTATOR`

### Pourquoi
- Django ne gère proprement qu’un seul `AUTH_USER_MODEL`.
- Un seul flux d’authentification (JWT), permissions et admin simplifiés.
- Évite la complexité/risque de deux modèles utilisateurs authentifiables.
- Permet d’appliquer facilement les règles métier (films liés à des auteurs, actions spectateur, etc.).

### Alternative envisagée
User unique + profils `AuthorProfile` / `SpectatorProfile` (OneToOne) :
- meilleure séparation des champs spécifiques,
- mais complexité supplémentaire inutile pour ce test.

### Implémentation
- Modèle : `src/users/models.py`
- Configuration : `AUTH_USER_MODEL = "users.User"` dans `src/cinema/settings.py`
- Migration : `src/users/migrations/0001_initial.py`


---

## Décision — Servir les fichiers statiques (Admin) en Docker

### Problème
L’interface Django admin s’affichait sans CSS dans l’environnement Docker (URLs `/static/...` non servies).

### Choix retenu
Utiliser **WhiteNoise** pour servir les fichiers statiques via Django, y compris en environnement Docker.

### Pourquoi
- Solution simple, standard, et robuste pour servir `/static/`.
- Évite une configuration Nginx dédiée juste pour le dev.
- Permet de garantir que l’admin reste utilisable dans le contexte du test.

### Implémentation
- Dépendance : `whitenoise` dans `requirements.txt`
- Middleware : `whitenoise.middleware.WhiteNoiseMiddleware` dans `src/cinema/settings.py`
- Static root : `STATIC_ROOT = BASE_DIR / "staticfiles"`
- Collecte : `python manage.py collectstatic`
- Gitignore : `staticfiles/`

---

## Décision — Modélisation Films / Favoris / Notations

### Choix retenu
Créer une app `movies` avec :
- `Movie` (film) + champs métier (titre, description, date, statut, évaluation)
- relation `Movie.authors` en ManyToMany vers `users.User` filtré sur `role=AUTHOR`
- `Favorite` (spectateur ↔ film)
- `MovieRatingNote` (spectateur ↔ film)
- `AuthorRatingNote` (spectateur ↔ auteur)

### Pourquoi
- Couvre directement les exigences : favoris + notations film/auteur.
- ManyToMany pour refléter le cas réel (plusieurs auteurs pour un film).
- Tables dédiées `Favorite`/`*RatingNote` pour :
  - empêcher les doublons (`unique_together`)
  - stocker des métadonnées (date, commentaire)
- Ajout d’un champ `source` (ADMIN/TMDB) pour permettre le filtrage demandé (contenu créé manuellement vs import TMDb).

### Implémentation
- Modèles : `src/movies/models.py`
- Admin : `src/movies/admin.py` + enrichissement `src/users/admin.py`
- Migrations : `src/movies/migrations/0001_initial.py` (si présent)

---

## Décision — API REST + JWT pour les actions spectateur

### Choix retenu
Mettre en place une API REST sécurisée par JWT avec Django REST Framework et SimpleJWT.

### Pourquoi
- L’énoncé impose une API REST complète avec authentification JWT.
- JWT permet une séparation claire entre :
  - lecture publique (films / auteurs)
  - actions protégées (favoris, notations).
- Les permissions par rôle (`AUTHOR` / `SPECTATOR`) sont explicites et testables.

### Implémentation
- Auth JWT : `djangorestframework-simplejwt`
- Endpoints :
  - `POST /api/auth/register/`
  - `POST /api/token/`
  - `POST /api/auth/logout/`
- Actions spectateur :
  - favoris (`/api/me/favorites/`)
  - notations film/auteur (`/api/me/ratings/...`)
- Permissions dédiées : `IsSpectator`
- Tests manuels validés via requêtes HTTP (PowerShell)

### Note sur les emails des auteurs TMDb
L’API TMDb ne fournit pas d’adresse email pour les auteurs.
Le modèle utilisateur imposant un email unique, un email fictif
stable de la forme `tmdb_<id>@example.invalid` est utilisé.

Ce choix permet :
- d’éviter toute collision en base
- de conserver l’unicité
- de garantir un import idempotent

En production, ce champ serait soit nullable,
soit géré via un modèle auteur distinct.

