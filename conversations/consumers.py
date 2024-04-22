import json
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from redis import StrictRedis
from .models import Conversation, Message, User

# Connect to Redis using configuration specified in settings
redis = StrictRedis.from_url(url=settings.REDIS_URL, encoding="utf-8", decode_responses=True)

@database_sync_to_async
def validate_connection(conversation, user) -> None:
    """Ensure that the user is part of the conversation; deny access otherwise."""
    if not conversation or not user or user not in [conversation.creator, conversation.invitee]:
        raise DenyConnection()

@database_sync_to_async
def create_new_message(message: str, conversation_id: str, sender_username: str) -> dict:
    """Create a new message in the database and return its details."""
    conversation = Conversation.objects.get(id=conversation_id)
    sender = User.objects.get(username=sender_username)
    new_message = Message.objects.create(conversation=conversation, sender=sender, content=message)
    return {'message': new_message.content, 'sender': new_message.sender.username, 'timestamp': new_message.timestamp.isoformat()}

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Manage connection to the WebSocket, including validating user and joining room."""
        self.conversation_id = self.scope["url_route"]["kwargs"]["id"]
        self.conversation_room = f"conversation_{self.conversation_id}"
        self.user = self.scope["user"]
        conversation = self.scope["conversation"]
        await self.accept("Token")
        await validate_connection(conversation, self.user)
        redis.sadd(f"conversation:{self.conversation_id}", self.user.username)
        await self.channel_layer.group_add(self.conversation_room, self.channel_name)

    async def disconnect(self, code):
        """Manage disconnection from WebSocket and update online users."""
        redis.srem(f"conversation:{self.conversation_id}", self.user.username)
        await self.channel_layer.group_discard(self.conversation_room, self.channel_name)
        await self.channel_layer.group_send(
            self.conversation_room,
            {"type": "conversations.online_users", "data": list(redis.smembers(f"conversation:{self.conversation_id}"))}
        )

    async def receive(self, text_data, bytes_data=None):
        """Handle incoming messages from WebSocket and route them based on event type."""
        text_data_json = json.loads(text_data)
        event = text_data_json["event"]
        await self.channel_layer.group_send(self.conversation_room, {"type": event, "data": text_data_json})

    async def conversations_chat(self, event):
        """Handle chat messages by creating new messages and notifying clients."""
        if event['data']['action'] == "SEND":
            new_message_dict = await create_new_message(event['data']['message'], self.conversation_id, event['data']['sender'])
            await self.send(text_data=json.dumps({"event": "conversations.chat", "action": "RECEIVE", "data": new_message_dict}))

    async def conversations_video(self, event):
        """Handle video call actions such as call initiation, acceptance, rejection, and ending."""
        await self.send(text_data=json.dumps({"event": "conversations.video", **event['data']}))

    async def conversations_game(self, event):
        """Manage tic-tac-toe game actions like starting a game, making moves, and ending the game."""
        await self.send(text_data=json.dumps({"event": "conversations.game", **event['data']}))

    async def conversations_online_users(self, event):
        """Update clients with the current list of online users."""
        await self.send(text_data=json.dumps({"users": event['data'], "event": "conversations.online_users"}))
