from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated

from ..deps import DBPool, create_access_token

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    name: str

@router.post("/register", response_model=TokenResponse)
async def register_user(user: UserCreate, pool: DBPool):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            'INSERT INTO users (name) VALUES ($1) RETURNING id, name',
            user.name
        )
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        user_id = row['id']
        token = create_access_token(data={"sub": user_id})
        return {"access_token": token, "token_type": "bearer"}

@router.get("/token/{user_id}", response_model=TokenResponse)
async def get_token_for_user(user_id: int, pool: DBPool):
    """Utility endpoint as requested for testing, to easily get a token for user ID"""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT id FROM users WHERE id = $1', user_id)
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
            
        token = create_access_token(data={"sub": row['id']})
        return {"access_token": token, "token_type": "bearer"}
