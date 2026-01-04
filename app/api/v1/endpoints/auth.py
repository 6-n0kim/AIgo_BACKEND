from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
import asyncpg

from app.db.database import get_db
from app.schemas.user import UserCreate, Token, UserPublic, EmailCheckResponse
from app.services import auth_service
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(payload: UserCreate, response: Response, db: asyncpg.Connection = Depends(get_db)):
    """Register a new user"""
    user, token = await auth_service.register(db, email=payload.email, password=payload.password)

    # Set HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert minutes to seconds
    )

    return {"access_token": token, "token_type": "bearer", "user": UserPublic(**user)}


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), response: Response = None, db: asyncpg.Connection = Depends(get_db)):
    """Login user and return access token (OAuth2PasswordRequestForm uses 'username' field for email)"""
    print(f"Login attempt: {form}")
    user, token = await auth_service.login(db, email=form.username, password=form.password)

    # Set HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert minutes to seconds
    )

    return {"access_token": token, "token_type": "bearer", "user": UserPublic(**user)}

@router.post("/logout")
async def logout(response: Response):
    """Logout user by clearing the access token cookie"""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}


@router.get("/check-email", response_model=EmailCheckResponse)
async def check_email(email: str, db: asyncpg.Connection = Depends(get_db)):
    """Check if email is available"""
    user = await auth_service.check_email(db, email=email)
    return {"available": user["available"], "message": user["message"]}