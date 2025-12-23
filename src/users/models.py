from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec champs supplémentaires :
    - rôle (AUTHOR ou SPECTATOR)
    - source (ADMIN ou TMDB) pour différencier création manuelle et import TMDb
    - tmdb_id pour stocker l’identifiant TMDb de l’auteur
    - full_name, birth_date, bio, avatar_url
    """

    class Role(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        SPECTATOR = "SPECTATOR", "Spectator"

    class Source(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        TMDB = "TMDB", "TMDb"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SPECTATOR,
    )

    source = models.CharField(
        max_length=10,
        choices=Source.choices,
        default=Source.ADMIN,
    )

    tmdb_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True,
        help_text="Identifiant TMDb de l’utilisateur (auteur) si importé depuis TMDb",
    )

    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.username


class Author(User):
    """
    Proxy model pour représenter les auteurs distinctement.
    Enregistre automatiquement le rôle en AUTHOR à la sauvegarde.
    """
    class Meta:
        proxy = True
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def save(self, *args, **kwargs):
        self.role = User.Role.AUTHOR
        super().save(*args, **kwargs)


class Spectator(User):
    """
    Proxy model pour représenter les spectateurs distinctement.
    Enregistre automatiquement le rôle en SPECTATOR à la sauvegarde.
    """
    class Meta:
        proxy = True
        verbose_name = "Spectator"
        verbose_name_plural = "Spectators"

    def save(self, *args, **kwargs):
        self.role = User.Role.SPECTATOR
        super().save(*args, **kwargs)
