from dataclasses import field
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(UserBase):
    name: Optional[str] = Field(None, max_length=100)
    email = Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=120)