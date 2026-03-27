from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database.db import get_db

from app.models.work_order_model import WorkOrders
from app.models.master_client_model import MasterClient
from app.models.master_machine_and_part import MasterMachines

from app.schemas.work_orders_schemas import (
    WorkOrderCreate,
    WorkOrderUpdate,
    WorkOrderResponse
)

router = APIRouter(
    prefix="/work-orders",
    tags=["Work Orders"]
)


# Generate Work Order Number
def generate_work_order_no(db: Session):

    last_order = db.query(WorkOrders).order_by(
        WorkOrders.id.desc()
    ).first()

    if not last_order:
        return "WO-001"

    new_number = last_order.id + 1

    return f"WO-{new_number:03d}"


# CREATE Work Order
@router.post("/", response_model=WorkOrderResponse)
def create_work_order(
    work_order: WorkOrderCreate,
    db: Session = Depends(get_db)
):

    # Check Client
    client = db.query(MasterClient).filter(
        MasterClient.id == work_order.client_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    # Check Machine
    machine = db.query(MasterMachines).filter(
        MasterMachines.id == work_order.machine_id
    ).first()

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    # Generate Number
    work_order_no = generate_work_order_no(db)

    new_work_order = WorkOrders(
        work_order_no=work_order_no,
        client_id=work_order.client_id,
        machine_id=work_order.machine_id,
        quantity=work_order.quantity,
        order_date=work_order.order_date,
        status=work_order.status
    )

    db.add(new_work_order)
    db.commit()
    db.refresh(new_work_order)

    return new_work_order


# GET All
@router.get("/", response_model=List[WorkOrderResponse])
def get_all_work_orders(db: Session = Depends(get_db)):

    work_orders = db.query(
        WorkOrders
    ).options(
        joinedload(WorkOrders.client),
        joinedload(WorkOrders.machine)
    ).all()

    return work_orders


# GET By ID
@router.get("/{work_order_id}", response_model=WorkOrderResponse)
def get_work_order_by_id(
    work_order_id: int,
    db: Session = Depends(get_db)
):

    work_order = db.query(WorkOrders).filter(
        WorkOrders.id == work_order_id
    ).first()

    if not work_order:
        raise HTTPException(
            status_code=404,
            detail="Work Order not found"
        )

    return work_order


# UPDATE
# @router.put("/{work_order_id}", response_model=WorkOrderResponse)
# def update_work_order(
#     work_order_id: int,
#     work_order: WorkOrderUpdate,
#     db: Session = Depends(get_db)
# ):

#     existing = db.query(WorkOrders).filter(
#         WorkOrders.id == work_order_id
#     ).first()

#     if not existing:
#         raise HTTPException(
#             status_code=404,
#             detail="Work Order not found"
#         )

#     # Validate Client
#     if work_order.client_id:
#         client = db.query(MasterClient).filter(
#             MasterClient.id == work_order.client_id
#         ).first()

#         if not client:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Client not found"
#             )

#     # Validate Machine
#     if work_order.machine_id:
#         machine = db.query(MasterMachines).filter(
#             MasterMachines.id == work_order.machine_id
#         ).first()

#         if not machine:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Machine not found"
#             )

#     # Update fields
#     for key, value in work_order.dict(
#         exclude_unset=True
#     ).items():
#         setattr(existing, key, value)

#     db.commit()
#     db.refresh(existing)

#     return existing

@router.put("/{work_order_id}", response_model=WorkOrderResponse)
def update_work_order(
    work_order_id: int,
    work_order: WorkOrderUpdate,
    db: Session = Depends(get_db)
):

    existing = db.query(WorkOrders).filter(
        WorkOrders.id == work_order_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Work Order not found"
        )

    # Validate Client
    if work_order.client_id:
        client = db.query(MasterClient).filter(
            MasterClient.id == work_order.client_id
        ).first()

        if not client:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )

    # Validate Machine
    if work_order.machine_id:
        machine = db.query(MasterMachines).filter(
            MasterMachines.id == work_order.machine_id
        ).first()

        if not machine:
            raise HTTPException(
                status_code=404,
                detail="Machine not found"
            )

    # Update fields
    for key, value in work_order.dict(
        exclude_unset=True
    ).items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing

# DELETE
@router.delete("/{work_order_id}")
def delete_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):

    work_order = db.query(WorkOrders).filter(
        WorkOrders.id == work_order_id
    ).first()

    if not work_order:
        raise HTTPException(
            status_code=404,
            detail="Work Order not found"
        )

    db.delete(work_order)
    db.commit()

    return {
        "message": "Work Order deleted successfully"
    }