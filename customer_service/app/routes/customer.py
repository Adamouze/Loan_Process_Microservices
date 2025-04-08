from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..services.customer_services import create_customer as create_customer_service, update_customer as update_customer_service, get_customer_by_id as get_customer_details_by_id, get_customer_by_full_name as get_customers_details_by_full_name, get_all_customers, delete_customer as delete_customer_service
from ..models.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from typing import List

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer_service(customer, db)
    
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer: CustomerUpdate, db: Session = Depends(get_db)):
    return update_customer_service(customer, db)
    
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_details_by_id(customer_id, db)

@router.get("/by-name/{full_name}", response_model=CustomerResponse)
def get_customer_by_full_name(full_name: str, db: Session = Depends(get_db)):
    return get_customers_details_by_full_name(full_name, db)

@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return get_all_customers(db)

@router.delete("/{customer_id}", response_model=dict)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return delete_customer_service(customer_id, db)



    