from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session
from uuid import uuid4
from typing import List

from .auth import UserIdDep
from .db import init_db, get_session
from .models import (
    Profile, ProfileUpsert,
    JobPreference, JobPreferenceUpsert,
    JobNote, JobNoteCreate, JobNoteRead
)

app = FastAPI(title="JobFit Copilot API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

# --- Profile ---
@app.get("/profile", response_model=Profile)
def get_profile(user_id: str = UserIdDep, session: Session = Depends(get_session)):
    p = session.get(Profile, user_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return p

@app.post("/profile", response_model=Profile)
def upsert_profile(payload: ProfileUpsert, user_id: str = UserIdDep, session: Session = Depends(get_session)):
    p = session.get(Profile, user_id) or Profile(user_id=user_id)
    p.name = payload.name
    p.role_target = payload.role_target
    p.skills = ",".join(payload.skills) if payload.skills else None
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

# --- Preferences ---
@app.get("/preferences", response_model=JobPreference)
def get_prefs(user_id: str = UserIdDep, session: Session = Depends(get_session)):
    p = session.get(JobPreference, user_id)
    if not p:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return p

@app.post("/preferences", response_model=JobPreference)
def upsert_prefs(payload: JobPreferenceUpsert, user_id: str = UserIdDep, session: Session = Depends(get_session)):
    pref = session.get(JobPreference, user_id) or JobPreference(user_id=user_id)
    pref.locations = ",".join(payload.locations) if payload.locations else None
    pref.salary_min = payload.salary_min
    pref.salary_currency = payload.salary_currency
    session.add(pref)
    session.commit()
    session.refresh(pref)
    return pref

# --- Notes ---
@app.get("/notes", response_model=List[JobNoteRead])
def list_notes(user_id: str = UserIdDep, session: Session = Depends(get_session)):
    result = session.exec(
        select(JobNote).where(JobNote.user_id == user_id).order_by(JobNote.created_at.desc())
    )
    notes = result.all()
    return [
        JobNoteRead(
            id=n.id,
            job_url=n.job_url,
            company=n.company,
            title=n.title,
            status=n.status,
            tags=n.tags.split(",") if n.tags else [],
            notes=n.notes
        ) for n in notes
    ]

@app.post("/notes", response_model=JobNoteRead)
def create_note(payload: JobNoteCreate, user_id: str = UserIdDep, session: Session = Depends(get_session)):
    n = JobNote(
        id=str(uuid4()),
        user_id=user_id,
        job_url=payload.job_url,
        company=payload.company,
        title=payload.title,
        status="saved",
        tags=",".join(payload.tags) if payload.tags else None,
        notes=payload.notes
    )
    session.add(n)
    session.commit()
    session.refresh(n)
    return JobNoteRead(
        id=n.id, job_url=n.job_url, company=n.company, title=n.title,
        status=n.status, tags=n.tags.split(",") if n.tags else [], notes=n.notes
    )

@app.patch("/notes/{note_id}", response_model=JobNoteRead)
def patch_note(note_id: str, patch: dict, user_id: str = UserIdDep, session: Session = Depends(get_session)):
    n = session.get(JobNote, note_id)
    if not n or n.user_id != user_id:
        raise HTTPException(status_code=404, detail="Note not found")
    for k, v in patch.items():
        if k == "tags" and isinstance(v, list):
            setattr(n, "tags", ",".join(v))
        else:
            setattr(n, k, v)
    session.add(n)
    session.commit()
    session.refresh(n)
    return JobNoteRead(
        id=n.id, job_url=n.job_url, company=n.company, title=n.title,
        status=n.status, tags=n.tags.split(",") if n.tags else [], notes=n.notes
    )

@app.delete("/notes/{note_id}")
def remove_note(note_id: str, user_id: str = UserIdDep, session: Session = Depends(get_session)):
    n = session.get(JobNote, note_id)
    if not n or n.user_id != user_id:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(n)
    session.commit()
    return {"deleted": True}
