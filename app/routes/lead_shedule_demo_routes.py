from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.models.master_users import MasterUser
from app.models.lead_demo_schedule import LeadDemoSchedule

from app.schemas.lead_demo_schemas import (
    ScheduleDemoCreate,
    DemoFeedbackUpdate,
    DemoResponse
)

router = APIRouter(
    prefix="/leads",
    tags=["Lead Demo Schedule"]
)

# ================================
# Schedule Demo
# ================================

@router.post(
    "/{lead_id}/schedule-demo",
    response_model=DemoResponse
)
def schedule_demo(
    lead_id: int,
    demo: ScheduleDemoCreate,
    db: Session = Depends(get_db)
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

    # Check User exists (employee)
    user = db.query(MasterUser).filter(
        MasterUser.id == demo.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Create Demo Schedule
    new_demo = LeadDemoSchedule(
        lead_id=lead_id,
        user_id=demo.user_id,
        scheduled_date=demo.scheduled_date,
        status="scheduled"
    )

    db.add(new_demo)

    # Update Lead Status
    lead.status = "demo_scheduled"

    db.commit()
    db.refresh(new_demo)

    return new_demo


# ================================
# Update Demo Feedback
# ================================

@router.put(
    "/demo-feedback/{demo_id}",
    response_model=DemoResponse
)
def update_demo_feedback(
    demo_id: int,
    feedback_data: DemoFeedbackUpdate,
    db: Session = Depends(get_db)
):

    # Check Demo exists
    demo = db.query(LeadDemoSchedule).filter(
        LeadDemoSchedule.id == demo_id
    ).first()

    if not demo:
        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    # Update Feedback
    demo.feedback = feedback_data.feedback
    demo.status = feedback_data.status

    demo.updated_at = datetime.utcnow()

    # Update Lead Status (optional but recommended)
    lead = db.query(MasterLead).filter(
        MasterLead.id == demo.lead_id
    ).first()

    if lead and feedback_data.status == "completed":
        lead.status = "demo_completed"

    db.commit()
    db.refresh(demo)

    return demo