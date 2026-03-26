from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.db import Base
class MasterRole(Base):
    __tablename__ = "master_roles"
    __table_args__ = {"extend_existing": True}
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False, unique=True)
    status = Column(Integer, default=1, comment="1=active, 0=inactive")
    eby = Column(Integer, default=0)
    eat = Column( DateTime, server_default=func.now()
    )
