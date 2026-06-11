from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.models.booking import Booking
from app.utils.deps import get_current_user
from datetime import datetime, timedelta
from collections import defaultdict
from beanie.operators import In
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

@router.get("/dashboard-stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Total counts
    active_doctors = await User.find(User.role == "doctor").count()
    total_patients = await User.find(User.role == "patient").count()
    
    # Bookings and revenue
    bookings = await Booking.find_all().to_list()
    total_bookings = len(bookings)
    total_revenue = sum(b.fee_amount for b in bookings if b.status not in ["cancelled"])
    
    # Calculate monthly bookings (last 6 months)
    now = datetime.utcnow()
    monthly_counts = defaultdict(int)
    specialty_counts = defaultdict(int)
    
    # We need doctor specialties
    doctor_ids = list(set([b.doctor_id for b in bookings]))
    doctors = await User.find(In(User.id, doctor_ids)).to_list()
    doc_specialty_map = {str(d.id): d.specialty for d in doctors}
    
    # Collect stats
    for b in bookings:
        # Month
        try:
            b_date = datetime.strptime(b.date, "%Y-%m-%d")
            months_ago = (now.year - b_date.year) * 12 + now.month - b_date.month
            if 0 <= months_ago < 6:
                month_name = b_date.strftime("%b")
                monthly_counts[month_name] += 1
        except Exception:
            pass
            
        # Specialty
        spec = doc_specialty_map.get(b.doctor_id, "General")
        if not spec:
            spec = "General"
        specialty_counts[spec] += 1
        
    return {
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "active_doctors": active_doctors,
        "total_patients": total_patients,
        "monthly_bookings": dict(monthly_counts),
        "specialty_distribution": dict(specialty_counts)
    }

@router.get("/appointments")
async def get_recent_appointments(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Get latest 20 bookings
    bookings = await Booking.find_all().sort(-Booking.created_at).limit(20).to_list()
    
    # We need patient and doctor names
    patient_ids = list(set([b.patient_id for b in bookings]))
    doctor_ids = list(set([b.doctor_id for b in bookings]))
    
    users = await User.find(In(User.id, patient_ids + doctor_ids)).to_list()
    user_map = {str(u.id): u for u in users}
    
    results = []
    for b in bookings:
        p = user_map.get(b.patient_id)
        d = user_map.get(b.doctor_id)
        
        results.append({
            "id": str(b.id),
            "booking_id": f"#MC-{str(b.id)[-4:].upper()}",
            "patient_name": f"{p.first_name} {p.last_name}" if p else "Unknown",
            "doctor_name": f"Dr. {d.first_name} {d.last_name}" if d else "Unknown",
            "doctor_initials": f"{d.first_name[0]}{d.last_name[0]}" if d else "UN",
            "specialty": d.specialty if d else "General",
            "date": b.date,
            "time_slot": b.time_slot,
            "fee": b.fee_amount,
            "status": b.status
        })
        
    return results

@router.get("/top-doctors")
async def get_top_doctors(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    bookings = await Booking.find_all().to_list()
    doc_counts = defaultdict(int)
    for b in bookings:
        doc_counts[b.doctor_id] += 1
        
    sorted_docs = sorted(doc_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    results = []
    for doc_id, count in sorted_docs:
        from beanie import PydanticObjectId
        try:
            d = await User.get(PydanticObjectId(doc_id))
            if d:
                results.append({
                    "id": str(d.id),
                    "name": f"Dr. {d.first_name} {d.last_name}",
                    "initials": f"{d.first_name[0]}{d.last_name[0]}",
                    "specialty": d.specialty or "General",
                    "bookings": count,
                    "rating": "4.9" # Placeholder
                })
        except:
            pass
            
    return results
