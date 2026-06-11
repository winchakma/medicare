from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.get("/list")
async def get_doctors():
    doctors = await User.find(User.role == "doctor", User.is_verified == True).to_list()
    return doctors
