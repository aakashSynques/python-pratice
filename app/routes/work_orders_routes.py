from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import os
import json
from app.database.db import get_db
from app.models.work_order_model import (
    WorkOrder,
    WorkOrderMachine
)
from app.schemas.work_orders_schemas import (
    WorkOrderCreate,
    WorkOrderUpdate,
    WorkOrderResponse
)
router = APIRouter(
    prefix="/work-orders",
    tags=["Work Orders"]
)

UPLOAD_DIR = "uploads/work_orders"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# Generate Work Order Number
def generate_work_order_no(db: Session):
    year = datetime.now().year
    last_order = db.query(WorkOrder)\
        .order_by(WorkOrder.id.desc())\
        .first()
    if last_order:
        next_id = last_order.id + 1
    else:
        next_id = 1
    return f"WO-{year}-{next_id:03d}"
# CREATE WORK ORDER

# @router.post("/create", response_model=WorkOrderResponse)
# def create_work_order(
#     work_order: WorkOrderCreate,
#     db: Session = Depends(get_db)
# ):
#     work_order_no = generate_work_order_no(db)
#     db_work_order = WorkOrder(
#         work_order_no=work_order_no,
#         client_id=work_order.client_id,
#         order_date=work_order.order_date,
#         expected_installation_date=work_order.expected_installation_date,
#         remarks=work_order.remarks,
#         created_by=work_order.created_by
#     )
#     db.add(db_work_order)
#     db.commit()
#     db.refresh(db_work_order)
#     # Add Machines
#     for machine in work_order.machines:
#         db_machine = WorkOrderMachine(
#             work_order_id=db_work_order.id,
#             machine_id=machine.machine_id,
#             quantity=machine.quantity,
#             remarks=machine.remarks
#         )
#         db.add(db_machine)
#     db.commit()
#     db.refresh(db_work_order)
#     return db_work_order



@router.post("/create", response_model=WorkOrderResponse)
def create_work_order(

    work_order: str = Form(...),   # JSON string

    document: UploadFile = File(None),

    db: Session = Depends(get_db)

):

    # Convert JSON → Schema
    work_order_data = WorkOrderCreate(
        **json.loads(work_order)
    )

    work_order_no = generate_work_order_no(db)

    file_path = None

    # Save File
    if document:

        file_name = f"{work_order_no}_{document.filename}"

        file_location = os.path.join(
            UPLOAD_DIR,
            file_name
        )

        with open(file_location, "wb") as buffer:
            buffer.write(document.file.read())

        file_path = file_location

    # Create Work Order

    db_work_order = WorkOrder(

        work_order_no=work_order_no,

        client_id=work_order_data.client_id,

        order_date=work_order_data.order_date,

        expected_installation_date=
            work_order_data.expected_installation_date,

        remarks=work_order_data.remarks,

        created_by=work_order_data.created_by,

        document_path=file_path
    )

    db.add(db_work_order)

    db.commit()

    db.refresh(db_work_order)

    # Add Machines

    for machine in work_order_data.machines:

        db_machine = WorkOrderMachine(

            work_order_id=db_work_order.id,

            machine_id=machine.machine_id,

            quantity=machine.quantity,

            remarks=machine.remarks
        )

        db.add(db_machine)

    db.commit()

    db.refresh(db_work_order)

    return db_work_order




# GET ALL WORK ORDERS
@router.get("/", response_model=list[WorkOrderResponse])
def get_work_orders(
    db: Session = Depends(get_db)
):
    orders = db.query(WorkOrder).all()
    return orders
# GET SINGLE WORK ORDER
@router.get("/{work_order_id}", response_model=WorkOrderResponse)
def get_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(WorkOrder).filter(
        WorkOrder.id == work_order_id
    ).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Work Order not found"
        )
    return order

# UPDATE WORK ORDER
@router.put("/{work_order_id}")
def update_work_order(
    work_order_id: int,
    work_order: WorkOrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(WorkOrder).filter(
        WorkOrder.id == work_order_id
    ).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Work Order not found"
        )
    for key, value in work_order.dict(
        exclude_unset=True
    ).items():
        setattr(order, key, value)
    db.commit()
    return {
        "message": "Work Order updated successfully"
    }


# DELETE WORK ORDER
@router.delete("/{work_order_id}")
def delete_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(WorkOrder).filter(
        WorkOrder.id == work_order_id
    ).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Work Order not found"
        )
    db.delete(order)
    db.commit()
    return {
        "message": "Work Order deleted successfully"
    }