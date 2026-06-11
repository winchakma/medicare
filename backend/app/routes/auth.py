from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models.user import User
from app.utils.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

class RegisterSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: str = "patient"

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user_data: RegisterSchema):
    existing = await User.find_one(User.email == user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role
    )
    await user.insert()
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user_data: LoginSchema):
    user = await User.find_one(User.email == user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(days=7)
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}
