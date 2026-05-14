from repo import account_repo

def get_all():
    return account_repo.get_all_accounts()

def get_by_customer_id(customer_id: int):
    return account_repo.get_accounts_by_customer_id(customer_id)

def get_premium():
    return account_repo.get_premium_accounts()