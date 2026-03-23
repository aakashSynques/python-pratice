from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerResponse(BaseModel):
    id: int
    name: str
    shop_name: Optional[str]
    email: str
    mobile: str
    address: Optional[str]
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic V2 replacement for orm_mode