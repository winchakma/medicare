from beanie import Document
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
