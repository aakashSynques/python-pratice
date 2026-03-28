from pydantic import BaseModel, EmailStr   
from typing import Optional
from datetime import datetime
# Request schema (Register)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    role_id: int
    address: Optional[str] = None
    password: str
    status: int 


class UserUpdate(BaseModel):

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    role_id: Optional[int] = None
    address: Optional[str] = None
    status: Optional[int] = None
# Response schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile: str
    address: Optional[str]
    role_id: int    
    status: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

#  Login Schema (NEW)
class UserLogin(BaseModel):
    email: EmailStr
    password: str