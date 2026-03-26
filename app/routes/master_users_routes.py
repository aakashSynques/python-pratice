from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.master_users import MasterUser
from app.models.master_role import MasterRole
from app.schemas.users_schemas import UserCreate, UserResponse, UserLogin

router = APIRouter(prefix="/users", tags=["Master Users"])

@router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(MasterUser).filter(MasterUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    role = db.query(MasterRole).filter(MasterRole.role_id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")
    # Create new user
    new_user = MasterUser(
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        address=user.address,
        password=user.password,
        role_id=user.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Get All Users
@router.get("/all", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(MasterUser).all()
    return users

# user Login API
@router.post("/login")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(MasterUser).filter(
        MasterUser.email == login_data.email
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.password != login_data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    if user.status != 1:
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )
    return {
        "message": "Login successful",
        "id": user.id,
        "name": user.name,
        "email": user.email
    }