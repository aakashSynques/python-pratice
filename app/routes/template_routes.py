# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from pathlib import Path

# router = APIRouter()

# # Absolute path to templates
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# # ===========================
# # Root & Dashboard
# # ===========================
# @router.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("index.html", context={"request": request})

# @router.get("/dashboard", response_class=HTMLResponse)
# def dashboard(request: Request):
#     return templates.TemplateResponse("dashboard.html", context={"request": request})

# # ===========================
# # Lead Management
# # ===========================
# @router.get("/leads", response_class=HTMLResponse)
# def leads_list(request: Request):
#     return templates.TemplateResponse("leads_list.html", context={"request": request})

# @router.get("/leads/add", response_class=HTMLResponse)
# def leads_add(request: Request):
#     return templates.TemplateResponse("leads_add.html", context={"request": request})

# @router.get("/leads/schedule", response_class=HTMLResponse)
# def leads_schedule(request: Request):
#     return templates.TemplateResponse("leads_schedule_demo.html", context={"request": request})

# # ===========================
# # Client Management
# # ===========================
# @router.get("/clients", response_class=HTMLResponse)
# def clients_list(request: Request):
#     return templates.TemplateResponse("clients_list.html", context={"request": request})

# @router.get("/clients/add", response_class=HTMLResponse)
# def clients_add(request: Request):
#     return templates.TemplateResponse("clients_add.html", context={"request": request})

# # ===========================
# # Work Order Management
# # ===========================
# @router.get("/work-orders", response_class=HTMLResponse)
# def work_orders_list(request: Request):
#     return templates.TemplateResponse("work_orders_list.html", context={"request": request})

# @router.get("/work-orders/add", response_class=HTMLResponse)
# def work_orders_add(request: Request):
#     return templates.TemplateResponse("work_orders_add.html", context={"request": request})

# # ===========================
# # Machine Management
# # ===========================
# @router.get("/machines", response_class=HTMLResponse)
# def machines_list(request: Request):
#     return templates.TemplateResponse("machines_list.html", context={"request": request})

# @router.get("/machines/add", response_class=HTMLResponse)
# def machines_add(request: Request):
#     return templates.TemplateResponse("machines_add.html", context={"request": request})

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from fastapi import Depends, Request
import base64
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.master_leads import MasterLead
from app.models.lead_demo_schedule import LeadDemoSchedule
from app.models.master_users import MasterUser
from app.models.master_role import MasterRole
from app.models.demo_feedback_model import LeadDemoFeedback
from app.utils import validate_feedback_token
from app.schemas.lead_demo_schemas import DemoFeedbackSubmit
router = APIRouter()

# Absolute path to templates folder
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ===========================
# Root & Dashboard
# ===========================
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )



@router.get("/roles", response_class=HTMLResponse)
def roles(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="roles.html",
        context={"request": request}
    )

@router.get("/users", response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"request": request}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )

# ===========================
# Lead Management
# ===========================
@router.get("/leads", response_class=HTMLResponse)
def leads_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="leads_list.html",
        context={"request": request}
    )

@router.get("/leads/add", response_class=HTMLResponse)
def leads_add(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="leads_add.html",
        context={"request": request}
    )

@router.get("/leads_schedule_demo", response_class=HTMLResponse)
def leads_schedule(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="leads_schedule_demo.html",
        context={"request": request}
    )





# ===========================
# Client Management
# ===========================
@router.get("/clients", response_class=HTMLResponse)
def clients_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clients_list.html",
        context={"request": request}
    )

@router.get("/clients/add", response_class=HTMLResponse)
def clients_add(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clients_add.html",
        context={"request": request}
    )

# ===========================
# Work Order Management
# ===========================
@router.get("/work-orders", response_class=HTMLResponse)
def work_orders_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="work_orders_list.html",
        context={"request": request}
    )

@router.get("/work-orders/add", response_class=HTMLResponse)
def work_orders_add(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="work_orders_add.html",
        context={"request": request}
    )

# ===========================
# Machine Management
# ===========================
@router.get("/machines", response_class=HTMLResponse)
def machines_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="machines_list.html",
        context={"request": request}
    )

