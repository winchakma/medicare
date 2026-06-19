from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Blog(Document):
    title: str
    category: str
    content: str
    author_id: str
    author_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "blogs"
