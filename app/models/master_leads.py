from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database.db import Base

class MasterLead(Base):
    __tablename__ = "master_leads"
    __table_args__ = {"extend_existing": True}  # avoid duplicate table errors

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False,)
    email = Column(String(150), nullable=True, index=True )
    phone = Column(String(20), nullable=True, index=True )
    address = Column(String(50), nullable=True)
    item_name = Column(String(50), nullable=True)
    source = Column(String(50), nullable=True, comment="Lead source (referral, website, etc.)")
    lead_status = Column(Integer, default=1, comment="1=new, 2=contacted, 3=demo_scheduled, 4=converted")
    is_active = Column(Integer, default=1, comment="1=active, 0=inactive")
    created_at = Column(DateTime, default=datetime.utcnow, )
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, )