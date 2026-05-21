from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from controllers.customer_controller import router as customer_router
from controllers.account_controller import router as account_router
from auth.auth_controller import router as auth_router
from database import customers_collection

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())

    if customers_collection.count_documents({}) == 0:
        customers_collection.insert_many([
            {
                "id"      : 1,
                "name"    : "Alice",
                "created_by": "admin",
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
                "created_by": "admin",
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

    # Create admin account if none exists
    if users_collection.count_documents({"role": "admin"}) == 0:
        from auth.auth_service import hash_password
        users_collection.insert_one({
            "username": "admin",
            "password": hash_password("admin123"),
            "role": "admin"
        })

    yield

app = FastAPI(title="Bank App REST API", lifespan=lifespan)

# Allow frontend to call the API from a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(account_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Bank App REST API! - Deployed via CI/CD"}