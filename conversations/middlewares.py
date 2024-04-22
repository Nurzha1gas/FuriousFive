from uuid import UUID

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware

from .models import Conversation, User

# Asynchronously retrieves a User by username, returning None if not found.
@database_sync_to_async
@database_sync_to_async
def get_user(username: str) -> User or None:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None

# Asynchronously retrieves a Conversation by its ID, returning None if not found.
@database_sync_to_async
@database_sync_to_async
def get_conversation(id: str) -> Conversation or None:
    try:
        return Conversation.objects.get(id=id)
    except Conversation.DoesNotExist:
        return None

# Validates if a given string is a properly formatted UUID version 4.
def validate_uuid(uuid_str: str) -> bool:
    uuid_str = uuid_str.lower().replace("-", "")

    try:
        value = UUID(uuid_str, version=4)
    except ValueError:
        return False

    return value.hex == uuid_str

# Middleware to inject a conversation object into the scope based on a valid UUID in the URL path.
class ConversationMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # get the conversation id from `scope`
        conversation_id = scope["path"].split("/")[-2]

        # checks if uuid is valid
        if not validate_uuid(conversation_id):
            scope["conversation"] = None
            return await self.inner(scope, receive, send)

        scope["conversation"] = await get_conversation(conversation_id)
        return await super().__call__(scope, receive, send)

# Middleware to inject a user object into the scope based on a token extracted from WebSocket subprotocols.
class UserMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])

        if b"sec-websocket-protocol" not in headers:
            scope["user"] = None
            return await self.inner(scope, receive, send)

        # converts from bytes to string
        subprotocols = headers.get(b"sec-websocket-protocol").decode("utf-8")
        if len(subprotocols.split(",")) != 2:
            scope["user"] = None
            return await self.inner(scope, receive, send)

        # split the subprotocol into two and get rid of whitespaces
        subprotocols = [protocol.strip() for protocol in subprotocols.split(",")]
        scope["user"] = await get_user(subprotocols[-1])

        return await super().__call__(scope, receive, send)

# Combines Cookie, Session, User, and Conversation middlewares to process incoming HTTP/WebSocket connections.
def ConversationUserSessionMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(UserMiddleware(ConversationMiddleware(inner))))
