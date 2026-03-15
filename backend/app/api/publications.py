import asyncio
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import List

from ..deps import DBPool, CurrentUser, RedisClient
from ..models import PublicationCreate, PublicationUpdate, PublicationResponse

router = APIRouter()

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@router.post("/", response_model=PublicationResponse)
async def create_publication(
    pub: PublicationCreate, 
    current_user: CurrentUser, 
    pool: DBPool,
    redis: RedisClient
):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            '''INSERT INTO publications (user_id, title, text) 
               VALUES ($1, $2, $3) 
               RETURNING id, user_id, title, text, created_at, updated_at''',
            current_user.id, pub.title, pub.text
        )
        if not row:
            raise HTTPException(status_code=500, detail="Failed to create publication")
            
        pub_dict = dict(row)
        
        # Cache the hot post in Redis for 10 minutes (600 seconds)
        cache_key = f"pub:{pub_dict['id']}"
        await redis.setex(cache_key, 600, json.dumps(pub_dict, default=serialize_datetime))
        
        # Also invalidate user's publication list cache if exists (optional but good practice)
        # Assuming we cache individual items for the list
        
        return pub_dict

@router.put("/{pub_id}", response_model=PublicationResponse)
async def update_publication(
    pub_id: int, 
    pub_update: PublicationUpdate, 
    current_user: CurrentUser, 
    pool: DBPool,
    redis: RedisClient
):
    async with pool.acquire() as conn:
        # Check ownership
        check = await conn.fetchrow('SELECT user_id FROM publications WHERE id = $1', pub_id)
        if not check:
            raise HTTPException(status_code=404, detail="Publication not found")
        if check['user_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this publication")
            
        # Build update query dynamically based on provided fields
        fields = []
        values = []
        idx = 1
        
        if pub_update.title is not None:
            fields.append(f"title = ${idx}")
            values.append(pub_update.title)
            idx += 1
        if pub_update.text is not None:
            fields.append(f"text = ${idx}")
            values.append(pub_update.text)
            idx += 1
            
        if not fields:
            # Nothing to update, just return current
            row = await conn.fetchrow('SELECT * FROM publications WHERE id = $1', pub_id)
            return dict(row)
            
        fields.append("updated_at = CURRENT_TIMESTAMP")
        
        query = f'''UPDATE publications SET {", ".join(fields)} 
                   WHERE id = ${idx} RETURNING id, user_id, title, text, created_at, updated_at'''
        values.append(pub_id)
        
        row = await conn.fetchrow(query, *values)
        pub_dict = dict(row)
        
        # Update cache if it exists, or just set it (fresh for 10 mins again)
        cache_key = f"pub:{pub_id}"
        await redis.setex(cache_key, 600, json.dumps(pub_dict, default=serialize_datetime))
        
        return pub_dict

@router.delete("/{pub_id}", response_model=dict)
async def delete_publication(
    pub_id: int, 
    current_user: CurrentUser, 
    pool: DBPool,
    redis: RedisClient
):
    async with pool.acquire() as conn:
        check = await conn.fetchrow('SELECT user_id FROM publications WHERE id = $1', pub_id)
        if not check:
            raise HTTPException(status_code=404, detail="Publication not found")
        if check['user_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this publication")
            
        await conn.execute('DELETE FROM publications WHERE id = $1', pub_id)
        
        # Remove from cache
        await redis.delete(f"pub:{pub_id}")
        
        return {"detail": "Publication deleted successfully"}

@router.get("/user/{user_id}", response_model=List[PublicationResponse])
async def get_user_publications(
    user_id: int, 
    pool: DBPool, 
    redis: RedisClient,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """
    Get publications for a user.
    Simulates a 2s delay if fetching from Postgres.
    """
    async with pool.acquire() as conn:
        # First get DB IDs to check Redis
        # Ordered by created_at DESC
        rows = await conn.fetch(
            'SELECT id FROM publications WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3',
            user_id, limit, offset
        )
        
        if not rows:
            return []
            
        ids = [row['id'] for row in rows]
        
        results = []
        db_fetch_needed = []
        
        # Try to get from Redis
        for pub_id in ids:
            cached = await redis.get(f"pub:{pub_id}")
            if cached:
                # Need to convert string dates back to datetime for pydantic
                data = json.loads(cached)
                data['created_at'] = datetime.fromisoformat(data['created_at'])
                data['updated_at'] = datetime.fromisoformat(data['updated_at'])
                results.append(data)
            else:
                db_fetch_needed.append(pub_id)
                
        # If any are missing from cache, fetch from PG with a 2-second sleep
        if db_fetch_needed:
            # Requirement: "При запросе через Postgres сделай искусственную задержку в 2 секунды (sleep)"
            await asyncio.sleep(2)
            
            placeholders = ', '.join(f'${i+1}' for i in range(len(db_fetch_needed)))
            query = f'SELECT id, user_id, title, text, created_at, updated_at FROM publications WHERE id IN ({placeholders})'
            
            pg_rows = await conn.fetch(query, *db_fetch_needed)
            
            for row in pg_rows:
                pub_dict = dict(row)
                results.append(pub_dict)
                
        # Sort results by created_at descending (since we mixed redis and pg results)
        results.sort(key=lambda x: x['created_at'], reverse=True)
        
        return results
