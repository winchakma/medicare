import re

file_path = r"c:\Users\user\Desktop\doctor\backend\app\routes\admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_routes = """
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
    return [{"id": str(d.id), "name": f"Dr. {d.first_name} {d.last_name}", "email": d.email, "specialty": d.specialty or "General", "experience": d.experience_years or 0, "fee": d.fee_per_visit or 0, "verified": d.is_verified, "created_at": d.created_at} for d in doctors]

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

@router.put("/settings")
async def update_settings(data: SettingsUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    await current_user.save()
    return {"message": "Settings updated"}
"""

content += "\n" + new_routes

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated admin.py")
