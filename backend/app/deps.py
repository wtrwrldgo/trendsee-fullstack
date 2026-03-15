import os
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from asyncpg import Pool
import redis.asyncio as aioredis
from typing import Annotated

from .db import get_db_pool, get_redis
from .models import UserResponse

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440) # 24 hours
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    pool: Pool = Depends(get_db_pool)
) -> UserResponse:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT id, name, created_at, updated_at FROM users WHERE id = $1', user_id)
        if row is None:
            raise credentials_exception
            
    return UserResponse(**dict(row))

CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
DBPool = Annotated[Pool, Depends(get_db_pool)]
RedisClient = Annotated[aioredis.Redis, Depends(get_redis)]
