from beanie import Document
from pydantic import Field
from datetime import datetime

class AdminConfig(Document):
    platform_fee_percentage: float = 10.0
    total_revenue: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "admin_configs"
