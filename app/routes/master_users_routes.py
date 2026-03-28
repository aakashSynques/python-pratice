from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.master_users import MasterUser
from app.models.master_role import MasterRole
from app.schemas.users_schemas import UserCreate, UserResponse, UserLogin, UserUpdate
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Master Users"])

@router.post("/create", response_model=UserResponse)

def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: MasterUser = Depends(get_current_user)):
    existing_user = db.query(MasterUser).filter(MasterUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    role = db.query(MasterRole).filter(MasterRole.role_id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = MasterUser(
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        address=user.address,
        password=hashed_password,
        role_id=user.role_id,
         status=user.status  

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
# Get All Users


@router.get("/all", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: MasterUser = Depends(get_current_user)):
    users = db.query(MasterUser).all()
    return users



# Update User
@router.put("/update/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    existing_user = db.query(MasterUser).filter(
        MasterUser.id == user_id
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    role = db.query(MasterRole).filter(
        MasterRole.role_id == user.role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.mobile = user.mobile
    existing_user.address = user.address
    existing_user.role_id = user.role_id
    existing_user.status = user.status

    db.commit()
    db.refresh(existing_user)

    return existing_user



# Delete User
@router.delete("/delete/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    user = db.query(MasterUser).filter(
        MasterUser.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}




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
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    if user.status != 1:
        raise HTTPException(
            status_code=403,
            detail="User is inactive"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }