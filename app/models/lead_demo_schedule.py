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
    status = Column(     String(50),  default="scheduled" )
    created_at = Column( DateTime, default=datetime.utcnow )
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)