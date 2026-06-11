from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = MongoClient(mongo_url)
    db = client["medicare_db"]
    collection = db["User"]
    
    doctors = [
        {
            "email": "john.cardiologist@example.com",
            "password_hash": "dummyhash",
            "first_name": "John",
            "last_name": "Smith",
            "role": "doctor",
            "is_verified": True,
            "specialty": "Cardiologist",
            "experience_years": 12,
            "location": "Dhaka Medical",
            "fee_per_visit": 1500,
            "profile_photo": ""
        },
        {
            "email": "sarah.neuro@example.com",
            "password_hash": "dummyhash",
            "first_name": "Sarah",
            "last_name": "Connor",
            "role": "doctor",
            "is_verified": True,
            "specialty": "Neurologist",
            "experience_years": 8,
            "location": "Apollo Hospital",
            "fee_per_visit": 2000,
            "profile_photo": ""
        },
        {
            "email": "emily.pedia@example.com",
            "password_hash": "dummyhash",
            "first_name": "Emily",
            "last_name": "Chen",
            "role": "doctor",
            "is_verified": True,
            "specialty": "Pediatrician",
            "experience_years": 5,
            "location": "Square Hospital",
            "fee_per_visit": 1200,
            "profile_photo": ""
        },
        {
            "email": "david.derma@example.com",
            "password_hash": "dummyhash",
            "first_name": "David",
            "last_name": "Lee",
            "role": "doctor",
            "is_verified": True,
            "specialty": "Dermatologist",
            "experience_years": 15,
            "location": "Popular Diag",
            "fee_per_visit": 1800,
            "profile_photo": ""
        },
        {
            "email": "michael.dentist@example.com",
            "password_hash": "dummyhash",
            "first_name": "Michael",
            "last_name": "Brown",
            "role": "doctor",
            "is_verified": True,
            "specialty": "Dentist",
            "experience_years": 10,
            "location": "Labaid",
            "fee_per_visit": 1000,
            "profile_photo": ""
        }
    ]
    
    for doc in doctors:
        if not collection.find_one({"email": doc["email"]}):
            collection.insert_one(doc)
            print(f"Inserted doctor {doc['first_name']} {doc['last_name']}")
            
    print("Database seeding completed.")

if __name__ == "__main__":
    main()
