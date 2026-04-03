from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Machine Schemas
class MachineCreate(BaseModel):
    name: str
    machine_code: str
    type: Optional[str] = None
    capicity: Optional[str] = None
    brand_name: Optional[str] = None
    description: Optional[str] = None

class MachineUpdate(BaseModel):
    name: Optional[str] = None
    machine_code: Optional[str] = None
    type: Optional[str] = None
    capicity: Optional[str] = None
    brand_name: Optional[str] = None
    description: Optional[str] = None

class MachineResponse(BaseModel):
    id: int
    name: str
    machine_code: str
    type: Optional[str]
    capicity: Optional[str]
    brand_name: Optional[str]
    description: Optional[str]
    status: int
    is_active: int
    created_at: datetime
    updated_at: datetime

class MachineResponseWithMessage(BaseModel):
    status: str
    message: str
    data: MachineResponse

    class Config:
        from_attributes = True


    # # Optional: include parts in response
    parts: Optional[List["MachinePartResponse"]] = []

    class Config:
        from_attributes = True



# Machine Part Schemas
class MachinePartCreate(BaseModel):
    name: str
    part_code: str
    machine_id: int

class MachinePartUpdate(BaseModel):
    name: Optional[str] = None
    part_code: Optional[str] = None
    machine_id: Optional[int] = None
    status: Optional[int] = None
    is_active: Optional[int] = None

class MachinePartResponse(BaseModel):
    id: int
    name: str
    part_code: str
    machine_id: int
    status: int        
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Fix forward reference for nested parts in MachineResponse
MachineResponse.update_forward_refs()