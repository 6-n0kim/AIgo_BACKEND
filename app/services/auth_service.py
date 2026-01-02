import asyncpg

from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import bad_request, unauthorized
from app.repositories import user_repo


async def register(db: asyncpg.Connection, *, email: str, password: str) -> tuple[dict, str]:
    """Register a new user"""
    existing = await user_repo.get_by_email(db, email)
    if existing:
        raise bad_request("Email already registered")

    user = await user_repo.create(db, email=email, hashed_password=hash_password(password))
    token = create_access_token(subject=str(user["id"]))
    return user, token


async def login(db: asyncpg.Connection, *, email: str, password: str) -> tuple[dict, str]:
    """Login user and return access token"""
    user = await user_repo.get_by_email(db, email)
    if not user or not verify_password(password, user["hashed_password"]):
        raise unauthorized("Incorrect email or password")
    if not user["is_active"]:
        raise unauthorized("Inactive user")

    token = create_access_token(subject=str(user["id"]))
    return user, token
