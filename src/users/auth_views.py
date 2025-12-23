from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .auth_serializers import SpectatorRegisterSerializer


class SpectatorRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SpectatorRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    """
    Logout côté serveur via blacklist du refresh token.
    Le client doit envoyer {"refresh": "<token>"}.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Missing refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh)
        token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
