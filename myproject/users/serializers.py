from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser для преобразования данных в формат JSON и обратно."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра чужих профилей."""

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar"]


class UserFullSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования своего профиля."""

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar", "password"]

    def update(self, instance, validated_data):
        # Извлекаем password из validated_data, если он есть
        password = validated_data.pop("password", None)
        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Обновляем пароль, если он есть
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "password2",
            "phone_number",
            "city",
            "avatar",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
