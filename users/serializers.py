from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'invite_code', 'activated_invite_code']


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для логина пользователя по номеру телефона.
    """
    phone_number = serializers.CharField(max_length=15)


class ActivateInviteCodeSerializer(serializers.Serializer):
    """
    Сериализатор для активации инвайт-кода.
    """
    invite_code = serializers.CharField(max_length=6)
