from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional
class ClientUpdate(BaseModel):
    gst_number: Optional[str] = None
    contact_person: Optional[str] = None
    contact_mobile: Optional[str] = None
    address: Optional[str] = None
    client_status: Optional[int] = None

class ClientResponse(BaseModel):
    id: int
    lead_id: int
    name: str
    email: Optional[EmailStr]
    mobile: Optional[str]
    address: Optional[str]
    gst_number: Optional[str]
    contact_person: Optional[str]
    contact_mobile: Optional[str]
    client_status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True