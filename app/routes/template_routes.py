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

@router.get("/leads/schedule", response_class=HTMLResponse)
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