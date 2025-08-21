from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Пользователь может редактировать только свои привычки.
    Публичные привычки доступны только для чтения всем."""

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем для публичных привычек
        if request.method in permissions.SAFE_METHODS and obj.is_public:
            return True
        # Для изменений — только владелец
        return obj.user == request.user
