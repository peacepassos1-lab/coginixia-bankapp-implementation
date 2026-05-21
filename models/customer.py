from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class AccountType(str, Enum):
    savings = "Savings"
    checking = "Checkings"

class Account(BaseModel):
    id: int
    account_number: str
    balance: float
    type: AccountType

class Customer(BaseModel):
    id: int
    name: str
    accounts: Optional[List[Account]] = []
    created_by: Optional[str] = None