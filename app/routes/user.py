from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.user import MasterCustomer
from app.schemas.user import CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(MasterCustomer).all()
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers