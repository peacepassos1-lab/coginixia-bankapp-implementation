from fastapi import APIRouter, HTTPException, Depends
from services import account_service
from auth.auth_dependency import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/")
def get_all_accounts(current_user: dict = Depends(get_current_user)):
    return account_service.get_all(
        username=current_user["username"],
        role=current_user["role"]
    )

@router.get("/premium")
def get_premium_accounts(current_user: dict = Depends(get_current_user)):
    return account_service.get_premium(
        username=current_user["username"],
        role=current_user["role"]
    )

@router.get("/customer/{customer_id}")
def get_accounts_by_customer(customer_id: int, current_user: dict = Depends(get_current_user)):
    accounts = account_service.get_by_customer_id(
        customer_id,
        username=current_user["username"],
        role=current_user["role"]
    )
    if accounts is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return accounts