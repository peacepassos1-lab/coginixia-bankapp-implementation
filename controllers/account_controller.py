from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache
from services import account_service
from auth.auth_dependency import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/")
@cache(expire=60)
def get_all_accounts(current_user: str = Depends(get_current_user)):
    return account_service.get_all()

@router.get("/premium")
@cache(expire=60)
def get_premium_accounts(current_user: str = Depends(get_current_user)):
    return account_service.get_premium()

@router.get("/customer/{customer_id}")
@cache(expire=60)
def get_accounts_by_customer(customer_id: int, current_user: str = Depends(get_current_user)):
    accounts = account_service.get_by_customer_id(customer_id)
    if accounts is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return accounts