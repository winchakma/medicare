from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.user import User
from app.models.booking import Booking
from app.utils.deps import get_current_user
from datetime import datetime

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

@router.get("/dashboard-stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    bookings = await Booking.find(Booking.doctor_id == str(current_user.id)).to_list()
    
    total_earnings = sum(b.fee_amount for b in bookings if b.status == "completed" or b.payment_status == "paid")
    
    # Simple logic for now
    upcoming_appointments = [b for b in bookings if b.status in ["pending", "confirmed"]]
    
    unique_patients = set(b.patient_id for b in bookings)
    total_patients = len(unique_patients)
    
    # Get recent patients details
    recent_patients = []
    # Just take up to 5 unique recent patients
    for pid in list(unique_patients)[:5]:
        p = await User.get(pid)
        if p:
            recent_patients.append({"id": str(p.id), "name": f"{p.first_name} {p.last_name}", "avatar": f"{p.first_name[0]}{p.last_name[0]}" if p.last_name else p.first_name[0:2]})
            
    upcoming_list = []
    for b in upcoming_appointments[:5]:
        p = await User.get(b.patient_id)
        p_name = f"{p.first_name} {p.last_name}" if p else "Unknown Patient"
        upcoming_list.append({
            "id": str(b.id),
            "patient_name": p_name,
            "date": b.date,
            "time_slot": b.time_slot,
            "consultation_type": b.consultation_type
        })
        
    return {
        "total_earnings": total_earnings,
        "upcoming_count": len(upcoming_appointments),
        "total_patients": total_patients,
        "upcoming_appointments": upcoming_list,
        "recent_patients": recent_patients
    }
