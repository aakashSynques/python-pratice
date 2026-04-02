from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from starlette import status
from app.utils import send_feedback_link_for_lead

from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.models.master_users import MasterUser
from app.models.lead_demo_schedule import LeadDemoSchedule
from app.models.demo_feedback_model import LeadDemoFeedback

from app.schemas.lead_demo_schemas import (
    ScheduleDemoCreate,
    DemoFeedbackUpdate,
    DemoResponse,
    DemoFeedbackResponse
)


from app.schemas.leads_schemas import (
    APIResponse
)

from app.auth import get_current_user


router = APIRouter(
    prefix="/leads",
    tags=["Lead Demo Schedule"]
)


# ===================================================
# GET ALL DEMO SCHEDULES
# ===================================================

# @router.get(
#     "/demo/all",
#     response_model=List[DemoResponse]
# )
# def get_all_demo_leads(
#     db: Session = Depends(get_db),
#     current_user: MasterUser = Depends(get_current_user)
# ):

#     demos = db.query(
#         LeadDemoSchedule
#     ).order_by(
#         LeadDemoSchedule.id.asc()
#     ).all()

#     return demos
@router.get(
    "/demo/all",
    response_model=List[DemoFeedbackResponse]
)
def get_all_demo_leads(
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    schedules = db.query(
        LeadDemoSchedule
    ).order_by(
        LeadDemoSchedule.id.asc()
    ).all()


    response = []

    for schedule in schedules:

        # Get Lead
        lead = db.query(
            MasterLead
        ).filter(
            MasterLead.id ==
            schedule.lead_id
        ).first()

        # Get User
        user = db.query(
            MasterUser
        ).filter(
            MasterUser.id ==
            schedule.user_id
        ).first()

        # Get Feedback
        feedback = db.query(
            LeadDemoFeedback
        ).filter(
            LeadDemoFeedback.demo_schedule_id ==
            schedule.id
        ).first()


        response.append({

            "id": schedule.id,
            "lead_id": schedule.lead_id,
            "user_id": schedule.user_id,
            "scheduled_date": schedule.scheduled_date,
            "feedback_email_send_status":
                schedule.feedback_email_send_status,

            "lead": lead,
            "user": user,
            "feedback": feedback

        })


    return response

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


@router.post("/send-feedback-email/{demo_id}")
def send_feedback_email(
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

    # Get Lead Email
    lead = db.query(
        MasterLead
    ).filter(
        MasterLead.id == demo.lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    # ✅ Send Email
    send_feedback_link_for_lead(
        demo_schedule_id=demo.id,
        lead_email=lead.email,
        lead_name=lead.name
    )

    # ✅ Increment Counter
    if demo.feedback_email_send_status is None:
        demo.feedback_email_send_status = 1
    else:
        demo.feedback_email_send_status += 1

    demo.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(demo)

    return {
        "message": "Feedback email sent successfully",
        "email_send_count": demo.feedback_email_send_status
    }



# *** NOTE: send-feedback endpoint is now handled in master_leads_routes.py to avoid duplicate route conflicts ***
