from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, String
from datetime import datetime
from app.database.db import Base
class LeadDemoSchedule(Base):
    __tablename__ = "lead_demo_schedule"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column( Integer, ForeignKey("master_leads.id"), nullable=False    )
    user_id = Column(  Integer, ForeignKey("master_users.id"),   nullable=False   )
    scheduled_date = Column(   DateTime,     nullable=False   )
    feedback = Column(Text, nullable=True)
    feedback_email_send_status = Column(Integer, default=0, comment="0=Not Sent, 1=Sent, counter")
    status = Column(Integer, default=1, comment="1=Scheduled, 2=Process, 3=Completed")
    created_at = Column( DateTime, default=datetime.utcnow )
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)