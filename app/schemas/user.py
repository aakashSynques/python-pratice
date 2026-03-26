# Schema batata hai API ka response kaise dikhega.

#exaple 
# Database me 10 column ho sakte hain,
# lekin API me sirf 5 dikhane hain.


from pydantic import BaseModel, EmailStr   
from typing import Optional
from datetime import datetime


# Request schema (Register)
class CustomerCreate(BaseModel):
    name: str
    shop_name: Optional[str] = None
    email: EmailStr
    mobile: str
    address: Optional[str] = None
    password: str


# Response schema
class CustomerResponse(BaseModel):
    id: int
    name: str
    shop_name: Optional[str]
    email: str
    mobile: str
    address: Optional[str]
    password: str
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#  Login Schema (NEW)
class CustomerLogin(BaseModel):
    email: EmailStr
    password: str