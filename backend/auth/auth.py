import jwt
from datetime import datetime, timedelta
from typing import Optional
from django.conf import settings
from django.contrib.auth.models import User
from ninja.security import APIKeyQuery, HttpBearer


def create_jwt_token(user_id: int) -> str:
    """Create JWT token with 90 days expiration."""
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=90)}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_jwt_token(token: str) -> dict | None:
    """Decode JWT token and return payload or None if invalid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


class BearerAuth(HttpBearer):
    """JWT authentication via Authorization header (Bearer token)."""

    def authenticate(self, request, token: str) -> Optional[User]:
        # Decode JWT token (token is already extracted from "Bearer " prefix)
        payload = decode_jwt_token(token)
        if not payload:
            return None

        # Get user from payload
        try:
            user = User.objects.get(id=payload['user_id'])
            return user
        except User.DoesNotExist:
            return None


class QueryTokenAuth(APIKeyQuery):
    """JWT authentication via query parameter (for SSE endpoints)."""

    param_name = "token"

    async def authenticate(self, request, key: Optional[str]) -> Optional[User]:
        if not key:
            return None

        # Decode JWT token
        payload = decode_jwt_token(key)
        if not payload:
            return None

        # Get user from payload
        try:
            user = await User.objects.aget(id=payload['user_id'])
            return user
        except User.DoesNotExist:
            return None


# Create the auth instances
jwt_bearer_auth = BearerAuth()
query_token_auth = QueryTokenAuth()
