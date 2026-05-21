from fastapi import APIRouter, HTTPException, Depends
from models.customer import Customer
from services import customer_service
from auth.auth_dependency import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/")
def get_all_customers(current_user: dict = Depends(get_current_user)):
    return customer_service.get_all(
        username=current_user["username"],
        role=current_user["role"]
    )

@router.get("/{customer_id}")
def get_customer(customer_id: int, current_user: dict = Depends(get_current_user)):
    customer = customer_service.get_by_id(
        customer_id,
        username=current_user["username"],
        role=current_user["role"]
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/")
def create_customer(customer: Customer, current_user: dict = Depends(get_current_user)):
    return customer_service.create(customer, username=current_user["username"])

@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: Customer, current_user: dict = Depends(get_current_user)):
    updated_customer = customer_service.update(
        customer_id,
        customer,
        username=current_user["username"],
        role=current_user["role"]
    )
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, current_user: dict = Depends(get_current_user)):
    success = customer_service.delete(
        customer_id,
        username=current_user["username"],
        role=current_user["role"]
    )
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": "Customer deleted successfully"}