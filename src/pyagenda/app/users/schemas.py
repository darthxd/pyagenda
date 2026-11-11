from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Modelo base para user"""
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """Modelo para create do user"""
    password: str

class UserUpdate(BaseModel):
    """Modelo para update do user"""
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserGet(UserBase):
    """Modelo para get do user"""
    id: int
    password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
