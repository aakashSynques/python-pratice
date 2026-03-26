from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleDemoCreate(BaseModel):

    user_id: int
    scheduled_date: datetime


class DemoFeedbackUpdate(BaseModel):

    feedback: str
    status: str


class DemoResponse(BaseModel):

    id: int
    lead_id: int
    user_id: int
    scheduled_date: datetime
    feedback: Optional[str]
    status: str

    class Config:
        from_attributes = True