# Model database table ko represent karta hai. (Model kya karta hai (Database ka Structure))


from sqlalchemy import Column, Integer, String, Text, DateTime, SmallInteger
from datetime import datetime
from app.database.db import Base

class MasterCustomer(Base):
    __tablename__ = "master_customers"
    __table_args__ = {"extend_existing": True}  # Avoid duplicate table error

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    shop_name = Column(String(150))
    email = Column(String(150), nullable=False, unique=True)
    mobile = Column(String(20), nullable=False)
    address = Column(Text)
    password = Column(String(200), nullable=False)
    status = Column(SmallInteger, default=1, comment="1=active,0=inactive")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)