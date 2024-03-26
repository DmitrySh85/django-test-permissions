from rest_framework.permissions import BasePermission

from users.models import ItemPermissions


class HasItemFetchPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            return user.item_permissions.fetch_permission
        except ItemPermissions.DoesNotExist:
            return False


class HasItemListFetchPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            return user.item_permissions.list_fetch_permission
        except ItemPermissions.DoesNotExist:
            return False


class HasItemCreatePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        try:
            return user.item_permissions.create_permission
        except ItemPermissions.DoesNotExist:
            return False


class HasItemUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return user.item_permissions.update_permission
        except ItemPermissions.DoesNotExist:
            return False