from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room, UserSession
from django.contrib.auth.models import User

@api_view(["POST"])
def create_room(request):
    name = request.data.get("name")
    if Room.objects.filter(name=name).exists():
        return Response({"error": "Room already exists"}, status=status.HTTP_400_BAD_REQUEST)

    room = Room.objects.create(name=name)
    return Response({"message": "Room created", "room_id": room.id}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def join_room(request):
    room_id = request.data.get("room_id")
    user_id = request.data.get("user_id")

    try:
        room = Room.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        UserSession.objects.create(user=user, room=room)
        return Response({"message": "User joined room"}, status=status.HTTP_200_OK)
    except (Room.DoesNotExist, User.DoesNotExist):
        return Response({"error": "Invalid room or user"}, status=status.HTTP_400_BAD_REQUEST)
