from datetime import timedelta

from .services.token_service import TokenService
from constance import config
from typing import Dict, Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "password"
        ]

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        user = get_user_model()(email=email)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')
        read_only_fields = ("id", "email")

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token.set_exp(
            lifetime=timedelta(seconds=config.ACCESS_TOKEN_LIFETIME))  # ACCESS_TOKEN_LIFETIME from settings
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        data["refresh_token"] = TokenService.create_refresh_token(self.user)
        # rename the fields in the result
        data["access_token"] = data.pop("access")
        data.pop("refresh")
        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh_token = attrs["refresh_token"]
        data = TokenService.update_tokens(refresh_token)
        return data


class TokenLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh_token = attrs["refresh_token"]
        result = TokenService.delete_refresh_token(refresh_token)
        if result:
            data = {"success": "User logged out."}
        else:
            data = {"success": "Something was wrong"}
        return data
