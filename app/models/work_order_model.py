from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base
class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, index=True)
    work_order_no = Column( String(50), unique=True, nullable=False )
    client_id = Column( Integer, ForeignKey("master_clients.id"), nullable=False )
    order_date = Column(Date, nullable=False)
    expected_installation_date = Column(Date)
    status = Column( String(50), default="Open" )
    remarks = Column(Text)
    document_path = Column(String(255))
    created_by = Column(Integer)
    created_at = Column( DateTime, default=datetime.utcnow )
    updated_at = Column( DateTime, default=datetime.utcnow, onupdate=datetime.utcnow )
    # Relationship
    machines = relationship(
        "WorkOrderMachine",
        back_populates="work_order",
        cascade="all, delete-orphan"
    )
 
# Work Order Machines Table 
class WorkOrderMachine(Base):
    __tablename__ = "work_order_machines"
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column( Integer, ForeignKey("work_orders.id"), nullable=False )
    machine_id = Column( Integer, ForeignKey("master_machines.id"), nullable=False )
    quantity = Column(Integer, default=1)
    remarks = Column(Text)
    work_order = relationship(
        "WorkOrder",
        back_populates="machines"
    )