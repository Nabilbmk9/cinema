from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Movie.objects.all().prefetch_related("authors", "ratings__spectator").order_by("-created_at")

        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        source = self.request.query_params.get("source")
        if source:
            qs = qs.filter(source=source)

        return qs
