from rest_framework.permissions import BasePermission


class IsSpectator(BasePermission):
    message = "Only spectators can perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "role", None) == "SPECTATOR")
