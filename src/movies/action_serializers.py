from django.conf import settings
from rest_framework import serializers

from movies.models import AuthorRatingNote, Favorite, Movie, MovieRatingNote


class FavoriteCreateSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()

    def validate_movie_id(self, value):
        if not Movie.objects.filter(id=value).exists():
            raise serializers.ValidationError("Movie not found.")
        return value


class MovieRatingCreateSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    score = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True, required=False)

    def validate_movie_id(self, value):
        if not Movie.objects.filter(id=value).exists():
            raise serializers.ValidationError("Movie not found.")
        return value


class AuthorRatingCreateSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    score = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(allow_blank=True, required=False)

    def validate_author_id(self, value):
        if not settings.AUTH_USER_MODEL:
            return value
        # On évite l’import circulaire : on récupère le modèle User via apps.get_model
        from django.apps import apps
        User = apps.get_model("users", "User")
        if not User.objects.filter(id=value, role="AUTHOR").exists():
            raise serializers.ValidationError("Author not found.")
        return value
