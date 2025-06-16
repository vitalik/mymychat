import json
import asyncio
from ninja import Router, Schema, ModelSchema
from django.shortcuts import get_object_or_404, aget_object_or_404
from django.http import StreamingHttpResponse
from chat.models import Chat, Prompt
from chat.redis_pubsub import pubsub
from auth.auth import query_token_auth


router = Router()


class ChatListSchema(ModelSchema):
    class Meta:
        model = Chat
        fields = ['id', 'uid', 'headline']


class PromptSchema(ModelSchema):
    class Meta:
        model = Prompt
        fields = ['id', 'status', 'result', 'input_text', 'output_text', 'created', 'modified']


class ChatDetailSchema(ModelSchema):
    prompts: list[PromptSchema]

    class Meta:
        model = Chat
        fields = ['id', 'uid', 'headline', 'model', 'timestamp']


class CreateChatSchema(Schema):
    input_text: str
    model: str
    system_prompt: str = ""


class ChatResponseSchema(Schema):
    uid: str
    headline: str


class CreatePromptSchema(Schema):
    input_text: str


@router.get("", response=list[ChatListSchema])
def list_chats(request):
    """List all chats for the authenticated user."""
    chats = Chat.objects.filter(user=request.auth)
    return [{"id": chat.id, "uid": chat.uid, "headline": chat.headline} for chat in chats]


@router.post("", response=ChatResponseSchema)
def create_chat(request, data: CreateChatSchema):
    """Create a new chat with initial prompt."""
    headline = data.input_text[:50]
    chat = Chat.objects.create(headline=headline, model=data.model, user=request.auth, system_prompt=data.system_prompt)

    Prompt.objects.create(chat=chat, input_text=data.input_text, status='queued')

    return {"uid": chat.uid, "headline": chat.headline}


@router.get("/{uid}", response=ChatDetailSchema)
def get_chat(request, uid: str):
    """Get chat details with all prompts for the authenticated user."""
    chat = get_object_or_404(Chat, uid=uid, user=request.auth)
    return chat


@router.post("/{uid}/prompts")
def new_prompt(request, uid: str, data: CreatePromptSchema):
    """Add a new prompt to an existing chat."""
    chat = get_object_or_404(Chat, uid=uid, user=request.auth)
    prompt = Prompt.objects.create(chat=chat, input_text=data.input_text, status='queued')
    return {"id": prompt.id, "status": prompt.status}


@router.post("/{uid}/share")
def share_chat(request, uid: str):
    """Share a chat publicly."""
    chat = get_object_or_404(Chat, uid=uid, user=request.auth)
    chat.is_shared = True
    chat.save()
    return {"uid": chat.uid, "is_shared": chat.is_shared}


@router.get("/{uid}/shared", response=ChatDetailSchema, auth=None)
def get_shared_chat(request, uid: str):
    """Get shared chat details without authentication."""
    chat = get_object_or_404(Chat, uid=uid, is_shared=True)
    return chat


@router.get("/{uid}/stream", auth=query_token_auth)
async def chat_stream(request, uid: str):
    """SSE endpoint for streaming chat updates."""

    # Ensure chat belongs to authenticated user (auth is automatic via QueryTokenAuth)
    await aget_object_or_404(Chat, uid=uid, user=request.auth)

    async def event_stream():
        """Async generator for SSE events."""
        try:
            # Send initial connection event
            yield f"data: {json.dumps({'type': 'connected', 'chat_uid': uid})}\n\n"

            # Subscribe to Redis channel and yield events
            async for message in pubsub.subscribe_to_chat(uid):
                # Format as SSE event
                event_data = json.dumps(message)
                yield f"data: {event_data}\n\n"

        except asyncio.CancelledError:
            # Client disconnected
            pass
        except Exception as e:
            # Send error event
            error_data = json.dumps({'type': 'error', 'message': str(e)})
            yield f"data: {error_data}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')

    # Set SSE headers
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    response['Access-Control-Allow-Origin'] = '*'  # Adjust for production
    response['Access-Control-Allow-Headers'] = 'Cache-Control'

    return response
