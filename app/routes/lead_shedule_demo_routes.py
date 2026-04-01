from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.models.master_users import MasterUser
from app.models.lead_demo_schedule import LeadDemoSchedule

from app.schemas.lead_demo_schemas import (
    ScheduleDemoCreate,
    DemoFeedbackUpdate,
    DemoResponse
)

from app.auth import get_current_user


router = APIRouter(
    prefix="/leads",
    tags=["Lead Demo Schedule"]
)


# ===================================================
# GET ALL DEMO SCHEDULES
# ===================================================

@router.get(
    "/demo/all",
    response_model=List[DemoResponse]
)
def get_all_demo_leads(
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    demos = db.query(
        LeadDemoSchedule
    ).order_by(
        LeadDemoSchedule.id.asc()
    ).all()

    return demos



# ===================================================
# GET SINGLE DEMO BY ID (Optional but useful)
# ===================================================

@router.get(
    "/demo/{demo_id}",
    response_model=DemoResponse
)
def get_demo_by_id(
    demo_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    demo = db.query(
        LeadDemoSchedule
    ).filter(
        LeadDemoSchedule.id == demo_id
    ).first()

    if not demo:
        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    return demo



# ===================================================
# SCHEDULE DEMO
# ===================================================

@router.post(
    "/{lead_id}/schedule-demo",
    response_model=DemoResponse
)
def schedule_demo(
    lead_id: int,
    demo: ScheduleDemoCreate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    # Check Lead exists
    lead = db.query(
        MasterLead
    ).filter(
        MasterLead.id == lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )


    # Check User exists
    user = db.query(
        MasterUser
    ).filter(
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
        status=1,
        feedback=None,
        created_at=datetime.utcnow()
    )

    db.add(new_demo)

    # Update Lead Status → Demo Scheduled
    lead.status = 2

    db.commit()
    db.refresh(new_demo)

    return new_demo



# ===================================================
# UPDATE DEMO FEEDBACK
# ===================================================

@router.put(
    "/demo-feedback/{demo_id}",
    response_model=DemoResponse
)
def update_demo_feedback(
    demo_id: int,
    feedback_data: DemoFeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    demo = db.query(
        LeadDemoSchedule
    ).filter(
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
    # Update Lead Status if Completed
    lead = db.query(
        MasterLead
    ).filter(
        MasterLead.id == demo.lead_id
    ).first()
    if lead and feedback_data.status == 3:
        lead.status = 3
    db.commit()
    db.refresh(demo)
    return demo



# ===================================================
# DELETE DEMO (Optional but recommended)
# ===================================================

@router.delete("/demo/{demo_id}")
def delete_demo(
    demo_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    demo = db.query(
        LeadDemoSchedule
    ).filter(
        LeadDemoSchedule.id == demo_id
    ).first()

    if not demo:
        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    db.delete(demo)
    db.commit()

    return {
        "message": "Demo deleted successfully"
    }