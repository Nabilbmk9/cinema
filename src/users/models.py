from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
    tmdb_id = models.PositiveIntegerField(null=True, blank=True, unique=True)

    # Champs demandés / utiles
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)

    birth_date = models.DateField(null=True, blank=True)

    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.username
