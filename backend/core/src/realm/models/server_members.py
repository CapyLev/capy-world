from django.db import models
from django.contrib.auth.models import User

from src.realm.models.server import Server


class ServerMember(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "server_member"
