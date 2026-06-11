import re

file_path = r"c:\Users\user\Desktop\doctor\backend\app\routes\admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add avatar_url to /doctors
old_doctor_return = 'return [{"id": str(d.id), "name": f"Dr. {d.first_name} {d.last_name}", "email": d.email, "specialty": d.specialty or "General", "experience": d.experience_years or 0, "fee": d.fee_per_visit or 0, "verified": d.is_verified, "created_at": d.created_at} for d in doctors]'
new_doctor_return = 'return [{"id": str(d.id), "name": f"Dr. {d.first_name} {d.last_name}", "email": d.email, "specialty": d.specialty or "General", "experience": d.experience_years or 0, "fee": d.fee_per_visit or 0, "verified": d.is_verified, "created_at": d.created_at, "avatar_url": d.avatar_url, "bio": d.bio, "location": d.location, "phone": d.phone} for d in doctors]'
content = content.replace(old_doctor_return, new_doctor_return)

# 2. Add avatar_url to the /me or /auth/me wait, admin profile is just via get_current_user in auth.py
# Let's add password to SettingsUpdate
content = content.replace("class SettingsUpdate(BaseModel):\n    first_name: str\n    last_name: str", "class SettingsUpdate(BaseModel):\n    first_name: str\n    last_name: str\n    password: str = None")

# 3. Update /settings
old_settings_route = """@router.put("/settings")
async def update_settings(data: SettingsUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    await current_user.save()
    return {"message": "Settings updated"}"""

new_settings_route = """@router.put("/settings")
async def update_settings(data: SettingsUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    
    if data.password:
        from app.utils.auth import get_password_hash
        current_user.password_hash = get_password_hash(data.password)
        
    await current_user.save()
    return {"message": "Settings updated"}"""

content = content.replace(old_settings_route, new_settings_route)

# 4. Add /upload-avatar
upload_avatar_route = """
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
"""

if "upload_admin_avatar" not in content:
    content += upload_avatar_route

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated admin.py")
