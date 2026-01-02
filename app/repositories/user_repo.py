from datetime import datetime
import asyncpg


async def get_by_email(conn: asyncpg.Connection, email: str) -> dict | None:
    """Get user by email address"""
    row = await conn.fetchrow(
        "SELECT id, email, hashed_password, is_active, created_at FROM users WHERE email = $1",
        email
    )
    if row is None:
        return None
    return dict(row)


async def get_by_id(conn: asyncpg.Connection, user_id: int) -> dict | None:
    """Get user by ID"""
    row = await conn.fetchrow(
        "SELECT id, email, hashed_password, is_active, created_at FROM users WHERE id = $1",
        user_id
    )
    if row is None:
        return None
    return dict(row)


async def create(conn: asyncpg.Connection, *, email: str, hashed_password: str) -> dict:
    """Create a new user"""
    row = await conn.fetchrow(
        """
        INSERT INTO users (email, hashed_password, is_active, created_at)
        VALUES ($1, $2, TRUE, CURRENT_TIMESTAMP)
        RETURNING id, email, hashed_password, is_active, created_at
        """,
        email,
        hashed_password
    )
    return dict(row)
