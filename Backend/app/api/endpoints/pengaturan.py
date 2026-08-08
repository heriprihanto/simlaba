from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, field_validator
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.email import send_reset_password_email
import string
import random
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

ROLE_MAP = {
    1: "User Admin",
    2: "Admin Bidang",
    3: "Supervisor",
    4: "Auditor",
    5: "Verifikator",
    6: "Kepala OPD",
    7: "Kepala Bidang OPD",
    8: "Kepala Sub Bidang OPD",
    9: "Staff OPD"
}


def generate_random_8char_password() -> str:
    """
    Generates an 8-character random password containing at least 1 uppercase letter,
    1 lowercase letter, and 1 digit.
    """
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits

    pwd = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits)
    ]

    all_allowed = uppercase + lowercase + digits
    pwd += [random.choice(all_allowed) for _ in range(5)]
    random.shuffle(pwd)
    return "".join(pwd)


# Pydantic Schemas for User
class UserCreate(BaseModel):
    username: str
    nama: str
    email: Optional[str] = None
    password: str
    role_id: int
    id_opds: Optional[List[int]] = None
    no_telp: Optional[str] = None
    jabatan: Optional[str] = None
    active: Optional[int] = 1

    @field_validator('username')
    def username_must_not_have_spaces(cls, v):
        if v is not None:
            v_cleaned = v.replace(" ", "").strip()
            if " " in v:
                raise ValueError("Username tidak boleh mengandung spasi")
            return v_cleaned
        return v


class UserUpdate(BaseModel):
    nama: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    id_opds: Optional[List[int]] = None
    no_telp: Optional[str] = None
    jabatan: Optional[str] = None
    active: Optional[int] = None


class UserToggleActive(BaseModel):
    active: int


# Pydantic Schemas for OPD
class OpdCreate(BaseModel):
    kode: str
    nama_pd: str
    nama_pd_singkat: Optional[str] = None
    nip_kepala: Optional[str] = None
    nama_kepala: Optional[str] = None
    jabatan_kepala: Optional[str] = None
    alamat: Optional[str] = None
    telp: Optional[str] = None
    email: Optional[str] = None
    aktif: Optional[int] = 1


class OpdUpdate(BaseModel):
    kode: Optional[str] = None
    nama_pd: Optional[str] = None
    nama_pd_singkat: Optional[str] = None
    nip_kepala: Optional[str] = None
    nama_kepala: Optional[str] = None
    jabatan_kepala: Optional[str] = None
    alamat: Optional[str] = None
    telp: Optional[str] = None
    email: Optional[str] = None
    aktif: Optional[int] = None


# Pydantic Schemas for Tagging
class TaggingCreate(BaseModel):
    tag: str
    ket: Optional[str] = None


class TaggingUpdate(BaseModel):
    tag: Optional[str] = None
    ket: Optional[str] = None


# -------------------------------------------------------------
# 1. USER MANAGEMENT ENDPOINTS (sso_users)
# -------------------------------------------------------------

