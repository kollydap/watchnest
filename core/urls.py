from django.urls import path
from core.views import create_room, join_room

urlpatterns = [
    path("rooms/create/", create_room, name="create_room"),
    path("rooms/join/<uuid:pk>/", join_room, name="join_room"),
]
