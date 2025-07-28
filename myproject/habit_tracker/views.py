from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Habit
from .serializers import HabitSerializer


class HabitPagination(PageNumberPagination):
    """Пагинация по 5 элементов на страницу."""

    page_size = 5


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Habit."""

    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_permissions(self):
        """Настраиваем права доступа. Для публичного списка
        (list_public) — разрешаем всем. Для остальных действий — только
        авторизованные пользователи."""

        if self.action == "list_public":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Возвращает queryset в зависимости от действия. Для
        list_public — все публичные привычки. Для остальных — только
        привычки текущего пользователя."""

        if self.action == "list_public":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привычки ставим пользователя из запроса."""

        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public")
    def list_public(self, request):
        """Дополнительный endpoint для списка публичных привычек с пагинацией."""

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
