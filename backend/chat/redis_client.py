import json
import redis.asyncio as redis
from django.conf import settings


class RedisClient:
    """Redis client for pub/sub streaming functionality."""

    def __init__(self):
        self.redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379')
        self._connection = None

    async def get_connection(self):
        """Get or create Redis connection."""
        if self._connection is None:
            self._connection = redis.from_url(self.redis_url, decode_responses=True)
        return self._connection

    async def publish_chunk(self, chat_uid: str, prompt_id: int, chunk: str):
        """Publish a text chunk to the chat's Redis channel."""
        connection = await self.get_connection()

        message = {
            'type': 'chunk',
            'prompt_id': prompt_id,
            'chunk': chunk,
        }

        channel = f"chat:{chat_uid}"
        await connection.publish(channel, json.dumps(message))

    async def publish_status(self, chat_uid: str, prompt_id: int, status: str):
        """Publish status update to the chat's Redis channel."""
        connection = await self.get_connection()

        message = {
            'type': 'status',
            'prompt_id': prompt_id,
            'status': status,
        }

        channel = f"chat:{chat_uid}"
        await connection.publish(channel, json.dumps(message))

    async def subscribe_to_chat(self, chat_uid: str):
        """Subscribe to a chat's Redis channel and yield messages."""
        connection = await self.get_connection()
        pubsub = connection.pubsub()

        channel = f"chat:{chat_uid}"
        await pubsub.subscribe(channel)

        try:
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    yield json.loads(message['data'])
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()

    async def close(self):
        """Close Redis connection."""
        if self._connection:
            await self._connection.close()


# Global Redis client instance
redis_client = RedisClient()
