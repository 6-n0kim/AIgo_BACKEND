import asyncpg

from app.core.config import settings

# Global connection pool
_pool: asyncpg.Pool | None = None


async def init_db_pool() -> None:
    """Initialize database connection pool"""
    global _pool
    _pool = await asyncpg.create_pool(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        min_size=2,
        max_size=10,
        command_timeout=60,
    )
    print(f"데이터베이스 연결 성공: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


async def close_db_pool() -> None:
    """Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        print("데이터베이스 연결 종료")


def get_pool() -> asyncpg.Pool:
    """Get the database connection pool"""
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_db_pool() first.")
    return _pool


async def get_db() -> asyncpg.Connection:
    """
    Dependency to get database connection.
    Usage in FastAPI endpoint:
        async def endpoint(db: asyncpg.Connection = Depends(get_db)):
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn


async def init_schema() -> None:
    """Initialize database schema - create tables if they don't exist"""
    pool = get_pool()
    async with pool.acquire() as conn:
        print("데이터베이스 스키마 초기화 시작")

        # Create users table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(320) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create index on email for faster lookups
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
        """)

        # Create topic table (from schema.txt)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS topic (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NULL,
                summary TEXT NULL,
                CONSTRAINT uk_topic_slug UNIQUE (slug)
            )
        """)

        # Add comments for documentation
        await conn.execute("COMMENT ON TABLE topic IS '토픽'")
        await conn.execute("COMMENT ON COLUMN topic.id IS '토픽ID'")
        await conn.execute("COMMENT ON COLUMN topic.name IS '이름'")
        await conn.execute("COMMENT ON COLUMN topic.slug IS '약어'")
        await conn.execute("COMMENT ON COLUMN topic.summary IS '설명'")

        print("데이터베이스 스키마 초기화 완료 (users, topic)")
