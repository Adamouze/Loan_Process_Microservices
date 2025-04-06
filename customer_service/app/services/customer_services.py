from app.orm.orm import Customer as CustomerORM
from app.models.customer import CustomerCreate, CustomerUpdate
from sqlalchemy.orm import Session
from app.error_handling.error_types import AlreadyExistsError, NotFoundError


# Create a customer
def create_customer(customer: CustomerCreate, db: Session):
    # Check if the customer already exists
    existing_customer = db.query(CustomerORM).filter(
        (CustomerORM.full_name == customer.full_name) | 
        (CustomerORM.email == customer.email)
    ).first()

    if existing_customer:
        raise AlreadyExistsError("Customer already exists")
    
    # Create a new customer
    new_customer = CustomerORM(
        full_name=customer.full_name,
        email=customer.email
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return new_customer

# Update an existing customer
def update_customer(customer: CustomerUpdate, db: Session):
    # Check if the customer exists
    existing_customer = db.query(CustomerORM).filter(CustomerORM.id == customer.id).first()
    if not existing_customer:
        raise NotFoundError("Customer not found")
    
    # Update the customer details
    existing_customer.full_name = customer.full_name if customer.full_name else existing_customer.full_name
    existing_customer.email = customer.email if customer.email else existing_customer.email
    
    db.commit()
    db.refresh(existing_customer)
    
    return existing_customer
    
# Get customer details by ID
def get_customer_by_id(customer_id: int, db: Session):
    customer = db.query(CustomerORM).filter(CustomerORM.id == customer_id).first()
    if not customer:
        raise NotFoundError("Customer not found")
    return customer

# Get customer details by full name
def get_customer_by_full_name(full_name: str, db: Session):
    customer = db.query(CustomerORM).filter(CustomerORM.full_name == full_name).first()
    if not customer:
        raise NotFoundError("Customer not found")
    return customer

# Get all customers
def get_all_customers(db: Session):
    customers = db.query(CustomerORM).all()
    if not customers:
        raise NotFoundError("No customers found")
    return customers
    
# Delete a customer
def delete_customer(customer_id: int, db: Session):
    customer = db.query(CustomerORM).filter(CustomerORM.id == customer_id).first()
    if not customer:
        raise NotFoundError("Customer not found")
    
    db.delete(customer)
    db.commit()
    
    return {"message": "Customer deleted successfully"}
