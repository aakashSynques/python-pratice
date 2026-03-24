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

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes import user
from app.database.db import Base, engine
# FastAPI instance
app = FastAPI(title="Customer API", version="1.0")
# Include user routes
app.include_router(user.router)
# Templates folder
templates = Jinja2Templates(directory="templates")

# Root endpoint to render index.html
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,        
        name="index.html",        
        context={"request": request}  
    )

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        request=request,        
        name="about.html",        
        context={"request": request}  
    )



# Optional: create tables if running main directly
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
