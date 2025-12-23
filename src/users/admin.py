from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import Exists, OuterRef

from movies.models import Favorite, Movie
from .models import User


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    autocomplete_fields = ("movie",)
    fk_name = "spectator"


class AuthoredMovieInline(admin.TabularInline):
    model = Movie.authors.through
    extra = 0
    verbose_name = "Movie"
    verbose_name_plural = "Movies"
    autocomplete_fields = ("movie",)


class HasMoviesFilter(admin.SimpleListFilter):
    title = "Has at least one movie"
    parameter_name = "has_movies"

    def lookups(self, request, model_admin):
        return (("yes", "Yes"), ("no", "No"))

    def queryset(self, request, queryset):
        through = Movie.authors.through
        has_movie_qs = through.objects.filter(user_id=OuterRef("pk"))
        annotated = queryset.annotate(has_movie=Exists(has_movie_qs))

        if self.value() == "yes":
            return annotated.filter(has_movie=True)
        if self.value() == "no":
            return annotated.filter(has_movie=False)
        return annotated


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active", HasMoviesFilter)
    search_fields = ("username", "email", "full_name")
    ordering = ("username",)

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Profile", {"fields": ("role", "full_name", "birth_date", "bio", "avatar_url")}),
    )

    inlines = (FavoriteInline, AuthoredMovieInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()
