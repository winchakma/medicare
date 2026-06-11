from beanie import Document
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
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    fee_per_visit: Optional[float] = None
    is_verified: bool = False
    
    # Availability Schedule (e.g., {"Monday": [{"start": "09:00", "end": "17:00"}], ...})
    schedule: Optional[Dict[str, List[Dict[str, str]]]] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
