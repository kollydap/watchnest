from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
