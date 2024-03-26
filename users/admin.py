from django.contrib import admin
from .models import CustomUser, ItemPermissions

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ItemPermissions)