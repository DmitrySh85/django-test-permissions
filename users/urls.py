from django.urls import path
from .views import(
    RegistrationView,
    LoginView,
    UpdateProfileRoleView,
    RetrieveUpdateItemPermissionsAPIView
)

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("role/", UpdateProfileRoleView.as_view()),
    path("permissions/<int:pk>/", RetrieveUpdateItemPermissionsAPIView.as_view())
]