from database import customers_collection
from models.customer import Customer, Account, AccountType


customers_db: dict[int, Customer] = {
    1: Customer(id = 1, name = "Alice", accounts = [Account(id = 1, account_number = "123456", balance = 1000.0, type = AccountType.savings)]),
    2: Customer(id = 2, name = "Bob", accounts = [Account(id = 2, account_number = "654321", balance = 500.0, type = AccountType.checking)]),
}

def get_all_customers():
    print("--- HIT DATABASE: fetching from MongoDB ---")
    all_customers_from_db = customers_collection.find()

    result = []

    for customer_data in all_customers_from_db:

        accounts_list = []
        for account_data in customer_data["accounts"]:
            account = Account(
                id = account_data["id"],
                account_number = account_data["account_number"],
                balance = account_data["balance"],
                type = account_data["type"]
            )
            accounts_list.append(account)
        
        customer = Customer(
            id = customer_data["id"],
            name = customer_data["name"],
            accounts = accounts_list
        )
        result.append(customer)
    return result
        

def get_customer_by_id(customer_id: int):
    customer_data = customers_collection.find_one({"id": customer_id})
    if customer_data is None:
        return None
    
    accounts_list = []
    for account_data in customer_data["accounts"]:
        account = Account(
            id = account_data["id"],
            account_number = account_data["account_number"],
            balance = account_data["balance"],
            type = account_data["type"]
        )
        accounts_list.append(account)

    customer = Customer(
        id = customer_data["id"],
        name = customer_data["name"],
        accounts = accounts_list
    )
    return customer



def save_customer(customer: Customer):
    accounts_to_save = []

    for account in customer.accounts:
        accounts_dict = {
            "id": account.id,
            "account_number": account.account_number,
            "balance": account.balance,
            "type": account.type
        }
        accounts_to_save.append(accounts_dict)
    customer_to_save = {
        "id": customer.id,
        "name": customer.name,
        "accounts": accounts_to_save
    }
    customers_collection.update_one({"id": customer.id}, {"$set": customer_to_save}, upsert=True)
    return customer



def delete_customer(customer_id: int):
    result = customers_collection.delete_one({"id": customer_id})
    if result.deleted_count == 1:
        return True
    return False



