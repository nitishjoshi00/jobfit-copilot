from typing import Dict, List
from .models import Profile, JobPreference, JobNote
from uuid import uuid4

_db_profiles: Dict[str, Profile] = {}
_db_prefs: Dict[str, JobPreference] = {}
_db_notes: Dict[str, List[JobNote]] = {}

def upsert_profile(p: Profile) -> Profile:
    _db_profiles[p.user_id] = p
    return p

def get_profile(uid: str):
    return _db_profiles.get(uid)

def upsert_prefs(p: JobPreference) -> JobPreference:
    _db_prefs[p.user_id] = p
    return p

def get_prefs(uid: str):
    return _db_prefs.get(uid)

def list_notes(uid: str) -> List[JobNote]:
    return _db_notes.get(uid, [])

def create_note(n: JobNote) -> JobNote:
    n.id = n.id or str(uuid4())
    _db_notes.setdefault(n.user_id, []).append(n)
    return n

def update_note(uid: str, note_id: str, patch: dict):
    notes = _db_notes.get(uid, [])
    for n in notes:
        if n.id == note_id:
            for k, v in patch.items():
                setattr(n, k, v)
            return n
    return None

def delete_note(uid: str, note_id: str) -> bool:
    notes = _db_notes.get(uid, [])
    for i, n in enumerate(notes):
        if n.id == note_id:
            notes.pop(i)
            return True
    return False
