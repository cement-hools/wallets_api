from rest_framework.permissions import (BasePermission, SAFE_METHODS)


class IsAdminUserOrReadOnly(BasePermission):
    """Права админа."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_staff and request.user.is_superuser)


class WalletIsOwnerOrAdmin(BasePermission):
    """Права для владелеца и админа."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user
                or request.user.is_staff or request.user.is_superuser)


class TransactionsIsOwnerOrAdmin(BasePermission):
    """Права для владелеца и админа."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.wallet.owner == request.user
                or request.user.is_staff or request.user.is_superuser)
