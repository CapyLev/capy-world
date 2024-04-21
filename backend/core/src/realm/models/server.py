from django.db import models
from django.contrib.auth.models import User


class Server(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="servers_images/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "server"
