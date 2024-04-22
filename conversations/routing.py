from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/conversations/<id>/", consumers.ConversationConsumer.as_asgi()),
]
# Defines WebSocket URL patterns for handling real-time conversations using ConversationConsumer.
