from models.customer import Customer
from repo import customer_repo

_cache = {}

def get_all(username: str = None, role: str = "user"):
    if role == "admin":
        cache_key = "all_customers_admin"
        result_username = None
    else:
        cache_key = f"all_customers_{username}"
        result_username = username

    if cache_key in _cache:
        print(f"--- CACHE HIT ---")
        return _cache[cache_key]

    result = customer_repo.get_all_customers(username=result_username)
    _cache[cache_key] = result
    return result

def clear_cache():
    _cache.clear()

def get_by_id(customer_id: int, username: str = None, role: str = "user"):
    if role == "admin":
        return customer_repo.get_customer_by_id(customer_id)
    return customer_repo.get_customer_by_id(customer_id, username=username)

def create(customer: Customer, username: str = None):
    customer.created_by = username
    result = customer_repo.save_customer(customer)
    clear_cache()
    return result

def update(customer_id: int, customer: Customer, username: str = None, role: str = "user"):
    if role == "admin":
        existing_customer = customer_repo.get_customer_by_id(customer_id)
    else:
        existing_customer = customer_repo.get_customer_by_id(customer_id, username=username)

    if not existing_customer:
        return None

    customer.id = customer_id
    customer.created_by = existing_customer.created_by
    result = customer_repo.save_customer(customer)
    clear_cache()
    return result

def delete(customer_id: int, username: str = None, role: str = "user"):
    if role == "admin":
        result = customer_repo.delete_customer(customer_id)
    else:
        result = customer_repo.delete_customer(customer_id, username=username)
    clear_cache()
    return result