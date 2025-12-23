from django.apps import apps
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsSpectator
from movies.models import AuthorRatingNote, Favorite, Movie, MovieRatingNote
from movies.serializers import MovieSerializer

from .action_serializers import (
    AuthorRatingCreateSerializer,
    FavoriteCreateSerializer,
    MovieRatingCreateSerializer,
)


class MyFavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSpectator]

    def get(self, request):
        movie_qs = Movie.objects.filter(favorited_by__spectator=request.user).prefetch_related("authors", "ratings__spectator")
        serializer = MovieSerializer(movie_qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = Movie.objects.get(id=serializer.validated_data["movie_id"])
        Favorite.objects.get_or_create(spectator=request.user, movie=movie)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyFavoriteDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSpectator]

    def delete(self, request, movie_id: int):
        Favorite.objects.filter(spectator=request.user, movie_id=movie_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyMovieRatingAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSpectator]

    def post(self, request):
        serializer = MovieRatingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie_id = serializer.validated_data["movie_id"]
        score = serializer.validated_data["score"]
        comment = serializer.validated_data.get("comment", "")

        obj, _created = MovieRatingNote.objects.update_or_create(
            spectator=request.user,
            movie_id=movie_id,
            defaults={"score": score, "comment": comment},
        )
        return Response({"id": obj.id}, status=status.HTTP_200_OK)


class MyAuthorRatingAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSpectator]

    def post(self, request):
        serializer = AuthorRatingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author_id = serializer.validated_data["author_id"]
        score = serializer.validated_data["score"]
        comment = serializer.validated_data.get("comment", "")

        obj, _created = AuthorRatingNote.objects.update_or_create(
            spectator=request.user,
            author_id=author_id,
            defaults={"score": score, "comment": comment},
        )
        return Response({"id": obj.id}, status=status.HTTP_200_OK)
