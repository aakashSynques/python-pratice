# entry points

from fastapi import FastAPI
from app.routes import user
from app.database.db import Base, engine

app = FastAPI(title="Customer API", version="1.0")

# Include user routes
app.include_router(user.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Go to /customers/ to see the customer list"}




# Create tables only when running directly
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)