from models.customer import Customer
from repo import customer_repo

_cache = {}

def get_all():
    if "all_customers" in _cache:
        print("--- CACHE HIT: fetching all customers from cache ---")
        return _cache["all_customers"]
    
    result = customer_repo.get_all_customers()

    _cache["all_customers"] = result
    print("--- HIT DATABASE: fetching all customers from MongoDB ---")
    return result

def clear_cache():
    _cache.clear()

def get_by_id(customer_id: int):
    return customer_repo.get_customer_by_id(customer_id)

def create(customer: Customer):
    result = customer_repo.save_customer(customer)
    clear_cache()
    return result

def update(customer_id: int, customer: Customer):
    existing_customer = customer_repo.get_customer_by_id(customer_id)
    if not existing_customer:
        return None
    customer.id = customer_id
    result = customer_repo.save_customer(customer)
    clear_cache()
    return result

def delete(customer_id: int):
    result = customer_repo.delete_customer(customer_id)
    clear_cache()
    return result   
   