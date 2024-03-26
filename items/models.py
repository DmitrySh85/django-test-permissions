from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Item(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    description = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)


