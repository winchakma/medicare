import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def promote_to_admin():
    uri = "mongodb+srv://winchakma:win123win@cluster0.htlsc44.mongodb.net/medicare_db?retryWrites=true&w=majority&appName=Cluster0"
    client = AsyncIOMotorClient(uri)
    db = client.medicare_db
    result = await db.users.update_one(
        {"email": "winchakma123@gmail.com"},
        {"$set": {"role": "admin"}}
    )
    if result.matched_count == 0:
        print("User not found!")
    else:
        print(f"Successfully promoted winchakma123@gmail.com to admin! Modified: {result.modified_count}")

if __name__ == "__main__":
    asyncio.run(promote_to_admin())
