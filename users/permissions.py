from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверяем, является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderator").exists()


class IsOwner(permissions.BasePermission):
    """Проверяем, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Проверяем, является ли пользователь владельцем объекта или админом"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser
