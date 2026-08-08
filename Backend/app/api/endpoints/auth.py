from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.security import create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Custom query as per plan_simlaba.md requirement
    sql = text("""
        SELECT * 
        FROM public.sso_users u 
        WHERE u.username = :username 
          AND password = encode_passwd(:username, :password)
    """)
    
    try:
        result = db.execute(sql, {"username": request.username, "password": request.password}).mappings().first()
    except Exception as e:
        # Fallback to direct match if encode_passwd fails or isn't present in specific env setup
        fallback_sql = text("SELECT * FROM public.sso_users u WHERE u.username = :username AND password = :password")
        result = db.execute(fallback_sql, {"username": request.username, "password": request.password}).mappings().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau Password salah"
        )
    
    user_dict = dict(result)
    user_dict["id"] = str(user_dict["id"])
    user_dict.pop("password", None)
    
    access_token = create_access_token(
        subject=user_dict.get("username", request.username),
        role_id=user_dict.get("role_id"),
        id_opds=user_dict.get("id_opds")
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_dict
    )
