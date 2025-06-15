from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja import Router, Schema
from .auth import create_jwt_token


router = Router()


class LoginSchema(Schema):
    email: str
    password: str


class RegisterSchema(Schema):
    email: str
    password: str


class AuthResponseSchema(Schema):
    token: str
    user_id: int
    email: str


class ErrorSchema(Schema):
    error: str


@router.post("/login", response={200: AuthResponseSchema, 400: ErrorSchema}, auth=None)
def login(request, data: LoginSchema):
    """Login with email and password, return JWT token."""
    # Use email as username for authentication
    user = authenticate(username=data.email, password=data.password)

    if user is None:
        return 400, {"error": "Invalid email or password"}

    token = create_jwt_token(user.id)

    return 200, {"token": token, "user_id": user.id, "email": user.email}


@router.post("/register", response={200: AuthResponseSchema, 400: ErrorSchema}, auth=None)
def register(request, data: RegisterSchema):
    """Register new user with email and password, return JWT token."""
    # Check if user already exists
    if User.objects.filter(username=data.email).exists():
        return 400, {"error": "User with this email already exists"}

    # Create new user (username = email)
    user = User.objects.create_user(username=data.email, email=data.email, password=data.password)

    token = create_jwt_token(user.id)

    return 200, {"token": token, "user_id": user.id, "email": user.email}


@router.get("/check")
def check_auth(request):
    """Check authentication status - returns 200 if authenticated, 401/403 if not."""
    return {"authenticated": True}
