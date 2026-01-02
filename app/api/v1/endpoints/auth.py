from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import asyncpg

from app.db.database import get_db
from app.schemas.user import UserCreate, Token, UserPublic
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(payload: UserCreate, db: asyncpg.Connection = Depends(get_db)):
    """Register a new user"""
    user, token = await auth_service.register(db, email=payload.email, password=payload.password)
    return {"access_token": token, "token_type": "bearer", "user": UserPublic(**user)}


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: asyncpg.Connection = Depends(get_db)):
    """Login user and return access token (OAuth2PasswordRequestForm uses 'username' field for email)"""
    user, token = await auth_service.login(db, email=form.username, password=form.password)
    return {"access_token": token, "token_type": "bearer", "user": UserPublic(**user)}
