# Schema batata hai API ka response kaise dikhega.

#exaple 
# Database me 10 column ho sakte hain,
# lekin API me sirf 5 dikhane hain.


from pydantic import BaseModel
from datetime import datetime
from typing import Optional
# Base Schema
class RoleBase(BaseModel):
    role_name: str
    status: int = 1

# Create Role
class RoleCreate(RoleBase):
    pass

# Response Schema
class RoleResponse(RoleBase):
    role_id: int
    eat: Optional[datetime] = None   
    class Config:
        from_attributes = True