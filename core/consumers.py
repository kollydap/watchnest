import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from core.models import Room, Message, RoomMember
from channels.auth import get_user
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Check if the room exists
        try:
            self.room = await self.get_room(self.room_name)
        except Room.DoesNotExist:
            await self.close()
            return

        # Check if the user is part of the room (for private rooms)
        user = self.scope["user"]
        if self.room.is_private:
            is_member = await self.is_room_member(user, self.room)
            if not is_member:
                await self.close()
                return

        # Join the room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username")

        if not message or not username:
            return

        # Save the message in the database
        user = await self.get_user(username)
        if user:
            msg = await self.save_message(user, self.room, message)

        # Broadcast the message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @staticmethod
    async def get_user(username):
        return await User.objects.filter(username=username).afirst()

    @staticmethod
    async def get_room(room_name):
        return await Room.objects.filter(name=room_name).afirst()

    @staticmethod
    async def save_message(user, room, message):
        return await Message.objects.acreate(user=user, room=room, content=message)

    @staticmethod
    async def is_room_member(user, room):
        return await RoomMember.objects.filter(user=user, room=room).aexists()


class WatchPartyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Authenticate user and connect to the WebSocket."""
        self.user = await get_user(self.scope)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"watchparty_{self.room_name}"

        # If user is not authenticated, close connection but define room_group_name first
        # if isinstance(self.user, AnonymousUser):
        #     await self.close()
        #     return

        # Join the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Ensure disconnect does not fail if room_group_name is missing."""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        """Handle incoming messages and broadcast them."""
        data = json.loads(text_data)
        action = data.get("action")
        timestamp = data.get("timestamp", 0)

        if not action:
            return

        # Broadcast action to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_video_event",
                "action": action,
                "timestamp": timestamp,
                "username": self.user.username,
            },
        )

    async def broadcast_video_event(self, event):
        """Send video events to all group members."""
        await self.send(
            text_data=json.dumps(
                {
                    "action": event["action"],
                    "timestamp": event["timestamp"],
                    "username": event["username"],
                }
            )
        )
