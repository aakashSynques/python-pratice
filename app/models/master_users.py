from sqlalchemy import Column, Integer, String, Text, DateTime, SmallInteger, ForeignKey
from datetime import datetime
from app.database.db import Base
class MasterUser(Base):
    __tablename__ = "master_users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    mobile = Column(String(20), nullable=False)
    address = Column(Text, nullable=True)
    password = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey("master_roles.role_id"), nullable=False, comment="Reference to MasterRole")
    status = Column(Integer, default=1, comment="1=active, 0=inactive")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)