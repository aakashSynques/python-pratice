from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.db import Base


class WorkOrders(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)

    work_order_no = Column(
        String(50),
        unique=True,
        nullable=False
    )

    client_id = Column(
        Integer,
        ForeignKey("master_clients.id"),
        nullable=False
    )

    machine_id = Column(
        Integer,
        ForeignKey("master_machines.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )

    order_date = Column(Date)

    status = Column(
        Enum(
            "pending",
            "approved",
            "completed",
            name="work_order_status_enum"
        ),
        default="pending"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    # ✅ Relationships (class ke andar honi chahiye)
    client = relationship(
        "MasterClient",
        back_populates="work_orders"
    )

    machine = relationship(
        "MasterMachines",
        back_populates="work_orders"
    )