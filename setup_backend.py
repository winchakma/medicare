import os
import shutil
import secrets

TRAVEL_DIR = "c:/Users/user/Desktop/mytravelproject/backend"
DOCTOR_DIR = "c:/Users/user/Desktop/doctor/backend"

# 1. Create directories
dirs = [
    "",
    "app",
    "app/models",
    "app/routes",
    "app/utils",
    "app/schemas",
]

for d in dirs:
    os.makedirs(os.path.join(DOCTOR_DIR, d), exist_ok=True)
    if d != "":
        with open(os.path.join(DOCTOR_DIR, d, "__init__.py"), "w") as f:
            pass

# 2. Copy and adapt requirements.txt
req_content = """fastapi==0.104.1
uvicorn==0.24.0
websockets==12.0
pydantic==2.5.2
pydantic-settings==2.1.0
python-dotenv==1.0.0
motor>=3.5.1
beanie>=2.1.0
PyJWT==2.8.0
passlib[bcrypt]==1.7.4
bcrypt==3.2.0
cloudinary==1.36.0
requests==2.31.0
python-multipart==0.0.6
gunicorn==21.2.0
google-generativeai==0.8.3
"""
with open(os.path.join(DOCTOR_DIR, "requirements.txt"), "w") as f:
    f.write(req_content)

# 3. Create .env
jwt_secret = secrets.token_hex(32)
env_content = f"""MONGODB_URL=mongodb+srv://admin:admin123@cluster0.abcde.mongodb.net/medicare_db?retryWrites=true&w=majority
JWT_SECRET_KEY={jwt_secret}
JWT_ALGORITHM=HS256
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
GEMINI_API_KEY=your_gemini_key
"""
with open(os.path.join(DOCTOR_DIR, ".env"), "w") as f:
    f.write(env_content)

# 4. Create database.py
database_content = """from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url or "cluster0.abcde.mongodb.net" in mongodb_url:
        print("[WARNING] MONGODB_URL is missing or using placeholder! Please update .env", flush=True)
        # We will not return here so it fails loudly if it's a dummy
        
    print(f"Connecting to MongoDB...", flush=True)
    
    try:
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=10000)
        await client.admin.command('ping')
        print("MongoDB Ping Successful.", flush=True)
        
        db_name = mongodb_url.split("/")[-1].split("?")[0] or "medicare_db"
        
        client.append_metadata = lambda x: None
            
        # We will add models here as we create them
        from app.models.user import User
        from app.models.booking import Booking
        from app.models.admin import AdminConfig
        
        await init_beanie(
            database=client[db_name],
            document_models=[
                User, Booking, AdminConfig
            ]
        )

        print(f"Beanie initialized with database: {db_name}", flush=True)
    except Exception as e:
        print(f"[DATABASE ERROR] Connection failed: {str(e)}", flush=True)
        raise e
"""
with open(os.path.join(DOCTOR_DIR, "app", "database.py"), "w") as f:
    f.write(database_content)

print("Backend structure, .env, and database.py set up.")
