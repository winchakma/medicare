import os

MODELS_DIR = "c:/Users/user/Desktop/doctor/backend/app/models"

user_content = """from beanie import Document
from pydantic import Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class User(Document):
    email: str
    password_hash: str
    role: str = "patient"  # patient, doctor, admin
    
    # Common Profile
    first_name: str
    last_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Doctor Specific Fields
    specialty: Optional[str] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    fee_per_visit: Optional[float] = None
    is_verified: bool = False
    
    # Availability Schedule (e.g., {"Monday": [{"start": "09:00", "end": "17:00"}], ...})
    schedule: Optional[Dict[str, List[Dict[str, str]]]] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
"""

booking_content = """from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Booking(Document):
    patient_id: str
    doctor_id: str
    
    date: str  # YYYY-MM-DD
    time_slot: str  # e.g. "10:00 AM"
    
    consultation_type: str = "in_person" # in_person, video
    status: str = "pending" # pending, confirmed, cancelled, completed
    
    fee_amount: float
    payment_status: str = "pending" # pending, paid
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "bookings"
"""

admin_content = """from beanie import Document
from pydantic import Field
from datetime import datetime

class AdminConfig(Document):
    platform_fee_percentage: float = 10.0
    total_revenue: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "admin_configs"
"""

with open(os.path.join(MODELS_DIR, "user.py"), "w") as f: f.write(user_content)
with open(os.path.join(MODELS_DIR, "booking.py"), "w") as f: f.write(booking_content)
with open(os.path.join(MODELS_DIR, "admin.py"), "w") as f: f.write(admin_content)

print("Models created.")
