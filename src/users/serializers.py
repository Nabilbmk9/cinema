from rest_framework import serializers
from .models import User


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer public pour un auteur.
    Utilisé dans les réponses API (lecture seule).
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "birth_date",
            "bio",
            "avatar_url",
            "role",
        )
        read_only_fields = ("id", "username", "role", "source", "tmdb_id")


class SpectatorPublicSerializer(serializers.ModelSerializer):
    """
    Serializer public minimal pour un spectateur,
    utilisé dans les notations (nested serializer).
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "role",
        )
