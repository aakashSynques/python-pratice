from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleDemoCreate(BaseModel):

    user_id: int
    scheduled_date: datetime


class DemoFeedbackUpdate(BaseModel):

    feedback: str
    status: int   # 2=Process, 3=Completed


class DemoResponse(BaseModel):
    id: int
    lead_id: int
    user_id: int
    scheduled_date: datetime
    feedback: Optional[str]
    status: int
    feedback_email_send_status: Optional[int] = None

    class Config:
        from_attributes = True


class DemoFeedbackSubmit(BaseModel):
    token: str
    general_feedback: Optional[str] = None
    employee_feedback: Optional[int] = None
    machine_feedback: Optional[int] = None









# ======================
# Lead Schema
# ======================

class LeadSchema(BaseModel):

    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]

    class Config:
        orm_mode = True



# ======================
# User Schema
# ======================

class UserSchema(BaseModel):

    id: int
    name: str
    email: str

    class Config:
        orm_mode = True



# ======================
# Feedback Schema
# ======================

class FeedbackSchema(BaseModel):

    general_feedback: Optional[str]
    employee_feedback: Optional[int]
    machine_feedback: Optional[int]

    class Config:
        orm_mode = True



# ======================
# Main Response
# ======================

class DemoFeedbackResponse(BaseModel):

    id: int
    lead_id: int
    user_id: int
    scheduled_date: datetime
    feedback_email_send_status: Optional[int]

    lead: Optional[LeadSchema]
    user: Optional[UserSchema]
    feedback: Optional[FeedbackSchema]

    class Config:
        orm_mode = True