from pymongo import MongoClient
import os
from dotenv import load_dotenv
from app.utils.auth import get_password_hash

load_dotenv()

def main():
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = MongoClient(mongo_url)
    db = client["medicare_db"]
    collection = db["User"]
    
    email = "winchakma123@gmail.com"
    existing = collection.find_one({"email": email})
    
    if existing:
        collection.update_one({"email": email}, {"$set": {"role": "admin"}})
        print(f"Updated {email} to admin role.")
    else:
        user = {
            "email": email,
            "password_hash": get_password_hash("admin123"),
            "first_name": "Win",
            "last_name": "Chakma",
            "role": "admin",
            "is_verified": True
        }
        collection.insert_one(user)
        print(f"Created {email} as admin with password 'admin123'.")

if __name__ == "__main__":
    main()
