import os
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class TMDbClient:
    api_key: str
    base_url: str = "https://api.themoviedb.org/3"
    language: str = "fr-FR"

    @classmethod
    def from_env(cls) -> "TMDbClient":
        api_key = os.getenv("TMDB_API_KEY")
        if not api_key:
            raise RuntimeError("TMDB_API_KEY is missing in environment.")
        return cls(api_key=api_key)

    def get(self, path: str, **params: Any) -> dict:
        url = f"{self.base_url}{path}"
        query = {"api_key": self.api_key, "language": self.language, **params}
        resp = requests.get(url, params=query, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def popular_movies(self, page: int) -> dict:
        return self.get("/movie/popular", page=page)

    def movie_credits(self, movie_id: int) -> dict:
        return self.get(f"/movie/{movie_id}/credits")
