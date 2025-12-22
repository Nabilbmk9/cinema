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
