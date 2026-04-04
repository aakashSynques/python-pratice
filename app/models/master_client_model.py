# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from datetime import datetime
# from app.database.db import Base
# from sqlalchemy.orm import relationship

# class MasterClient(Base):

#     __tablename__ = "master_clients"

#     id = Column(Integer, primary_key=True, index=True)

#     lead_id = Column(
#         Integer,
#         ForeignKey("master_leads.id"),
#         nullable=False
#     )

#     # Lead se copy honge
#     name = Column(String(100), nullable=False)

#     email = Column(
#         String(150),
#         nullable=True   # FIXED
#     )

#     mobile = Column(String(20), nullable=True)

#     address = Column(Text, nullable=True)

#     # Extra Client Fields
#     gst_number = Column(String(50), nullable=True)

#     contact_person = Column(String(100), nullable=True)

#     contact_mobile = Column(String(20), nullable=True)

#     status = Column(
#         String(50),
#         default="active"
#     )

#     created_at = Column(
#         DateTime,
#         default=datetime.utcnow
#     )

#     updated_at = Column(
#         DateTime,
#         default=datetime.utcnow,
#         onupdate=datetime.utcnow
#     )



# work_orders = relationship(
#     "WorkOrders",
#     back_populates="client"
# )


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from app.database.db import Base


class MasterClient(Base):

    __tablename__ = "master_clients"

    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(
        Integer,
        ForeignKey("master_leads.id"),
        nullable=False
    )

    # Lead se copy honge
    name = Column(String(100), nullable=False)

    email = Column(String(150), nullable=True)

    mobile = Column(String(20), nullable=True)

    address = Column(Text, nullable=True)

    gst_number = Column(String(50), nullable=True)

    contact_person = Column(String(100), nullable=True)

    contact_mobile = Column(String(20), nullable=True)

    client_status = Column( Integer, default=0, comment="0=active, 1=inactive" )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
