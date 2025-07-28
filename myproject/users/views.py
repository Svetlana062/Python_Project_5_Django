from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CustomUserSerializer,
    RegistrationSerializer,
    UserFullSerializer,
    UserPublicSerializer,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели CustomUser."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # сериализатор для преобразования данных

    def get_permissions(self):
        if self.action == "create":
            # регистрация — открыта всем
            permission_classes = []
        elif self.action in ["retrieve", "update", "partial_update"]:
            # просмотр и редактирование своих данных
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            # остальные действия (например, list, destroy) — только админ
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserProfileView(generics.RetrieveAPIView):
    """View для профиля пользователя."""

    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        # Используем сериализатор для просмотра своего профиля
        if self.request.user.is_authenticated:
            if self.request.method in ["PUT", "PATCH"]:
                return UserFullSerializer
            # если запрашивается свой профиль
            if self.get_object() == self.request.user:
                return UserFullSerializer
        # Иначе — публичный сериализатор
        return UserPublicSerializer

    def get_object(self):
        # Получение объекта по pk из URL или текущего пользователя
        pk = self.kwargs.get("pk")
        if pk:
            return super().get_object()
        else:
            # если pk не передан — возвращаем текущего пользователя
            return self.request.user

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            # Только владелец может редактировать
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class RegisterAPIView(APIView):
    """APIView для регистрации новых пользователей."""

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
