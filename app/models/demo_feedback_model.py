from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from datetime import datetime
from app.database.db import Base
class LeadDemoFeedback(Base):
    __tablename__ = "lead_demo_feedback"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column( Integer, ForeignKey("master_leads.id"), nullable=False    )
    user_id = Column( Integer, ForeignKey("master_users.id"), nullable=False    )
    demo_schedule_id = Column(  Integer, ForeignKey("lead_demo_schedule.id"),   nullable=False   )
    general_feedback = Column(Text, nullable=True)
    employee_feedback = Column(Integer, nullable=True)
    machine_feedback = Column(Integer, nullable=True)
    status = Column(Integer, default=1)
    created_at = Column( DateTime, default=datetime.utcnow )
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    