@router.get("/machines/add", response_class=HTMLResponse)
def machines_add(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="machines_add.html",
        context={"request": request}
    )





@router.get("/feedback/{token}", response_class=HTMLResponse)
def feedback_form(request: Request, token: str):
    # Validate token only, page will fetch details via JS API call
    token_data = validate_feedback_token(token)
    if not token_data:
        return templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={"request": request, "error": "Invalid or Expired Link"}
        )

    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={
            "request": request,
            "token": token,
            "error": None
        }
    )


@router.get("/api/feedback-data/{token}")
def feedback_data_api(token: str, db: Session = Depends(get_db)):
    token_data = validate_feedback_token(token)
    if not token_data:
        return {"success": False, "message": "Invalid or expired link"}
    demo_schedule_id = token_data.get("demo_schedule_id")
    if not demo_schedule_id:
        return {"success": False, "message": "demo_schedule_id not present in token"}
    
    demo = db.query(LeadDemoSchedule).filter(LeadDemoSchedule.id == demo_schedule_id).first()
    if not demo:
        return {"success": False, "message": "Demo schedule not found"}
    
    # Fetch lead data
    lead = db.query(MasterLead).filter(MasterLead.id == demo.lead_id).first()
    
    # Fetch user data with role
    user = db.query(MasterUser, MasterRole.role_name).join(MasterRole, MasterUser.role_id == MasterRole.role_id).filter(MasterUser.id == demo.user_id).first()
    
    return {
        "success": True,
        "data": {
            "demo": {
                "id": demo.id,
                "lead_id": demo.lead_id,
                "user_id": demo.user_id,
                "scheduled_date": demo.scheduled_date.isoformat() if demo.scheduled_date else None,
                "feedback": demo.feedback,
                "status": demo.status,
                "feedback_email_send_status": demo.feedback_email_send_status,
                "created_at": demo.created_at.isoformat() if demo.created_at else None,
                "updated_at": demo.updated_at.isoformat() if demo.updated_at else None
            },
            "lead": {
                "id": lead.id if lead else None,
                "name": lead.name if lead else None,
                "email": lead.email if lead else None,
                "phone": lead.phone if lead else None,
                "address": lead.address if lead else None,
                "item_name": lead.item_name if lead else None,
                "source": lead.source if lead else None,
                "lead_status": lead.lead_status if lead else None
            } if lead else None,
            "user": {
                "id": user[0].id if user else None,
                "name": user[0].name if user else None,
                "email": user[0].email if user else None,
                "phone": user[0].mobile if user else None,
                "role": user[1] if user else None
            } if user else None
        }
    }


@router.post("/api/submit-feedback")
def submit_feedback(feedback: DemoFeedbackSubmit, db: Session = Depends(get_db)):
    # Decode token and get demo schedule
    token_data = validate_feedback_token(feedback.token)
    if not token_data:
        return {"success": False, "message": "Invalid or expired token"}

    demo_schedule_id = token_data.get("demo_schedule_id")
    if not demo_schedule_id:
        return {"success": False, "message": "demo_schedule_id not present in token"}

    demo = db.query(LeadDemoSchedule).filter(LeadDemoSchedule.id == demo_schedule_id).first()
    if not demo:
        return {"success": False, "message": "Demo schedule not found"}

    try:
        new_feedback = LeadDemoFeedback(
            lead_id=demo.lead_id,
            user_id=demo.user_id,
            demo_schedule_id=demo.id,
            general_feedback=feedback.general_feedback,
            employee_feedback=feedback.employee_feedback,
            machine_feedback=feedback.machine_feedback,
            status=3
        )

        db.add(new_feedback)
        demo.feedback = feedback.general_feedback
        demo.status = 3
        db.commit()
        db.refresh(new_feedback)

        return {"success": True, "message": "Feedback submitted successfully", "data": {
            "feedback_id": new_feedback.id,
            "demo_schedule_id": new_feedback.demo_schedule_id
        }}

    except Exception as exc:
        db.rollback()
        # Log the exception in real app (e.g. logger.exception(exc))
        return {"success": False, "message": "Failed to submit feedback", "error": str(exc)}
