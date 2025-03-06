from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Group, GroupMember
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
def create_group(request):
    name = request.data.get("name")
    if Group.objects.filter(name=name).exists():
        return Response(
            {"error": "Room already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    room = Group.objects.create(name=name, host=request.user)
    return Response(
        {"message": "Room created", "room_name": room.name},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def join_room(request):
    room_id = request.data.get("room_id")
    try:
        room = Group.objects.get(id=room_id)
        GroupMember.objects.create(user=request.user, group=room)

        return Response(
            {"message": "User joined room", "room_name": room.name},
            status=status.HTTP_200_OK,
        )
    except (Group.DoesNotExist, User.DoesNotExist):
        return Response(
            {"error": "Invalid room or user"}, status=status.HTTP_400_BAD_REQUEST
        )
