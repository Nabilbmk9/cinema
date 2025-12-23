from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Movie, MovieStatus
from .serializers import MovieSerializer
from cinema.permissions import ReadOnlyOrAdmin


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        qs = (
            Movie.objects.all()
            .prefetch_related("authors", "ratings__spectator")
            .order_by("-created_at")
        )

        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        source = self.request.query_params.get("source")
        if source:
            qs = qs.filter(source=source)

        return qs

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def archive(self, request, pk=None):
        movie = self.get_object()
        movie.status = MovieStatus.ARCHIVED
        movie.save(update_fields=["status", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)
