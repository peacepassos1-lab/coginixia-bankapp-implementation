from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from controllers.customer_controller import router as customer_router
from controllers.account_controller import router as account_router
from database import customers_collection
from auth.auth_controller import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())

    if customers_collection.count_documents({}) == 0:
        customers_collection.insert_many([
            {
                "id"      : 1,
                "name"    : "Alice",
                "accounts": [
                    {
                        "id"            : 1,
                        "account_number": "123456",
                        "balance"       : 15000.0,
                        "type"          : "Savings"
                    }
                ]
            },
            {
                "id"      : 2,
                "name"    : "Bob",
                "accounts": [
                    {
                        "id"            : 2,
                        "account_number": "654321",
                        "balance"       : 500.0,
                        "type"          : "Checkings"
                    }
                ]
            }
        ])
    yield

app = FastAPI(title="Bank App REST API", lifespan=lifespan)

app.include_router(customer_router)
app.include_router(account_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bank App API!"}
