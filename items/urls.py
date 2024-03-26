from django.urls import path
from .views import ItemViewSet


urlpatterns = [
    path("item/", ItemViewSet.as_view({
        "get": "list", "post": "create",
    })),
    path("item/<int:pk>/", ItemViewSet.as_view({
        "get": "retrieve", "delete": "destroy", "put": "update"
    })),
]