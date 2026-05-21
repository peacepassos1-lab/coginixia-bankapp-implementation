from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import auth_service

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_info = auth_service.verify_token(token)

    if user_info is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_info