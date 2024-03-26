from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

ROLE_CHOICES =[
    ("ADMIN", "admin"),
    ("MANAGER", "manager"),
    ("CUSTOMER", "customer")
]
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_role = models.CharField(choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about_me = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
class ItemPermissions(models.Model):

    """ Permission class for Item model objects """
    user = models.OneToOneField("CustomUser", related_name="item_permissions", on_delete=models.PROTECT)
    fetch_permission = models.BooleanField(default=True)
    list_fetch_permission = models.BooleanField(default=True)
    update_permission = models.BooleanField(default=False)
    partial_update_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)