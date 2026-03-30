from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional, Any


# Create Lead
class LeadCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    item_name: str
    address: str
    source: Optional[str] = None


# Update Lead
class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    item_name: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None


# Response Schema (Single Lead)
class LeadResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    item_name: str
    status: str
    address: Optional[str]
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class APIResponse(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[Any] = None