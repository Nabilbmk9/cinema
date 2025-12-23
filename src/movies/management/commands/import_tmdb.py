import logging
from datetime import datetime
from typing import Optional

from django.core.management.base import BaseCommand
from django.db import transaction

from movies.models import Movie, MovieEvaluation, MovieStatus, Source as MovieSource
from movies.tmdb_client import TMDbClient

logger = logging.getLogger(__name__)


def map_vote_to_evaluation(vote_avg: Optional[float]) -> str:
    if vote_avg is None:
        return MovieEvaluation.OK
    # TMDb vote_average est sur 10
    if vote_avg < 3.0:
        return MovieEvaluation.VERY_BAD
    if vote_avg < 5.0:
        return MovieEvaluation.BAD
    if vote_avg < 7.0:
        return MovieEvaluation.OK
    if vote_avg < 8.5:
        return MovieEvaluation.GOOD
    return MovieEvaluation.EXCELLENT


class Command(BaseCommand):
    help = "Import movies + authors from TMDb (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--pages", type=int, default=1, help="Number of pages to import from /movie/popular")
        parser.add_argument("--language", type=str, default="fr-FR", help="TMDb language (default: fr-FR)")

    @transaction.atomic
    def handle(self, *args, **options):
        pages = max(1, int(options["pages"]))
        language = options["language"]

        client = TMDbClient.from_env()
        client = TMDbClient(api_key=client.api_key, language=language)

        # Import User model (custom) sans import circulaire
        from django.apps import apps
        User = apps.get_model("users", "User")

        created_movies = 0
        updated_movies = 0
        created_authors = 0
        linked_authors = 0

        for page in range(1, pages + 1):
            data = client.popular_movies(page=page)
            results = data.get("results", [])

            for item in results:
                tmdb_movie_id = item.get("id")
                if not tmdb_movie_id:
                    continue

                title = item.get("title") or ""
                overview = item.get("overview") or ""
                release_date_raw = item.get("release_date") or None
                poster_path = item.get("poster_path") or ""
                backdrop_path = item.get("backdrop_path") or ""
                original_language = item.get("original_language") or ""
                popularity = item.get("popularity")
                vote_average = item.get("vote_average")

                release_date = None
                if release_date_raw:
                    try:
                        release_date = datetime.strptime(release_date_raw, "%Y-%m-%d").date()
                    except ValueError:
                        release_date = None

                defaults = {
                    "title": title[:255],
                    "description": overview,
                    "release_date": release_date,
                    "poster_path": poster_path,
                    "backdrop_path": backdrop_path,
                    "original_language": original_language,
                    "popularity": popularity,
                    "evaluation": map_vote_to_evaluation(vote_average),
                    "status": MovieStatus.PUBLISHED,
                    "source": MovieSource.TMDB,
                }

                movie, created = Movie.objects.update_or_create(
                    tmdb_id=tmdb_movie_id,
                    defaults=defaults,
                )
                if created:
                    created_movies += 1
                else:
                    updated_movies += 1

                # Auteurs (credits.cast) : on prend les 5 premiers pour rester raisonnable
                credits = client.movie_credits(movie_id=tmdb_movie_id)
                cast = credits.get("cast") or []

                for person in cast[:5]:
                    person_id = person.get("id")
                    name = person.get("name") or ""
                    if not person_id or not name:
                        continue

                    # Username stable pour éviter collisions
                    username = f"tmdb_{person_id}"

                    placeholder_email = f"tmdb_{person_id}@example.invalid"

                    author, author_created = User.objects.get_or_create(
                        tmdb_id=person_id,
                        defaults={
                            "username": username,
                            "email": placeholder_email,
                            "role": "AUTHOR",
                            "source": "TMDB",
                            "full_name": name[:255],
                        },
                    )
                    if author_created:
                        author.set_unusable_password()
                        author.save(update_fields=["password"])
                        created_authors += 1

                    movie.authors.add(author)
                    linked_authors += 1

        self.stdout.write(self.style.SUCCESS(
            f"TMDb import done: movies created={created_movies}, updated={updated_movies}, "
            f"authors created={created_authors}, author links={linked_authors}"
        ))
