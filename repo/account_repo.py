from database import customers_collection
from models.customer import Account

def get_all_accounts():
    all_customers = customers_collection.find()
    all_accounts = []

    for customer_data in all_customers:
        for account_data in customer_data["accounts"]:
            account = Account(
                id=account_data["id"],
                account_number=account_data["account_number"],
                balance=account_data["balance"],
                type=account_data["type"]
            )
            all_accounts.append(account)
    return all_accounts

def get_accounts_by_customer_id(customer_id):
    customer_data = customers_collection.find_one({"id": customer_id})
    if customer_data is None:
        return None
    
    accounts_list = []
    for account_data in customer_data["accounts"]:
        account = Account(
            id=account_data["id"],
            account_number=account_data["account_number"],
            balance=account_data["balance"],
            type=account_data["type"]
        )
        accounts_list.append(account)
    return accounts_list


def get_premium_accounts():
    all_accounts = get_all_accounts()
    premium_accounts = []

    for account in all_accounts:
        if account.balance > 10000:
            premium_accounts.append(account)
    return premium_accounts