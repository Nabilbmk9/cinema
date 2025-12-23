from django.urls import path
from .auth_views import LogoutAPIView, SpectatorRegisterAPIView

urlpatterns = [
    path("auth/register/", SpectatorRegisterAPIView.as_view(), name="spectator_register"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),
]
