from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Source(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    TMDB = "TMDB", "TMDb"


class MovieStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"


class MovieEvaluation(models.TextChoices):
    VERY_BAD = "VERY_BAD", "Very bad"
    BAD = "BAD", "Bad"
    OK = "OK", "Ok"
    GOOD = "GOOD", "Good"
    EXCELLENT = "EXCELLENT", "Excellent"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)

    evaluation = models.CharField(
        max_length=20,
        choices=MovieEvaluation.choices,
        default=MovieEvaluation.OK,
    )
    status = models.CharField(
        max_length=20,
        choices=MovieStatus.choices,
        default=MovieStatus.DRAFT,
    )
    source = models.CharField(
        max_length=10,
        choices=Source.choices,
        default=Source.ADMIN,
    )

    # Inspiré TMDb
    tmdb_id = models.PositiveIntegerField(null=True, blank=True, unique=True)
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)
    original_language = models.CharField(max_length=10, blank=True)
    popularity = models.FloatField(null=True, blank=True)

    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="authored_movies",
        blank=True,
        limit_choices_to={"role": "AUTHOR"},
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Favorite(models.Model):
    spectator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        limit_choices_to={"role": "SPECTATOR"},
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("spectator", "movie")

    def __str__(self) -> str:
        return f"{self.spectator_id} -> {self.movie_id}"


class MovieRatingNote(models.Model):
    spectator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movie_notes",
        limit_choices_to={"role": "SPECTATOR"},
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")

    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("spectator", "movie")

    def __str__(self) -> str:
        return f"{self.movie_id} rated by {self.spectator_id}: {self.score}"


class AuthorRatingNote(models.Model):
    spectator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_notes",
        limit_choices_to={"role": "SPECTATOR"},
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings_as_author",
        limit_choices_to={"role": "AUTHOR"},
    )

    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("spectator", "author")

    def __str__(self) -> str:
        return f"{self.author_id} rated by {self.spectator_id}: {self.score}"
