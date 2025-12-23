from django.contrib import admin

from .models import AuthorRatingNote, Favorite, Movie, MovieRatingNote


class MovieRatingNoteInline(admin.TabularInline):
    model = MovieRatingNote
    extra = 0
    autocomplete_fields = ("spectator",)


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    autocomplete_fields = ("spectator", "movie")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "evaluation", "source", "release_date", "created_at")
    list_filter = ("status", "evaluation", "source", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    filter_horizontal = ("authors",)
    inlines = (MovieRatingNoteInline,)


@admin.register(MovieRatingNote)
class MovieRatingNoteAdmin(admin.ModelAdmin):
    list_display = ("movie", "spectator", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("movie__title", "spectator__username", "spectator__email")
    autocomplete_fields = ("movie", "spectator")


@admin.register(AuthorRatingNote)
class AuthorRatingNoteAdmin(admin.ModelAdmin):
    list_display = ("author", "spectator", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("author__username", "author__email", "spectator__username", "spectator__email")
    autocomplete_fields = ("author", "spectator")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("spectator", "movie", "created_at")
    list_filter = ("created_at",)
    search_fields = ("movie__title", "spectator__username", "spectator__email")
    autocomplete_fields = ("movie", "spectator")
