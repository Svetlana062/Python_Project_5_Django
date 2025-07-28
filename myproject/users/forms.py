from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания нового пользователя."""

    class Meta:
        model = CustomUser
        fields = ["username", "email", "avatar", "phone_number", "city"]

    def clean_email(self):
        """Создаем запрос к базе данных, чтобы проверить наличие пользователя
        с таким email."""

        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_username(self):
        """Создаем запрос к базе данных, чтобы проверить наличие пользователя
        с таким username."""

        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username


class RegistrationForm(UserCreationForm):
    """Форма для регистрации нового пользователя."""

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "avatar",
            "phone_number",
            "city",
        )

    def clean_email(self):
        """Создаем запрос к базе данных, чтобы проверить наличие пользователя
        с таким email."""

        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_username(self):
        """Создаем запрос к базе данных, чтобы проверить наличие пользователя
        с таким username."""

        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username


class LoginForm(AuthenticationForm):
    """Форма входа пользователя."""

    username = forms.EmailField(label="Email")
