from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    phone: Optional[str] = ""
    email: Optional[str] = ""
    integral: Optional[int] = 0
    level: Optional[int] = 1
    is_member: Optional[bool] = False
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    integral: Optional[int] = None
    level: Optional[int] = None
    is_member: Optional[bool] = None
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    phone: str
    email: str
    integral: int
    level: int
    is_member: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
