from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum

class WorkOrderStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    completed = "completed"
    cancel = "cancel"

#  Client Basic Details (Nested)
class ClientBasic(BaseModel):
    id: int
    client_name: str = Field(alias="name")
    mobile_no: Optional[str] = Field( default=None, alias="mobile"  )
    email:str = Field(alias="email")
    address: str = Field(alias="address")
    class Config:
        from_attributes = True
        populate_by_name = True

#  Machine Basic Details (Nested)
class MachineBasic(BaseModel):
    id: int
    machine_name: str = Field(alias="name")
    machine_code: str = Field(alias="machine_code")
    machine_type : str = Field(alias="type")
    class Config:
        from_attributes = True
        populate_by_name = True

#  CREATE Work Order
class WorkOrderCreate(BaseModel):
    client_id: int
    machine_id: int
    quantity: Optional[int] = 1
    order_date: date
    status: Optional[WorkOrderStatus] = None
#  UPDATE Work Order
class WorkOrderUpdate(BaseModel):
    client_id: Optional[int] = None
    machine_id: Optional[int] = None
    quantity: Optional[int] = None
    order_date: Optional[date] = None
    status: Optional[str] = "pending"


# RESPONSE Work Order (Main)
class WorkOrderResponse(BaseModel):
    id: int
    work_order_no: str
    client_id: int
    machine_id: int
    quantity: int
    order_date: date
    status: str
    created_at: datetime
    # Nested Details
    client: Optional[ClientBasic]
    machine: Optional[MachineBasic]
    class Config:
        from_attributes = True
        populate_by_name = True