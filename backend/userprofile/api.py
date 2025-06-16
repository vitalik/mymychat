from ninja import Router, Schema, ModelSchema
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from userprofile.models import UserProfile, SystemPrompt
from userprofile.utils import get_userprofile, get_userprofile_sync


router = Router()


class UserProfileSchema(Schema):
    openai_key: str = ""
    openrouter_key: str = ""


class UserProfileResponseSchema(Schema):
    openai_key_set: bool
    openrouter_key_set: bool


class SystemPromptSchema(ModelSchema):
    class Meta:
        model = SystemPrompt
        fields = ['id', 'text', 'created_at']


class CreateSystemPromptSchema(Schema):
    text: str


@router.get("/profile", response=UserProfileResponseSchema)
def get_profile(request):
    """Get user profile with masked API keys."""
    profile = get_userprofile_sync(request.auth)
    return {"openai_key_set": bool(profile.openai_key), "openrouter_key_set": bool(profile.openrouter_key)}


@router.patch("/profile")
def update_profile(request, data: UserProfileSchema):
    """Update user profile API keys."""
    profile = get_userprofile_sync(request.auth)

    if data.openai_key is not None:
        profile.openai_key = data.openai_key
    if data.openrouter_key is not None:
        profile.openrouter_key = data.openrouter_key

    profile.save()

    return {"openai_key_set": bool(profile.openai_key), "openrouter_key_set": bool(profile.openrouter_key)}


@router.get("/system-prompts", response=list[SystemPromptSchema])
def list_system_prompts(request):
    """List user's system prompts."""
    prompts = SystemPrompt.objects.filter(user=request.auth)
    return list(prompts)


@router.post("/system-prompts", response=SystemPromptSchema)
def create_system_prompt(request, data: CreateSystemPromptSchema):
    """Create a new system prompt."""
    prompt = SystemPrompt.objects.create(user=request.auth, text=data.text)
    return prompt


@router.put("/system-prompts/{prompt_id}", response=SystemPromptSchema)
def update_system_prompt(request, prompt_id: int, data: CreateSystemPromptSchema):
    """Update a system prompt."""
    prompt = get_object_or_404(SystemPrompt, id=prompt_id, user=request.auth)
    prompt.text = data.text
    prompt.save()
    return prompt


@router.delete("/system-prompts/{prompt_id}")
def delete_system_prompt(request, prompt_id: int):
    """Delete a system prompt."""
    prompt = get_object_or_404(SystemPrompt, id=prompt_id, user=request.auth)
    prompt.delete()
    return {"success": True}
