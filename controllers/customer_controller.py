from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache
from models.customer import Customer
from services import customer_service
from auth.auth_dependency import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/")
def get_all_customers(current_user: str = Depends(get_current_user)):
    return customer_service.get_all()

@router.get("/{customer_id}")
def get_customer(customer_id: int, current_user: str = Depends(get_current_user)):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/")
def create_customer(customer: Customer, current_user: str = Depends(get_current_user)):
    return customer_service.create(customer)

@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: Customer, current_user: str = Depends(get_current_user)):
    updated_customer = customer_service.update(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, current_user: str = Depends(get_current_user)):
    success = customer_service.delete(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": "Customer deleted successfully"}