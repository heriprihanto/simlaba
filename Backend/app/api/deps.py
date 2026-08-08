from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> dict:
    if not token:
        # Default guest/admin representation for ease of development if unauthenticated
        return {"id": 1, "username": "admin", "nama": "Administrator", "role": "admin"}
    
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau telah kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload["sub"]
    query = text("SELECT id, username, nama, email FROM public.sso_users WHERE username = :username")
    result = db.execute(query, {"username": username}).mappings().first()
    
    if not result:
        return {"id": 1, "username": username, "nama": username, "role": "user"}
    
    return dict(result)
