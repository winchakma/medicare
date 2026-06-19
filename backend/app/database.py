from motor.motor_asyncio import AsyncIOMotorClient
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
        from app.models.blog import Blog
        
        await init_beanie(
            database=client[db_name],
            document_models=[
                User, Booking, AdminConfig, Blog
            ]
        )

        print(f"Beanie initialized with database: {db_name}", flush=True)
    except Exception as e:
        print(f"[DATABASE ERROR] Connection failed: {str(e)}", flush=True)
        raise e
