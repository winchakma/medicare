from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.user import User
from app.utils.deps import get_current_user

router = APIRouter()

class DoctorProfileUpdate(BaseModel):
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    fee_per_visit: Optional[float] = None

@router.get("/list")
async def get_doctors():
    doctors = await User.find(User.role == "doctor", User.is_verified == True).to_list()
    return doctors

@router.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me")
async def update_my_profile(profile: DoctorProfileUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    current_user.first_name = profile.first_name
    current_user.last_name = profile.last_name
    current_user.specialty = profile.specialty
    current_user.experience_years = profile.experience_years
    current_user.location = profile.location
    current_user.fee_per_visit = profile.fee_per_visit
    
    await current_user.save()
    return current_user