@router.get("/users")
def get_users(
    q: Optional[str] = Query(None, description="Search by username, nama, or email"),
    role_id: Optional[int] = Query(None, description="Filter by role_id"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    try:
        where_clauses = ["COALESCE(deleted, 0) = 0"]
        params = {"limit": limit, "offset": offset}

        if q and q.strip():
            where_clauses.append("(username ILIKE :q OR nama ILIKE :q OR email ILIKE :q)")
            params["q"] = f"%{q.strip()}%"

        if role_id is not None:
            where_clauses.append("role_id = :role_id")
            params["role_id"] = role_id

        where_sql = "WHERE " + " AND ".join(where_clauses)

        sql = text(f"""
            SELECT id, role_id, email, username, nama, last_login, created_on,
                   active, no_telp, jabatan, id_opds
            FROM sso_users
            {where_sql}
            ORDER BY created_on DESC NULLS LAST, username ASC
            LIMIT :limit OFFSET :offset
        """)

        count_sql = text(f"""
            SELECT COUNT(*) 
            FROM sso_users
            {where_sql}
        """)

        rows = db.execute(sql, params).mappings().all()
        total = db.execute(count_sql, params).scalar() or 0

        data = []
        for r in rows:
            user_dict = dict(r)
            user_dict["id"] = str(user_dict["id"])
            user_dict["role_name"] = ROLE_MAP.get(user_dict.get("role_id"), f"Role {user_dict.get('role_id')}")
            data.append(user_dict)

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "roles": ROLE_MAP,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    check_sql = text("SELECT id FROM sso_users WHERE username = :username AND COALESCE(deleted, 0) = 0")
    if db.execute(check_sql, {"username": payload.username}).first():
        raise HTTPException(status_code=400, detail=f"Username '{payload.username}' sudah digunakan")

    try:
        sql = text("""
            INSERT INTO sso_users (
                id, username, nama, email, password, role_id, id_opds, no_telp, jabatan, active, created_on, deleted
            )
            VALUES (
                gen_random_uuid(), :username, :nama, :email, encode_passwd(:username, :password),
                :role_id, :id_opds, :no_telp, :jabatan, :active, NOW(), 0
            )
            RETURNING id, username, nama, email, role_id, id_opds, active
        """)
        
        opds_val = payload.id_opds if payload.id_opds else None

        new_row = db.execute(sql, {
            "username": payload.username.strip(),
            "nama": payload.nama.strip(),
            "email": payload.email.strip() if payload.email else None,
            "password": payload.password,
            "role_id": payload.role_id,
            "id_opds": opds_val,
            "no_telp": payload.no_telp,
            "jabatan": payload.jabatan,
            "active": payload.active if payload.active is not None else 1
        }).mappings().first()
        db.commit()
        
        res = dict(new_row)
        res["id"] = str(res["id"])
        res["role_name"] = ROLE_MAP.get(res.get("role_id"), f"Role {res.get('role_id')}")
        return res
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menambah user: {str(e)}")


@router.put("/users/{user_id}")
def update_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db)):
    check_sql = text("SELECT id, username FROM sso_users WHERE id = :id AND COALESCE(deleted, 0) = 0")
    existing = db.execute(check_sql, {"id": user_id}).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    try:
        update_fields = []
        params = {"id": user_id}

        if payload.nama is not None:
            update_fields.append("nama = :nama")
            params["nama"] = payload.nama.strip()

        if payload.email is not None:
            update_fields.append("email = :email")
            params["email"] = payload.email.strip()

        if payload.role_id is not None:
            update_fields.append("role_id = :role_id")
            params["role_id"] = payload.role_id

        if payload.id_opds is not None:
            update_fields.append("id_opds = :id_opds")
            params["id_opds"] = payload.id_opds if len(payload.id_opds) > 0 else None

        if payload.no_telp is not None:
            update_fields.append("no_telp = :no_telp")
            params["no_telp"] = payload.no_telp

        if payload.jabatan is not None:
            update_fields.append("jabatan = :jabatan")
            params["jabatan"] = payload.jabatan

        if payload.active is not None:
            update_fields.append("active = :active")
            params["active"] = payload.active

        if payload.password and payload.password.strip():
            update_fields.append("password = encode_passwd(:username, :password)")
            params["username"] = existing.username
            params["password"] = payload.password

        if not update_fields:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diubah")

        sql = text(f"""
            UPDATE sso_users
            SET {", ".join(update_fields)}
            WHERE id = :id
            RETURNING id, username, nama, email, role_id, id_opds, active
        """)

        updated_row = db.execute(sql, params).mappings().first()
        db.commit()

        res = dict(updated_row)
        res["id"] = str(res["id"])
        res["role_name"] = ROLE_MAP.get(res.get("role_id"), f"Role {res.get('role_id')}")
        return res
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal mengupdate user: {str(e)}")


