from fastapi import APIRouter, HTTPException

from ..deps import DBPool, CurrentUser
from ..models import UserUpdate, UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user(user_update: UserUpdate, current_user: CurrentUser, pool: DBPool):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            '''UPDATE users SET name = $1, updated_at = CURRENT_TIMESTAMP 
               WHERE id = $2 RETURNING id, name, created_at, updated_at''',
            user_update.name, current_user.id
        )
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(row)

@router.delete("/me", response_model=dict)
async def delete_user(current_user: CurrentUser, pool: DBPool):
    async with pool.acquire() as conn:
        await conn.execute('DELETE FROM users WHERE id = $1', current_user.id)
        return {"detail": "User deleted successfully"}
