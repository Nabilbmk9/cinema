from rest_framework import serializers
from .models import User


class SpectatorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "full_name", "birth_date")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data, role=User.Role.SPECTATOR)
        user.set_password(password)
        user.save()
        return user
