from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объект только его автору.
    Остальным — только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение (GET, HEAD, OPTIONS) — всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение на изменение/удаление — только автору
        return obj.author == request.user
