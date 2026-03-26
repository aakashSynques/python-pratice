from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Create Lead
class LeadCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    address: str
    item_name: str
    source: Optional[str] = None
    address: Optional[str] = None


# Update Lead
class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None


# Response Schema
class LeadResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    status: str
    address: Optional[str]
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True