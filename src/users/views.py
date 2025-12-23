from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = User.objects.filter(role=User.Role.AUTHOR).order_by("username")
        source = self.request.query_params.get("source")
        if source:
            qs = qs.filter(source=source)
        return qs

    def perform_destroy(self, instance):
        if instance.authored_movies.exists():
            raise ValidationError("Impossible de supprimer un auteur ayant des films.")
        return super().perform_destroy(instance)
