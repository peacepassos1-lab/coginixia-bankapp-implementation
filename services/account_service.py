from repo import account_repo

def get_all(username: str = None, role: str = "user"):
    if role == "admin":
        return account_repo.get_all_accounts()
    return account_repo.get_all_accounts(username=username)

def get_by_customer_id(customer_id: int, username: str = None, role: str = "user"):
    if role == "admin":
        return account_repo.get_accounts_by_customer_id(customer_id)
    return account_repo.get_accounts_by_customer_id(customer_id, username=username)

def get_premium(username: str = None, role: str = "user"):
    if role == "admin":
        return account_repo.get_premium_accounts()
    return account_repo.get_premium_accounts(username=username)