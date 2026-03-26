from pydantic import BaseModel, EmailStr
from typing import Optional


class ClientUpdate(BaseModel):

    gst_number: Optional[str] = None

    contact_person: Optional[str] = None

    contact_mobile: Optional[str] = None

    address: Optional[str] = None

    status: Optional[str] = None


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

    status: str

    class Config:
        from_attributes = True