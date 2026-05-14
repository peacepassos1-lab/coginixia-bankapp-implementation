from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import auth_service

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = auth_service.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username