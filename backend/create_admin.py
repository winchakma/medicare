from pymongo import MongoClient
import os
from app.utils.auth import get_password_hash

def main():
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    db = client[os.getenv("MONGODB_DB", "medicare_db")]
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
