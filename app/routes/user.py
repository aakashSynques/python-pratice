# Route API endpoint banata hai. (Routes kya karta hai (API Logic))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.user import MasterCustomer
from app.schemas.user import CustomerResponse, CustomerCreate

router = APIRouter(prefix="/customers", tags=["Customers"])

# GET All Customers
@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(MasterCustomer).all()
    if not customers:
        raise HTTPException(
            status_code=404,
            detail="No customers found"
        )
    return customers


#  Customer Register API
@router.post("/register", response_model=CustomerResponse)
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    # Check email exists
    existing_customer = db.query(MasterCustomer).filter(
        MasterCustomer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    # Create new customer
    new_customer = MasterCustomer(
        name=customer.name,
        shop_name=customer.shop_name,
        email=customer.email,
        mobile=customer.mobile,
        address=customer.address,
        password=customer.password,
        status=1
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer