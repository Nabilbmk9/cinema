from django.urls import path
from .action_views import (
    MyAuthorRatingAPIView,
    MyFavoriteDeleteAPIView,
    MyFavoritesAPIView,
    MyMovieRatingAPIView,
)

urlpatterns = [
    path("me/favorites/", MyFavoritesAPIView.as_view(), name="my_favorites"),
    path("me/favorites/<int:movie_id>/", MyFavoriteDeleteAPIView.as_view(), name="my_favorite_delete"),
    path("me/ratings/movies/", MyMovieRatingAPIView.as_view(), name="my_movie_rating"),
    path("me/ratings/authors/", MyAuthorRatingAPIView.as_view(), name="my_author_rating"),
]
