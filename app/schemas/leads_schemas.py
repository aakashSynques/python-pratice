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
    lead_status: Optional[int] = None
    address: Optional[str] = None


# Response Schema 
class LeadResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    item_name: str
    lead_status: int
    address: Optional[str]
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class LeadStatusUpdate(BaseModel):
    lead_status: int   # 1=new, 2=contacted, 3=demo_scheduled, 4=converted


class APIResponse(BaseModel):
    success: bool
    status: int
    message: str
    data: Optional[Any] = None