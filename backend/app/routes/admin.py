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


@router.get("/patients")
async def get_patients(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    patients = await User.find(User.role == "patient").sort(-User.created_at).to_list()
    return [{"id": str(p.id), "name": f"{p.first_name} {p.last_name}", "email": p.email, "phone": p.phone or "N/A", "created_at": p.created_at} for p in patients]

@router.get("/doctors")
async def get_doctors(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    doctors = await User.find(User.role == "doctor").sort(-User.created_at).to_list()
    return [{"id": str(d.id), "name": f"Dr. {d.first_name} {d.last_name}", "email": d.email, "specialty": d.specialty or "General", "experience": d.experience_years or 0, "fee": d.fee_per_visit or 0, "verified": d.is_verified, "created_at": d.created_at, "avatar_url": d.avatar_url, "bio": d.bio, "location": d.location, "phone": d.phone} for d in doctors]

@router.get("/all-appointments")
async def get_all_appointments(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    # Same as get_recent_appointments but all
    bookings = await Booking.find_all().sort(-Booking.created_at).to_list()
    
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

@router.get("/recent-activity")
async def get_recent_activity(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    activities = []
    
    # Get recent bookings
    recent_bookings = await Booking.find_all().sort(-Booking.created_at).limit(5).to_list()
    patient_ids = list(set([b.patient_id for b in recent_bookings]))
    doctor_ids = list(set([b.doctor_id for b in recent_bookings]))
    
    # Get recent users
    recent_users = await User.find_all().sort(-User.created_at).limit(5).to_list()
    # Add to ids so we don't fetch again
    
    all_user_ids = list(set(patient_ids + doctor_ids + [str(u.id) for u in recent_users]))
    users = await User.find(In(User.id, all_user_ids)).to_list()
    user_map = {str(u.id): u for u in users}
    
    for b in recent_bookings:
        p = user_map.get(b.patient_id)
        d = user_map.get(b.doctor_id)
        d_name = f"Dr. {d.first_name} {d.last_name}" if d else "Unknown"
        action = "confirmed" if b.status == "confirmed" else "booked" if b.status == "pending" else b.status
        color = "var(--teal)" if b.status == "confirmed" else "var(--amber)" if b.status == "pending" else "var(--red)"
        
        activities.append({
            "text": f"Booking #MC-{str(b.id)[-4:].upper()} {action} with {d_name}",
            "time": b.created_at,
            "color": color
        })
        
    for u in recent_users:
        # If created in last 7 days (or just top 5)
        if u.role == "patient":
            activities.append({
                "text": f"New patient registered: {u.first_name} {u.last_name}",
                "time": u.created_at,
                "color": "#185FA5"
            })
        elif u.role == "doctor":
            activities.append({
                "text": f"New doctor joined: Dr. {u.first_name} {u.last_name}",
                "time": u.created_at,
                "color": "#0F6E56"
            })
            
    # Sort by time
    activities.sort(key=lambda x: x["time"], reverse=True)
    
    # Format time
    now = datetime.utcnow()
    results = []
    for a in activities[:6]:
        diff = now - a["time"].replace(tzinfo=None)
        if diff.days > 0:
            time_str = f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            time_str = f"{diff.seconds // 3600} hours ago"
        elif diff.seconds >= 60:
            time_str = f"{diff.seconds // 60} mins ago"
        else:
            time_str = "Just now"
            
        results.append({
            "text": a["text"],
            "time_str": time_str,
            "color": a["color"]
        })
        
    return results

class SettingsUpdate(BaseModel):
    first_name: str
    last_name: str
    password: str = None

@router.put("/settings")
async def update_settings(data: SettingsUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    
    if data.password:
        from app.utils.auth import get_password_hash
        current_user.password_hash = get_password_hash(data.password)
        
    await current_user.save()
    return {"message": "Settings updated"}

from fastapi import File, UploadFile
import os
import shutil

@router.post("/upload-avatar")
async def upload_admin_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    os.makedirs("uploads/avatars", exist_ok=True)
    file_path = f"uploads/avatars/{current_user.id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    current_user.avatar_url = f"/{file_path}"
    await current_user.save()
    return {"avatar_url": current_user.avatar_url}

@router.put("/doctors/{doctor_id}/verify")
async def toggle_doctor_verification(doctor_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    from beanie import PydanticObjectId
    try:
        doctor = await User.get(PydanticObjectId(doctor_id))
        if not doctor or doctor.role != "doctor":
            raise HTTPException(status_code=404, detail="Doctor not found")
        doctor.is_verified = not doctor.is_verified
        await doctor.save()
        return {"message": "Verification status updated", "verified": doctor.is_verified}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    from beanie import PydanticObjectId
    try:
        doctor = await User.get(PydanticObjectId(doctor_id))
        if not doctor or doctor.role != "doctor":
            raise HTTPException(status_code=404, detail="Doctor not found")
        await doctor.delete()
        return {"message": "Doctor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
