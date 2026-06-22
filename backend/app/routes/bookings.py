from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from app.models.booking import Booking
from app.models.user import User
from app.utils.deps import get_current_user
from beanie import PydanticObjectId

router = APIRouter()

class BookingCreateSchema(BaseModel):
    doctor_id: str
    date: str  # YYYY-MM-DD
    time_slot: str  # e.g., "10:00 AM"
    consultation_type: str = "in_person"
    fee_amount: float

class StatusUpdateSchema(BaseModel):
    status: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_booking(booking_data: BookingCreateSchema, current_user: User = Depends(get_current_user)):
    if current_user.role != "patient":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only patients can book appointments")
        
    try:
        doctor = await User.get(PydanticObjectId(booking_data.doctor_id))
        if not doctor or doctor.role != "doctor":
            raise HTTPException(status_code=404, detail="Doctor not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid doctor ID")
        
    booking = Booking(
        patient_id=str(current_user.id),
        doctor_id=booking_data.doctor_id,
        date=booking_data.date,
        time_slot=booking_data.time_slot,
        consultation_type=booking_data.consultation_type,
        fee_amount=booking_data.fee_amount,
        status="pending",
        payment_status="paid"
    )
    await booking.insert()
    return booking

@router.get("/my-appointments")
async def get_my_appointments(current_user: User = Depends(get_current_user)):
    if current_user.role != "patient":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    bookings = await Booking.find(Booking.patient_id == str(current_user.id)).sort(-Booking.created_at).to_list()
    res = []
    for b in bookings:
        try:
            doc = await User.get(PydanticObjectId(b.doctor_id))
        except Exception:
            doc = None
            
        res.append({
            "id": str(b.id),
            "date": b.date,
            "time_slot": b.time_slot,
            "consultation_type": b.consultation_type,
            "status": b.status,
            "fee_amount": b.fee_amount,
            "payment_status": b.payment_status,
            "doctor_name": f"Dr. {doc.first_name} {doc.last_name}" if doc else "Unknown Doctor",
            "specialty": doc.specialty if doc else "General",
            "avatar_url": doc.avatar_url if doc else None,
            "location": doc.location if doc else "Online"
        })
    return res

@router.get("/doctor-appointments")
async def get_doctor_appointments(current_user: User = Depends(get_current_user)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        
    bookings = await Booking.find(Booking.doctor_id == str(current_user.id)).sort(-Booking.created_at).to_list()
    res = []
    for b in bookings:
        try:
            pat = await User.get(PydanticObjectId(b.patient_id))
        except Exception:
            pat = None
            
        res.append({
            "id": str(b.id),
            "date": b.date,
            "time_slot": b.time_slot,
            "consultation_type": b.consultation_type,
            "status": b.status,
            "fee_amount": b.fee_amount,
            "payment_status": b.payment_status,
            "patient_name": f"{pat.first_name} {pat.last_name}" if pat else "Unknown Patient",
            "phone": pat.phone if pat else "N/A",
            "email": pat.email if pat else "N/A"
        })
    return res

@router.put("/{booking_id}/status")
async def update_booking_status(booking_id: str, data: StatusUpdateSchema, current_user: User = Depends(get_current_user)):
    try:
        booking = await Booking.get(PydanticObjectId(booking_id))
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid booking ID")
        
    # Only the assigned doctor or admin can change status
    if current_user.role != "admin" and str(current_user.id) != booking.doctor_id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update status")
         
    booking.status = data.status
    await booking.save()
    return {"message": f"Booking status updated to {data.status}"}
