from django.urls import path
from core.views import (
    create_room,
    join_room,
    list_public_rooms,
    list_user_rooms,
    list_rooms_created_by_user,
)

urlpatterns = [
    path("rooms/create/", create_room, name="create_room"),
    path("rooms/join/<uuid:pk>/", join_room, name="join_room"),
    path("rooms/public/", list_public_rooms, name="public-rooms"),
    path("rooms/member/", list_user_rooms, name="user-rooms"),
    path("rooms/host/", list_rooms_created_by_user, name="created-rooms"),
]
