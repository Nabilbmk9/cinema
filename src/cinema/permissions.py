from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnlyOrAdmin(BasePermission):
    """
    Anonyme : accès en lecture seule.
    Utilisateur staff/admin: accès complet.
    """

    def has_permission(self, request, view):
        # Méthodes GET, HEAD et OPTIONS => autorisées à tous
        if request.method in SAFE_METHODS:
            return True
        # Autres méthodes => uniquement si l'utilisateur est authentifié et staff
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
