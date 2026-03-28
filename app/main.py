# # entry points

# from fastapi import FastAPI
# from app.routes import user
# from app.database.db import Base, engine

# app = FastAPI(title="Customer API", version="1.0")

# # Include user routes
# app.include_router(user.router)

# # Root endpoint
# @app.get("/")
# def root():
#     return {"message": "Go to /customers/ to see the customer list"}

# # Create tables only when running directly
# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)


# app/main.py
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from app.routes import master_users_routes

# from app.routes import master_role_routes
# from app.routes import master_leads_routes
# from app.routes import lead_shedule_demo_routes
# from app.routes import master_client_routes
# from app.routes import master_machine_and_part_routes
# from app.routes import work_orders_routes

# from app.database.db import Base, engine
# # FastAPI instance
# app = FastAPI(title="Tea Vending ERP API", version="1.0")
# # Include Routers
# app.include_router(master_users_routes.router)
# app.include_router(master_role_routes.router)
# app.include_router(master_leads_routes.router)
# app.include_router(lead_shedule_demo_routes.router)
# app.include_router(master_client_routes.router)
# app.include_router(master_machine_and_part_routes.router)
# app.include_router(work_orders_routes.router)






# # Templates folder
# templates = Jinja2Templates(directory="templates")
# # Root endpoint to render index.html
# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html",
#         context={"request": request}
#     )
# # Optional About Page
# @app.get("/dashboard", response_class=HTMLResponse)
# def dashboard(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="dashboard.html",
#         context={"request": request}
#     )


# # Create tables automatically
# Base.metadata.create_all(bind=engine)


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Database
from app.database.db import Base, engine

# API Routers
from app.routes import master_users_routes
from app.routes import master_role_routes
from app.routes import master_leads_routes
from app.routes import lead_shedule_demo_routes
from app.routes import master_client_routes
from app.routes import master_machine_and_part_routes
from app.routes import work_orders_routes
from app.routes import template_routes

# ===========================
# FastAPI instance
# ===========================
app = FastAPI(title="Tea Vending ERP API", version="1.0")

# ===========================
# Mount static files
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# ===========================
# Include API Routers
# ===========================
app.include_router(master_users_routes.router)
app.include_router(master_role_routes.router)
app.include_router(master_leads_routes.router)
app.include_router(lead_shedule_demo_routes.router)
app.include_router(master_client_routes.router)
app.include_router(master_machine_and_part_routes.router)
app.include_router(work_orders_routes.router)

# ===========================
# Include Template Router
# ===========================
app.include_router(template_routes.router)

# ===========================
# Create DB tables
# ===========================
Base.metadata.create_all(bind=engine)