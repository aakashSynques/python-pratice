from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.master_role import MasterRole
from app.schemas.role_schemas import (RoleCreate, RoleResponse)
router = APIRouter(    prefix="/roles",    tags=["Master Roles"])
# Create Role
@router.post("/create", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    existing_role = db.query(MasterRole).filter(
        MasterRole.role_name == role.role_name
    ).first()
    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Role already exists"
        )
    new_role = MasterRole(
        role_name=role.role_name,
        status=role.status
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
# Get All Roles
@router.get("/all")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(MasterRole).all()

    for r in roles:
        print(r.role_id, r.role_name, r.eat)

    return roles
