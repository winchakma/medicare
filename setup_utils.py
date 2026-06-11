import os

BACKEND_DIR = "c:/Users/user/Desktop/doctor/backend"
UTILS_DIR = os.path.join(BACKEND_DIR, "app/utils")
ROUTES_DIR = os.path.join(BACKEND_DIR, "app/routes")
SCHEMAS_DIR = os.path.join(BACKEND_DIR, "app/schemas")

# 1. UTILS: auth.py
auth_util_content = """from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
    return encoded_jwt
"""
with open(os.path.join(UTILS_DIR, "auth.py"), "w") as f: f.write(auth_util_content)

# 2. ROUTES: auth.py
auth_route_content = """from fastapi import APIRouter, HTTPException, Depends
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
"""
with open(os.path.join(ROUTES_DIR, "auth.py"), "w") as f: f.write(auth_route_content)

# 3. ROUTES: doctors.py
doctors_route_content = """from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.get("/list")
async def get_doctors():
    doctors = await User.find(User.role == "doctor", User.is_verified == True).to_list()
    return doctors
"""
with open(os.path.join(ROUTES_DIR, "doctors.py"), "w") as f: f.write(doctors_route_content)

# 4. MAIN.PY
main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth, doctors

app = FastAPI(title="MediCare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_database():
    await init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])

@app.get("/")
def read_root():
    return {"message": "MediCare API is running"}
"""
with open(os.path.join(BACKEND_DIR, "main.py"), "w") as f: f.write(main_content)

print("Utils, Routes, and main.py created.")
