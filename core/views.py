from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import Room, RoomMember
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_room(request):
    """
    Create a new chat room. Only authenticated users can create a room.
    """
    name = request.data.get("name")

    if Room.objects.filter(name=name).exists():
        return Response(
            {"error": "Room already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    room = Room.objects.create(name=name, host=request.user)

    return Response(
        {
            "message": "Room created successfully",
            "room_name": room.name,
            "room_id": room.id,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def join_room(request, pk):
    """
    Allows an authenticated user to join a chat room.
    """

    try:
        room = Room.objects.get(pk=pk)

        # Prevent duplicate room membership
        if RoomMember.objects.filter(user=request.user, room=room).exists():
            return Response(
                {"message": "User is already in the room"},
                status=status.HTTP_200_OK,
            )

        RoomMember.objects.create(user=request.user, room=room)

        return Response(
            {"message": "User joined room successfully", "room_name": room.name},
            status=status.HTTP_200_OK,
        )

    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def list_public_rooms(request):
    """Get all public rooms."""
    public_rooms = Room.objects.filter(is_private=False).values("id", "name", "host_id")
    return Response({"rooms": list(public_rooms)}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_user_rooms(request):
    """Get all rooms where the authenticated user is a member."""
    user_rooms = RoomMember.objects.filter(user=request.user).values(
        "room__id", "room__name", "room__host_id"
    )
    return Response({"rooms": list(user_rooms)}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_rooms_created_by_user(request):
    """Get all rooms created by the authenticated user."""
    created_rooms = Room.objects.filter(host=request.user).values("id", "name")
    return Response({"rooms": list(created_rooms)}, status=status.HTTP_200_OK)
