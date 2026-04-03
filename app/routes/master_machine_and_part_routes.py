from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.models.master_machine_and_part import MasterMachines, MasterMachineParts
from app.schemas.machine_and_part_schemas import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
    MachinePartCreate,
    MachinePartUpdate,
    MachinePartResponse,
    MachineResponseWithMessage
)
from app.auth import get_current_user  # Optional, if using auth

router = APIRouter(
    prefix="/machines",
    tags=["Machines"]
)


# Machine Routes

# @router.post("/add-machines", response_model=MachineResponse)
# def create_machine(machine: MachineCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     new_machine = MasterMachines(**machine.dict())
#     db.add(new_machine)
#     db.commit()
#     db.refresh(new_machine)
#     return new_machine



@router.get("/", response_model=List[MachineResponse])
def get_all_machines(db: Session = Depends(get_db)):
    machines = db.query(MasterMachines).all()
    if not machines:
        raise HTTPException(status_code=404, detail="No machines found")
    return machines


# @router.post("/add-machines")
# def create_machine(machine: MachineCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     new_machine = MasterMachines(**machine.dict())
#     db.add(new_machine)
#     db.commit()
#     db.refresh(new_machine)
#     return {
#         "status": "success",
#         "message": "Machine added successfully",
#         "data": new_machine
#     }
@router.post("/add-machines")
def create_machine(
    machine: MachineCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    try:

        # Check duplicate first
        existing_machine = db.query(MasterMachines).filter(
            MasterMachines.machine_code == machine.machine_code
        ).first()

        if existing_machine:
            return {
                "success": False,
                "message": "Machine code already exists"
            }

        new_machine = MasterMachines(**machine.dict())

        db.add(new_machine)
        db.commit()
        db.refresh(new_machine)

        return {
            "success": True,
            "message": "Machine added successfully",
            "data": new_machine
        }

    except Exception as e:

        db.rollback()

        return {
            "success": False,
            "message": str(e)
        }


@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    machine = db.query(MasterMachines).filter(MasterMachines.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

# @router.put("/{machine_id}", response_model=MachineResponse)
# def update_machine(machine_id: int, machine: MachineUpdate, db: Session = Depends(get_db)):
#     db_machine = db.query(MasterMachines).filter(MasterMachines.id == machine_id).first()
#     if not db_machine:
#         raise HTTPException(status_code=404, detail="Machine not found")
#     for key, value in machine.dict(exclude_unset=True).items():
#         setattr(db_machine, key, value)
#     db.commit()
#     db.refresh(db_machine)
#     return db_machine

@router.put("/{machine_id}", response_model=MachineResponseWithMessage)
def update_machine(
    machine_id: int,
    machine: MachineUpdate,
    db: Session = Depends(get_db)
):
    db_machine = db.query(MasterMachines).filter(
        MasterMachines.id == machine_id
    ).first()
    if not db_machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )
    try:
        if machine.machine_code:
            existing_machine = db.query(MasterMachines).filter(
                MasterMachines.machine_code == machine.machine_code,
                MasterMachines.id != machine_id   
            ).first()
            if existing_machine:
                return {
                    "status": "error",
                    "message": "Machine code already exists",
                    "data": None
                }
        for key, value in machine.dict(
            exclude_unset=True
        ).items():
            setattr(db_machine, key, value)
        db.commit()
        db.refresh(db_machine)
        return {
            "status": "success",
            "message": "Machine updated successfully",
            "data": db_machine
        }
    except IntegrityError:
        db.rollback()
        return {
            "status": "error",
            "message": "Machine code already exists",
            "data": None
        }
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e),
            "data": None
        }



# @router.put("/{machine_id}", response_model=MachineResponseWithMessage)
# def update_machine(machine_id: int, machine: MachineUpdate, db: Session = Depends(get_db)):
#     db_machine = db.query(MasterMachines).filter(MasterMachines.id == machine_id).first()
#     if not db_machine:
#         raise HTTPException(status_code=404, detail="Machine not found")    
#     for key, value in machine.dict(exclude_unset=True).items():
#         setattr(db_machine, key, value)
    
#     db.commit()
#     db.refresh(db_machine)
    
#     return {
#         "status": "success",
#         "message": "Machine updated successfully",
#         "data": db_machine
#     }




@router.delete("/{machine_id}")
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    db_machine = db.query(MasterMachines).filter(MasterMachines.id == machine_id).first()
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    db_machine.is_active = 0  # Soft delete
    db.commit()
    return {"detail": "Machine deleted successfully"}


# --------------------------
# Machine Part Routes
# --------------------------


# @router.get("/parts/", response_model=List[MachinePartResponse])
# def get_all_parts(db: Session = Depends(get_db)):
#     parts = db.query(MasterMachineParts).all()
#     return parts

@router.get("/parts/", response_model=List[MachinePartResponse])
def get_all_parts(db: Session = Depends(get_db)):
    parts = db.query(MasterMachineParts).all()
    if not parts:
        raise HTTPException(status_code=404, detail="No machines parts found")
    return parts



@router.post("/parts/add", response_model=MachinePartResponse)
def create_machine_part(
    part: MachinePartCreate,
    db: Session = Depends(get_db)
):
    #  Check machine exists
    machine = db.query(MasterMachines).filter(
        MasterMachines.id == part.machine_id
    ).first()
    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Associated machine not found"
        )
    #  Check duplicate part_code
    existing_part = db.query(MasterMachineParts).filter(
        MasterMachineParts.part_code == part.part_code
    ).first()
    if existing_part:
        raise HTTPException(
            status_code=400,
            detail="Part code already exists, please use unique part_code"
        )
    #  Create new part
    new_part = MasterMachineParts(**part.dict())
    db.add(new_part)
    db.commit()
    db.refresh(new_part)
    return new_part


@router.get("/parts/{part_id}", response_model=MachinePartResponse)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(MasterMachineParts).filter(MasterMachineParts.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

@router.put("/parts/{part_id}", response_model=MachinePartResponse)
def update_part(part_id: int, part: MachinePartUpdate, db: Session = Depends(get_db)):
    db_part = db.query(MasterMachineParts).filter(MasterMachineParts.id == part_id).first()
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")
    for key, value in part.dict(exclude_unset=True).items():
        setattr(db_part, key, value)
    db.commit()
    db.refresh(db_part)
    return db_part

@router.delete("/parts/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    db_part = db.query(MasterMachineParts).filter(MasterMachineParts.id == part_id).first()
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")
    db_part.is_active = 0  # Soft delete
    db.commit()
    return {"detail": "Part deleted successfully"}