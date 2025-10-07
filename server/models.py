from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

# --- Table models ---
class Profile(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    name: Optional[str] = None
    role_target: Optional[str] = None
    skills: Optional[str] = None  # comma-separated
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JobPreference(SQLModel, table=True):
    user_id: str = Field(primary_key=True)
    locations: Optional[str] = None  # comma-separated
    salary_min: Optional[int] = None
    salary_currency: str = "EUR"
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JobNote(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    job_url: str
    company: str
    title: str
    status: str = "saved"  # saved | applied | interviewing | offer | rejected
    tags: Optional[str] = None  # comma-separated
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# --- IO schemas (no table=True) ---
class ProfileUpsert(SQLModel):
    name: Optional[str] = None
    role_target: Optional[str] = None
    skills: List[str] = []

class JobPreferenceUpsert(SQLModel):
    locations: List[str] = []
    salary_min: Optional[int] = None
    salary_currency: str = "EUR"

class JobNoteCreate(SQLModel):
    job_url: str
    company: str
    title: str
    tags: List[str] = []
    notes: Optional[str] = None

class JobNoteRead(SQLModel):
    id: str
    job_url: str
    company: str
    title: str
    status: str
    tags: List[str] = []
    notes: Optional[str] = None
