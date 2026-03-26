from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models.master_users import MasterUser
from app.models.master_leads import MasterLead
from app.models.master_client_model import MasterClient

from app.schemas.client_schema import (
    ClientResponse,
    ClientUpdate
)
from app.auth import get_current_user

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


# =====================================
# Convert Lead → Client
# =====================================

@router.post("/convert/{lead_id}")
def convert_lead_to_client(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    # Check Lead exists
    lead = db.query(MasterLead).filter(
        MasterLead.id == lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    # Check already converted
    existing_client = db.query(
        MasterClient
    ).filter(
        MasterClient.lead_id == lead_id
    ).first()

    if existing_client:
        raise HTTPException(
            status_code=400,
            detail="Lead already converted"
        )

    # Create Client from Lead
    new_client = MasterClient(

        lead_id=lead.id,

        name=lead.name,
        email=lead.email,

        # IMPORTANT mapping
        mobile=lead.phone,

        address=lead.address,

        status="active"
    )

    db.add(new_client)

    # Update Lead Status
    lead.status = "converted"

    db.commit()
    db.refresh(new_client)

    return {
        "message": "Lead converted to Client successfully",
        "client_id": new_client.id
    }


# =====================================
# GET All Clients
# =====================================

@router.get(
    "/",
    response_model=List[ClientResponse]
)
def get_clients(
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    clients = db.query(
        MasterClient
    ).all()

    return clients


# =====================================
# GET Client by ID
# =====================================

@router.get(
    "/{client_id}",
    response_model=ClientResponse
)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    client = db.query(
        MasterClient
    ).filter(
        MasterClient.id == client_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return client


# =====================================
# UPDATE Client
# =====================================

@router.put(
    "/{client_id}",
    response_model=ClientResponse
)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    client = db.query(
        MasterClient
    ).filter(
        MasterClient.id == client_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    for key, value in client_data.dict(
        exclude_unset=True
    ).items():

        setattr(client, key, value)

    db.commit()
    db.refresh(client)

    return client