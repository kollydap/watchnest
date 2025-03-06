import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Group, Message, GroupMember

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'chat_{self.group_name}'
        
        # Check if the group exists
        try:
            self.group = await self.get_group(self.group_name)
        except Group.DoesNotExist:
            await self.close()
            return
        
        # Check if the user is part of the group (for private groups)
        user = self.scope['user']
        if self.group.is_private:
            is_member = await self.is_group_member(user, self.group)
            if not is_member:
                await self.close()
                return
        
        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')
        
        if not message or not username:
            return
        
        # Save the message in the database
        user = await self.get_user(username)
        if user:
            msg = await self.save_message(user, self.group, message)
        
        # Broadcast the message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))
    
    @staticmethod
    async def get_user(username):
        return await User.objects.filter(username=username).afirst()
    
    @staticmethod
    async def get_group(group_name):
        return await Group.objects.filter(name=group_name).afirst()
    
    @staticmethod
    async def save_message(user, group, message):
        return await Message.objects.acreate(user=user, group=group, content=message)
    
    @staticmethod
    async def is_group_member(user, group):
        return await GroupMember.objects.filter(user=user, group=group).aexists()


class WatchPartyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"watchparty_{self.room_name}"

        # Join the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data["action"]

        # Broadcast action to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_video_event",
                "action": action,
                "timestamp": data.get("timestamp", 0),
            },
        )

    async def broadcast_video_event(self, event):
        await self.send(
            text_data=json.dumps(
                {"action": event["action"], "timestamp": event["timestamp"]}
            )
        )
