from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime 
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.models.master_users import MasterUser
from app.schemas.leads_schemas import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    APIResponse
)
from app.auth import get_current_user

router = APIRouter(
    prefix="/leads",
    tags=["Master Leads"]
)

# Create Lead
@router.post(
    "/create-leads",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED
)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):
    try:
        if lead.email:
            existing = db.query(MasterLead).filter(
                MasterLead.email == lead.email
            ).first()

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists"
                )
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
        return APIResponse(
            success=True,
            status=201,
            message="Lead created successfully",
            data=LeadResponse.model_validate(new_lead)
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Get All Leads

@router.get("/all-leads", response_model=List[LeadResponse])
def get_all_leads(
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
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



# Update Lead
@router.put(
    "/{lead_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK
)
def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):
    try:
        # Find Lead
        lead = db.query(MasterLead).filter(
            MasterLead.id == lead_id,
            MasterLead.is_active == 1
        ).first()

        # Not Found
        if not lead:
            raise HTTPException(
                status_code=404,
                detail="Lead not found"
            )

        # Update Fields
        update_data = lead_update.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(lead, key, value)

        # Update timestamp
        lead.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(lead)

        return APIResponse(
            success=True,
            status=200,
            message="Lead updated successfully",
            data=LeadResponse.model_validate(lead)
        )

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update lead: {str(e)}"
        )

# ===============================
# Soft Delete Lead
# ===============================
@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
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