@router.put("/users/{user_id}/status")
def toggle_user_status(user_id: str, payload: UserToggleActive, db: Session = Depends(get_db)):
    check_sql = text("SELECT id, username FROM sso_users WHERE id = :id AND COALESCE(deleted, 0) = 0")
    if not db.execute(check_sql, {"id": user_id}).first():
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    try:
        sql = text("UPDATE sso_users SET active = :active WHERE id = :id RETURNING id, username, active")
        row = db.execute(sql, {"id": user_id, "active": payload.active}).mappings().first()
        db.commit()
        res = dict(row)
        res["id"] = str(res["id"])
        return res
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal mengubah status user: {str(e)}")


@router.put("/users/{user_id}/reset-password")
def reset_user_password_random(user_id: str, db: Session = Depends(get_db)):
    check_sql = text("SELECT id, username, nama, email FROM sso_users WHERE id = :id AND COALESCE(deleted, 0) = 0")
    existing = db.execute(check_sql, {"id": user_id}).mappings().first()
    if not existing:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    new_password = generate_random_8char_password()

    try:
        sql = text("""
            UPDATE sso_users
            SET password = encode_passwd(:username, :new_password)
            WHERE id = :id
            RETURNING id, username, email
        """)
        db.execute(sql, {
            "id": user_id,
            "username": existing["username"],
            "new_password": new_password
        })
        db.commit()

        user_email = existing.get("email")
        email_sent = False

        if user_email and "@" in user_email:
            email_sent = send_reset_password_email(
                recipient_email=user_email,
                recipient_name=existing.get("nama") or existing["username"],
                username=existing["username"],
                new_password=new_password
            )

        return {
            "message": f"Password user '{existing['username']}' berhasil di-reset",
            "id": str(user_id),
            "username": existing["username"],
            "nama": existing.get("nama"),
            "email": user_email,
            "generated_password": new_password,
            "email_sent": email_sent
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal reset password: {str(e)}")


@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    check_sql = text("SELECT id FROM sso_users WHERE id = :id AND COALESCE(deleted, 0) = 0")
    if not db.execute(check_sql, {"id": user_id}).first():
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    try:
        sql = text("UPDATE sso_users SET deleted = 1, active = 0 WHERE id = :id")
        db.execute(sql, {"id": user_id})
        db.commit()
        return {"message": "User berhasil dihapus", "id": user_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menghapus user: {str(e)}")


# -------------------------------------------------------------
# 2. PERANGKAT DAERAH MANAGEMENT ENDPOINTS (ta_opd CRUD)
# -------------------------------------------------------------

@router.get("/opd")
def get_opd_setting(
    q: Optional[str] = Query(None, description="Search OPD by kode, nama, or kepalaname"),
    db: Session = Depends(get_db)
):
    try:
        if q and q.strip():
            pattern = f"%{q.strip()}%"
            sql = text("""
                SELECT id_sub_pd, id_pd, kode, nama_pd, nama_pd_singkat,
                       nip_kepala, nama_kepala, jabatan_kepala, alamat, telp, email, aktif
                FROM ta_opd
                WHERE nama_pd ILIKE :q OR kode ILIKE :q OR nama_pd_singkat ILIKE :q OR nama_kepala ILIKE :q
                ORDER BY kode ASC
            """)
            params = {"q": pattern}
        else:
            sql = text("""
                SELECT id_sub_pd, id_pd, kode, nama_pd, nama_pd_singkat,
                       nip_kepala, nama_kepala, jabatan_kepala, alamat, telp, email, aktif
                FROM ta_opd
                ORDER BY kode ASC
            """)
            params = {}

        rows = db.execute(sql, params).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/opd", status_code=status.HTTP_201_CREATED)
def create_opd(payload: OpdCreate, db: Session = Depends(get_db)):
    check_sql = text("SELECT id_sub_pd FROM ta_opd WHERE kode = :kode")
    if db.execute(check_sql, {"kode": payload.kode.strip()}).first():
        raise HTTPException(status_code=400, detail=f"Kode OPD '{payload.kode}' sudah digunakan")

    try:
        next_id_sql = text("SELECT COALESCE(MAX(id_sub_pd), 0) + 1 FROM ta_opd")
        next_id = db.execute(next_id_sql).scalar()

        sql = text("""
            INSERT INTO ta_opd (
                id_sub_pd, id_pd, kode, nama_pd, nama_pd_singkat,
                nip_kepala, nama_kepala, jabatan_kepala, alamat, telp, email, aktif
            )
            VALUES (
                :id_sub_pd, :id_sub_pd, :kode, :nama_pd, :nama_pd_singkat,
                :nip_kepala, :nama_kepala, :jabatan_kepala, :alamat, :telp, :email, :aktif
            )
            RETURNING id_sub_pd, kode, nama_pd, nama_pd_singkat, nip_kepala, nama_kepala, jabatan_kepala, aktif
        """)
        new_row = db.execute(sql, {
            "id_sub_pd": next_id,
            "kode": payload.kode.strip(),
            "nama_pd": payload.nama_pd.strip(),
            "nama_pd_singkat": payload.nama_pd_singkat.strip() if payload.nama_pd_singkat else None,
            "nip_kepala": payload.nip_kepala.strip() if payload.nip_kepala else None,
            "nama_kepala": payload.nama_kepala.strip() if payload.nama_kepala else None,
            "jabatan_kepala": payload.jabatan_kepala.strip() if payload.jabatan_kepala else None,
            "alamat": payload.alamat,
            "telp": payload.telp,
            "email": payload.email,
            "aktif": payload.aktif if payload.aktif is not None else 1
        }).mappings().first()
        db.commit()
        return dict(new_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menambah Perangkat Daerah: {str(e)}")


@router.put("/opd/{id_sub_pd}")
def update_opd(id_sub_pd: int, payload: OpdUpdate, db: Session = Depends(get_db)):
    check_sql = text("SELECT id_sub_pd FROM ta_opd WHERE id_sub_pd = :id")
    if not db.execute(check_sql, {"id": id_sub_pd}).first():
        raise HTTPException(status_code=404, detail="Perangkat Daerah tidak ditemukan")

    try:
        sql = text("""
            UPDATE ta_opd
            SET kode = COALESCE(:kode, kode),
                nama_pd = COALESCE(:nama_pd, nama_pd),
                nama_pd_singkat = COALESCE(:nama_pd_singkat, nama_pd_singkat),
                nip_kepala = COALESCE(:nip_kepala, nip_kepala),
                nama_kepala = COALESCE(:nama_kepala, nama_kepala),
                jabatan_kepala = COALESCE(:jabatan_kepala, jabatan_kepala),
                alamat = COALESCE(:alamat, alamat),
                telp = COALESCE(:telp, telp),
                email = COALESCE(:email, email),
                aktif = COALESCE(:aktif, aktif)
            WHERE id_sub_pd = :id
            RETURNING id_sub_pd, kode, nama_pd, nama_pd_singkat, nip_kepala, nama_kepala, jabatan_kepala, aktif
        """)
        updated_row = db.execute(sql, {
            "id": id_sub_pd,
            "kode": payload.kode.strip() if payload.kode else None,
            "nama_pd": payload.nama_pd.strip() if payload.nama_pd else None,
            "nama_pd_singkat": payload.nama_pd_singkat.strip() if payload.nama_pd_singkat else None,
            "nip_kepala": payload.nip_kepala.strip() if payload.nip_kepala else None,
            "nama_kepala": payload.nama_kepala.strip() if payload.nama_kepala else None,
            "jabatan_kepala": payload.jabatan_kepala.strip() if payload.jabatan_kepala else None,
            "alamat": payload.alamat,
            "telp": payload.telp,
            "email": payload.email,
            "aktif": payload.aktif
        }).mappings().first()
        db.commit()
        return dict(updated_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal mengupdate Perangkat Daerah: {str(e)}")


@router.delete("/opd/{id_sub_pd}")
def delete_opd(id_sub_pd: int, db: Session = Depends(get_db)):
    check_sql = text("SELECT id_sub_pd, nama_pd FROM ta_opd WHERE id_sub_pd = :id")
    row = db.execute(check_sql, {"id": id_sub_pd}).first()
    if not row:
        raise HTTPException(status_code=404, detail="Perangkat Daerah tidak ditemukan")

    try:
        sql = text("DELETE FROM ta_opd WHERE id_sub_pd = :id")
        db.execute(sql, {"id": id_sub_pd})
        db.commit()
        return {"message": f"Perangkat Daerah '{row.nama_pd}' berhasil dihapus", "id_sub_pd": id_sub_pd}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menghapus Perangkat Daerah: {str(e)}")


# -------------------------------------------------------------
# 3. TAGGING MANAGEMENT ENDPOINTS (ref_tagging CRUD)
# -------------------------------------------------------------

@router.get("/tagging")
def get_tagging(
    q: Optional[str] = Query(None, description="Search tagging by tag or ket"),
    db: Session = Depends(get_db)
):
    try:
        if q and q.strip():
            sql = text("SELECT id, tag, ket FROM ref_tagging WHERE tag ILIKE :q OR ket ILIKE :q ORDER BY id ASC")
            rows = db.execute(sql, {"q": f"%{q.strip()}%"}).mappings().all()
        else:
            sql = text("SELECT id, tag, ket FROM ref_tagging ORDER BY id ASC")
            rows = db.execute(sql).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/tagging", status_code=status.HTTP_201_CREATED)
def create_tagging(payload: TaggingCreate, db: Session = Depends(get_db)):
    if not payload.tag or not payload.tag.strip():
        raise HTTPException(status_code=400, detail="Nama Tagging tidak boleh kosong")

    try:
        # Sync sequence to max ID
        seq_sync_sql = text("SELECT setval('public.ref_tagging_id_seq', COALESCE((SELECT MAX(id) FROM ref_tagging), 0))")
        db.execute(seq_sync_sql)

        sql = text("""
            INSERT INTO ref_tagging (id, tag, ket)
            VALUES (nextval('public.ref_tagging_id_seq'), :tag, :ket)
            RETURNING id, tag, ket
        """)
        new_row = db.execute(sql, {
            "tag": payload.tag.strip(),
            "ket": payload.ket.strip() if payload.ket else None
        }).mappings().first()
        db.commit()
        return dict(new_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menambah Tagging: {str(e)}")


@router.put("/tagging/{id}")
def update_tagging(id: int, payload: TaggingUpdate, db: Session = Depends(get_db)):
    check_sql = text("SELECT id FROM ref_tagging WHERE id = :id")
    if not db.execute(check_sql, {"id": id}).first():
        raise HTTPException(status_code=404, detail="Tagging tidak ditemukan")

    try:
        sql = text("""
            UPDATE ref_tagging
            SET tag = COALESCE(:tag, tag),
                ket = COALESCE(:ket, ket)
            WHERE id = :id
            RETURNING id, tag, ket
        """)
        updated_row = db.execute(sql, {
            "id": id,
            "tag": payload.tag.strip() if payload.tag else None,
            "ket": payload.ket.strip() if payload.ket else None
        }).mappings().first()
        db.commit()
        return dict(updated_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal mengupdate Tagging: {str(e)}")


@router.delete("/tagging/{id}")
def delete_tagging(id: int, db: Session = Depends(get_db)):
    check_sql = text("SELECT id, tag FROM ref_tagging WHERE id = :id")
    row = db.execute(check_sql, {"id": id}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Tagging tidak ditemukan")

    try:
        sql = text("DELETE FROM ref_tagging WHERE id = :id")
        db.execute(sql, {"id": id})
        db.commit()
        return {"message": f"Tagging '{row['tag']}' berhasil dihapus", "id": id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menghapus Tagging: {str(e)}")
