from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import users_collection
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str):
    return password_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)

def create_access_token(username: str):
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": username, "exp": expire_time}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def register_user(username: str, password: str):
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        return None
    hashed_password = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "role": "user"
    })
    return {"message": "User registered successfully"}

def login_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if user is None:
        return None
    
    password_matches = verify_password(password, user["password"])
    if not password_matches:
        return None
    token = create_access_token(username)
    return {"access_token": token, "token_type": "bearer"}

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
