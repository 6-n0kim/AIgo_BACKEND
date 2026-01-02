from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.schemas.user import UserPublic

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user
