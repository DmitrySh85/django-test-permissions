from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .serializers import ItemSerializer
from .models import Item
from .permissions import(
    HasItemFetchPermission,
    HasItemListFetchPermission,
    HasItemCreatePermission,
    HasItemUpdatePermission,
)

class ItemViewSet(viewsets.ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == "customer":
            return queryset.filter(user=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), HasItemFetchPermission()]
        elif self.action == 'list':
            return [IsAuthenticated(), HasItemListFetchPermission()]
        elif self.action == 'create':
            return [IsAuthenticated(), HasItemCreatePermission()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), HasItemUpdatePermission()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if not self.request.user.item_permissions.create_permission:
            raise PermissionDenied("You don't have permission to create items.")
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.item_permissions.update_permission:
            raise PermissionDenied("You don't have permission to update items.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.item_permissions.delete_permission:
            raise PermissionDenied("You don't have permission to delete items.")
        instance.delete()

