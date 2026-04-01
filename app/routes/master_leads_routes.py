from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime 
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy import outerjoin
from typing import List
from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.models.master_users import MasterUser
from app.models.lead_demo_schedule import LeadDemoSchedule
from app.schemas.leads_schemas import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadStatusUpdate,
    APIResponse
)
from app.auth import get_current_user
from app.utils import generate_feedback_token, send_feedback_email

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
            address=lead.address
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

# @router.get("/all-leads", response_model=List[LeadResponse])
# def get_all_leads(
#     db: Session = Depends(get_db),
#     current_user: MasterUser = Depends(get_current_user)
# ):

#     leads = db.query(MasterLead).filter(
#         MasterLead.is_active == 1
#     ).all()

#     return leads


@router.get("/all-leads")
def get_all_leads(
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    results = db.query(
        MasterLead,
        LeadDemoSchedule
    ).outerjoin(
        LeadDemoSchedule,
        MasterLead.id == LeadDemoSchedule.lead_id
    ).filter(
        MasterLead.is_active == 1
    ).order_by(
        MasterLead.id.desc()
    ).all()

    leads_dict = {}

    for lead, demo in results:

        if lead.id not in leads_dict:

            leads_dict[lead.id] = {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "source": lead.source,
                "item_name": lead.item_name,
                "lead_status": lead.lead_status,
                "address": lead.address,
                "is_active": lead.is_active,
                "created_at": lead.created_at,
                "updated_at": lead.updated_at,
                "demos": []
            }

        if demo:
            leads_dict[lead.id]["demos"].append({
                "id": demo.id,
                "user_id": demo.user_id,
                "scheduled_date": demo.scheduled_date,
                "feedback": demo.feedback,
                "status": demo.status
            })

    return list(leads_dict.values())


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




# ===============================
# Update Lead Status Only
# ===============================
VALID_LEAD_STATUS = [1, 2, 3, 4, 5]


@router.patch(
    "/{lead_id}/status",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK
)
def update_lead_status(
    lead_id: int,
    status_data: LeadStatusUpdate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    try:
        # Find Lead
        lead = db.query(MasterLead).filter(
            MasterLead.id == lead_id,
            MasterLead.is_active == 1
        ).first()

        if not lead:
            raise HTTPException(
                status_code=404,
                detail="Lead not found"
            )

        # Validate Status
        if status_data.lead_status not in VALID_LEAD_STATUS:
            raise HTTPException(
                status_code=400,
                detail="Invalid status value"
            )

        # Update Status
        lead.lead_status = status_data.lead_status
        lead.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(lead)

        return APIResponse(
            success=True,
            status=200,
            message="Lead status updated successfully",
            data=LeadResponse.model_validate(lead)
        )

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to update status: {str(e)}"
        )


# Send Feedback Link
@router.post(
    "/send-feedback/{lead_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK
)
def send_feedback_link(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):
    try:
        # Fetch lead details
        lead = db.query(MasterLead).filter(MasterLead.id == lead_id).first()
        if not lead:
            raise HTTPException(
                status_code=404,
                detail="Lead not found"
            )

        if not lead.email:
            raise HTTPException(
                status_code=400,
                detail="Lead does not have an email address"
            )

        # Generate encrypted token
        token = generate_feedback_token(lead.id, lead.email)

        # Generate feedback URL
        feedback_url = f"http://localhost:8000/feedback/{token}"

        # Send email
        email_sent = send_feedback_email(lead.email, lead.name, feedback_url)
        if not email_sent:
            raise HTTPException(
                status_code=500,
                detail="Failed to send email"
            )

        return APIResponse(
            success=True,
            message="Feedback email sent successfully"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send feedback email: {str(e)}"
        )