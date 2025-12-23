from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = User.objects.filter(role=User.Role.AUTHOR).order_by("username")
        source = self.request.query_params.get("source")
        if source:
            qs = qs.filter(source=source)
        return qs
