from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_models import UserRegister, UserLogin, Token
from auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBearer()

@router.post("/register")
def register(user: UserRegister):
    result = auth_service.register_user(user.username, user.password)

    if result is None:
        raise HTTPException(status_code=400, detail="Username already exists")
    return result   

@router.post("/login")
def login(user: UserLogin):
    result = auth_service.login_user(user.username, user.password)

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return result

@router.get("/protected-test")
def protected_test(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = auth_service.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": f"Hello, {username}! You are authenticated."}
