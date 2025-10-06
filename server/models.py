from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Profile(BaseModel):
    user_id: str
    name: Optional[str] = None
    role_target: Optional[str] = None
    skills: List[str] = []
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JobPreference(BaseModel):
    user_id: str
    locations: List[str] = []
    salary_min: Optional[int] = None
    salary_currency: str = "EUR"
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JobNote(BaseModel):
    id: Optional[str] = None
    user_id: str
    job_url: str
    company: str
    title: str
    status: str = "saved"
    tags: List[str] = []
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
