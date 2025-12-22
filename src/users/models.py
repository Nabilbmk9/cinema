from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        SPECTATOR = "SPECTATOR", "Spectator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SPECTATOR,
    )

    # Champs demandés / utiles
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)

    birth_date = models.DateField(null=True, blank=True)

    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.username
