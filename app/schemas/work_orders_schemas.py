from pydantic import BaseModel
from typing import List, Optional
from datetime import date
# Machine Create Schema
class WorkOrderMachineCreate(BaseModel):
    machine_id: int
    quantity: int
    remarks: Optional[str] = None

# Work Order Create

class WorkOrderCreate(BaseModel):
    client_id: int
    order_date: date
    expected_installation_date: Optional[date] = None
    remarks: Optional[str] = None
    created_by: Optional[int] = None
    machines: List[WorkOrderMachineCreate]

# Update Schema
class WorkOrderUpdate(BaseModel):
    expected_installation_date: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None

# Response Schema
class WorkOrderMachineResponse(BaseModel):
    id: int
    machine_id: int
    quantity: int
    class Config:
        from_attributes = True

class WorkOrderResponse(BaseModel):
    id: int
    work_order_no: str
    client_id: int
    order_date: date
    status: str
    machines: List[WorkOrderMachineResponse]

    class Config:
        from_attributes = True