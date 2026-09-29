# security.py
import bcrypt
from fastapi import HTTPException


def hash_password(password: str) -> str:
    """Hashes a plain-text password using Bcrypt."""
    try:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Error hashing password")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against the stored hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
