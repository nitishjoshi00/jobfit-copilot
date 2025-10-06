from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .auth import UserIdDep
from .models import Profile, JobPreference, JobNote
from . import repo

app = FastAPI(title="JobFit Copilot API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/profile", response_model=Profile)
def get_profile(user_id: str = UserIdDep):
    p = repo.get_profile(user_id)
    if not p:
        raise HTTPException(status_code=404, detail="Profile not found")
    return p

@app.post("/profile", response_model=Profile)
def upsert_profile(payload: Profile, user_id: str = UserIdDep):
    payload.user_id = user_id
    return repo.upsert_profile(payload)

@app.get("/preferences", response_model=JobPreference)
def get_prefs(user_id: str = UserIdDep):
    p = repo.get_prefs(user_id)
    if not p:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return p

@app.post("/preferences", response_model=JobPreference)
def upsert_prefs(payload: JobPreference, user_id: str = UserIdDep):
    payload.user_id = user_id
    return repo.upsert_prefs(payload)

@app.get("/notes", response_model=list[JobNote])
def list_notes(user_id: str = UserIdDep):
    return repo.list_notes(user_id)

@app.post("/notes", response_model=JobNote)
def create_note(payload: JobNote, user_id: str = UserIdDep):
    payload.user_id = user_id
    return repo.create_note(payload)

@app.patch("/notes/{note_id}", response_model=JobNote)
def patch_note(note_id: str, patch: dict, user_id: str = UserIdDep):
    n = repo.update_note(user_id, note_id, patch)
    if not n:
        raise HTTPException(status_code=404, detail="Note not found")
    return n

@app.delete("/notes/{note_id}")
def remove_note(note_id: str, user_id: str = UserIdDep):
    ok = repo.delete_note(user_id, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"deleted": True}
