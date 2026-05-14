from models.customer import Account, Customer
from repo import customer_repo

def get_all_accounts():
    all_customers = customer_repo.get_all_customers()
    accounts = []
    for customer in all_customers:
        accounts.extend(customer.accounts)
    return accounts

def get_accounts_by_customer_id(customer_id):
    customer = customer_repo.get_customer_by_id(customer_id)
    if not customer:
        return None
    return customer.accounts

def get_premium_accounts():
    all_accounts = get_all_accounts()
    return [acc for acc in all_accounts if acc.balance > 10000]