from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str

class UserUpdate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

class PublicationCreate(BaseModel):
    title: str
    text: str

class PublicationUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

class PublicationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    text: str
    created_at: datetime
    updated_at: datetime
