# from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.database.db import Base
# # Master Machines Table
# class MasterMachines(Base):
#     __tablename__ = "master_machines"
#     __table_args__ = {"extend_existing": True}

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False, comment="Machine name / model")
#     machine_code = Column(String(50), unique=True, nullable=False, comment="Unique code / serial number")
#     type = Column(String(50), nullable=True, comment="Category / type of machine")
#     status = Column(Integer, default=1, comment="1=available, 0=unavailable")
#     is_active = Column(Integer, default=1, comment="1=active, 0=inactive")
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     # Relationship: Machine -> Parts
#     parts = relationship("MasterMachineParts", back_populates="machine")


# # Machine Parts Table
# class MasterMachineParts(Base):
#     __tablename__ = "machine_parts"
#     __table_args__ = {"extend_existing": True}

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False, comment="Part name / model")
#     part_code = Column(String(50), unique=True, nullable=False, comment="Unique part code / serial number")
#     # ForeignKey linking to MasterMachines
#     machine_id = Column(Integer, ForeignKey("master_machines.id"), nullable=False, comment="Associated machine id")  
#     status = Column(Integer, default=1, comment="1=available, 0=unavailable")
#     is_active = Column(Integer, default=1, comment="1=active, 0=inactive")
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     # Relationship: Part -> Machine
#     machine = relationship("MasterMachines", back_populates="parts")



   

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base


# Master Machines Table
class MasterMachines(Base):
    __tablename__ = "master_machines"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
        comment="Machine name / model"
    )

    machine_code = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="Unique code / serial number"
    )

    type = Column(
        String(50),
        nullable=True,
        comment="Category / type of machine"
    )

    status = Column(
        Integer,
        default=1,
        comment="1=available, 0=unavailable"
    )

    is_active = Column(
        Integer,
        default=1,
        comment="1=active, 0=inactive"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship: Machine -> Parts
    parts = relationship(
        "MasterMachineParts",
        back_populates="machine"
    )

    # ✅ ADD THIS (INSIDE CLASS)
    work_orders = relationship(
        "WorkOrders",
        back_populates="machine"
    )


# Machine Parts Table
class MasterMachineParts(Base):
    __tablename__ = "machine_parts"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
        comment="Part name / model"
    )

    part_code = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="Unique part code / serial number"
    )

    machine_id = Column(
        Integer,
        ForeignKey("master_machines.id"),
        nullable=False,
        comment="Associated machine id"
    )

    status = Column(
        Integer,
        default=1,
        comment="1=available, 0=unavailable"
    )

    is_active = Column(
        Integer,
        default=1,
        comment="1=active, 0=inactive"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship: Part -> Machine
    machine = relationship(
        "MasterMachines",
        back_populates="parts"
    )