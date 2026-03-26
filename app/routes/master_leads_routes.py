from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.schemas.leads_schemas import (
    LeadCreate,
    LeadUpdate,
    LeadResponse
)

router = APIRouter(
    prefix="/leads",
    tags=["Master Leads"]
)

# ===============================
# Create Lead
# ===============================
@router.post("/create-leads", response_model=LeadResponse)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db)
):

    new_lead = MasterLead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        item_name=lead.item_name,
        source=lead.source,
        address=lead.address,
        status="new"
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead


# ===============================
# Get All Leads
# ===============================
@router.get("/all-leads", response_model=List[LeadResponse])
def get_all_leads(
    db: Session = Depends(get_db)
):

    leads = db.query(MasterLead).filter(
        MasterLead.is_active == 1
    ).all()

    return leads


# ===============================
# Get Lead By ID
# ===============================
@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = db.query(MasterLead).filter(
        MasterLead.id == lead_id,
        MasterLead.is_active == 1
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return lead


# ===============================
# Update Lead
# ===============================
@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db)
):

    lead = db.query(MasterLead).filter(
        MasterLead.id == lead_id,
        MasterLead.is_active == 1
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    for key, value in lead_update.dict(
        exclude_unset=True
    ).items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)

    return lead


# ===============================
# Soft Delete Lead
# ===============================
@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = db.query(MasterLead).filter(
        MasterLead.id == lead_id,
        MasterLead.is_active == 1
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    lead.is_active = 0

    db.commit()

    return {
        "message": "Lead deleted successfully"
    }