from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.security import decode_token

# Make Bearer token optional for public/internal endpoints while enabling secure JWT extraction
security_bearer = HTTPBearer(auto_error=False)


class CurrentUser:
    def __init__(self, username: Optional[str] = None, role_id: Optional[int] = None, id_opds: Optional[List[int]] = None, nama: Optional[str] = None):
        self.username = username
        self.role_id = role_id
        self.id_opds = id_opds or []
        self.nama = nama or username or "Pengguna"
        self.name = self.nama


def get_current_user_from_jwt(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> Optional[CurrentUser]:
    """
    Extracts authenticated user context (username, role_id, id_opds) securely from JWT token payload.
    If valid JWT token is present in Authorization Bearer header, claims are decoded and verified.
    """
    if not credentials or not credentials.credentials:
        return None

    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        return None

    username = payload.get("sub")
    role_id = payload.get("role_id")
    id_opds = payload.get("id_opds")
    nama = payload.get("nama") or payload.get("name")

    # If role_id, id_opds, or nama is not in token claims, fallback to database lookup by username
    if username and (role_id is None or id_opds is None or not nama):
        try:
            sql = text("SELECT role_id, id_opds, nama FROM sso_users WHERE username = :username AND COALESCE(deleted, 0) = 0")
            row = db.execute(sql, {"username": username}).mappings().first()
            if row:
                if role_id is None: role_id = row.get("role_id")
                if id_opds is None: id_opds = row.get("id_opds")
                if not nama: nama = row.get("nama")
        except Exception:
            pass

    return CurrentUser(username=username, role_id=role_id, id_opds=id_opds, nama=nama)
