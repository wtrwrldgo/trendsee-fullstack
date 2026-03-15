import os
import asyncpg
import redis.asyncio as aioredis
from typing import Optional
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://trendsee:trendseepassword@localhost:5432/trendsee")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class DBConnection:
    pool: Optional[asyncpg.Pool] = None
    redis: Optional[aioredis.Redis] = None

db_state = DBConnection()

async def init_db():
    db_state.pool = await asyncpg.create_pool(DATABASE_URL)
    db_state.redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    
    # Init tables
    async with db_state.pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS publications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

async def get_db_pool() -> asyncpg.Pool:
    return db_state.pool

async def get_redis() -> aioredis.Redis:
    return db_state.redis
