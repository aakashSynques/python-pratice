from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db import get_db
from app.models.master_role import MasterRole
from app.models.master_users import MasterUser
from app.schemas.role_schemas import (RoleCreate, RoleResponse)
from app.auth import get_current_user
router = APIRouter(    prefix="/roles",    tags=["Master Roles"])
# Create Role
@router.post("/create", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
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
def get_roles(db: Session = Depends(get_db), current_user: MasterUser = Depends(get_current_user)):
    roles = db.query(MasterRole).all()

    for r in roles:
        print(r.role_id, r.role_name, r.eat)

    return roles



# Update Role
@router.put("/update/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):
    
    existing_role = db.query(MasterRole).filter(
        MasterRole.role_id == role_id
    ).first()

    if not existing_role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    # Check duplicate name
    duplicate_role = db.query(MasterRole).filter(
        MasterRole.role_name == role.role_name,
        MasterRole.role_id != role_id
    ).first()

    if duplicate_role:
        raise HTTPException(
            status_code=400,
            detail="Role name already exists"
        )

    # Update fields
    existing_role.role_name = role.role_name
    existing_role.status = role.status

    db.commit()
    db.refresh(existing_role)

    return existing_role


# Delete Role
@router.delete("/delete/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: MasterUser = Depends(get_current_user)
):

    role = db.query(MasterRole).filter(
        MasterRole.role_id == role_id
    ).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    db.delete(role)
    db.commit()

    return {
        "message": "Role deleted successfully"
    }

