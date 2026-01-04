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
    if not user:
        raise unauthorized("아이디가 존재하지 않습니다")
    elif not verify_password(password, user["hashed_password"]):
        raise unauthorized("비밀번호가 일치하지 않습니다")
    if not user["is_active"]:
        raise unauthorized("회원이 활성화되지 않았습니다")

    token = create_access_token(subject=str(user["id"]))
    print(f"Token: {token}")
    return user, token

async def check_email(db: asyncpg.Connection, *, email: str) -> dict:
    """Check if email is available"""
    user = await user_repo.get_by_email(db, email)
    print(f"User: {user}")
    if user is None:
        return {"available": True, "message": "Email is available"}
    else:
        return {"available": False, "message": "Email is already in use"}
