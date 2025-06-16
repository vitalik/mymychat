from userprofile.models import UserProfile


async def get_userprofile(user):
    """Get or create user profile for the given user."""
    profile, created = await UserProfile.objects.aget_or_create(user=user)
    return profile


def get_userprofile_sync(user):
    """Get or create user profile for the given user (sync version)."""
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile
