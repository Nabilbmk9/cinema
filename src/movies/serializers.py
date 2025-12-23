from rest_framework import serializers

from movies.models import Movie, MovieRatingNote
from users.serializers import AuthorSerializer, SpectatorPublicSerializer


class MovieRatingNoteSerializer(serializers.ModelSerializer):
    """
    Serializer pour les notes de films.
    Le spectateur est sérialisé via un nested serializer (conforme à l'énoncé).
    """

    spectator = SpectatorPublicSerializer(read_only=True)

    class Meta:
        model = MovieRatingNote
        fields = (
            "id",
            "spectator",
            "score",
            "comment",
            "created_at",
        )


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer principal pour les films.
    Inclut :
    - auteurs (nested)
    - notes (nested)
    """

    authors = AuthorSerializer(many=True, read_only=True)
    ratings = MovieRatingNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "release_date",
            "evaluation",
            "status",
            "source",
            "tmdb_id",
            "poster_path",
            "backdrop_path",
            "original_language",
            "popularity",
            "authors",
            "ratings",
            "created_at",
        )
