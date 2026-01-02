from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import asyncpg

from app.core.exceptions import unauthorized
from app.core.security import decode_token
from app.db.database import get_db
from app.repositories import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    db: asyncpg.Connection = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> dict:
    """Validate JWT token and return current user"""
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise unauthorized("Invalid token")

    user = await user_repo.get_by_id(db, user_id)
    if not user:
        raise unauthorized("User not found")
    if not user["is_active"]:
        raise unauthorized("Inactive user")
    return user
