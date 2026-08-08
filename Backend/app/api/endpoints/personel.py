from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from pydantic import BaseModel, field_validator
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.deps import get_current_user_from_jwt, CurrentUser
import os
import uuid
import shutil

router = APIRouter()


class PersonelBase(BaseModel):
    nip: Optional[str] = None
    nama: str
    jabatan: Optional[str] = None
    pangkat: Optional[str] = None
    golongan: Optional[str] = None
    tahun: Optional[int] = 2026
    kedudukan: Optional[int] = 1
    id_sub_pd: Optional[int] = None
    foto_profil: Optional[str] = None

    @field_validator('nip')
    def nip_must_not_have_spaces(cls, v):
        if v is not None:
            v_cleaned = v.replace(" ", "").strip()
            if " " in v:
                raise ValueError("NIP tidak boleh mengandung spasi")
            return v_cleaned
        return v


class PersonelCreate(PersonelBase):
    pass


class PersonelUpdate(BaseModel):
    nip: Optional[str] = None
    nama: Optional[str] = None
    jabatan: Optional[str] = None
    pangkat: Optional[str] = None
    golongan: Optional[str] = None
    tahun: Optional[int] = None
    kedudukan: Optional[int] = None
    id_sub_pd: Optional[int] = None
    foto_profil: Optional[str] = None

    @field_validator('nip')
    def nip_must_not_have_spaces(cls, v):
        if v is not None:
            v_cleaned = v.replace(" ", "").strip()
            if " " in v:
                raise ValueError("NIP tidak boleh mengandung spasi")
            return v_cleaned
        return v


# Upload Endpoint for Profile Photo
@router.post("/upload-foto")
async def upload_foto_profil(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar (JPG, PNG, WEBP)")

    try:
        ext = os.path.splitext(file.filename)[1].lower()
        if not ext or ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            ext = ".jpg"

        filename = f"foto_{uuid.uuid4().hex[:12]}{ext}"
        
        # Path: Backend/uploads/
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        uploads_dir = os.path.join(backend_dir, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        filepath = os.path.join(uploads_dir, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"/uploads/{filename}"
        return {"url": file_url, "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengunggah foto: {str(e)}")


# Endpoint Level 1: Daftar OPD order by kode + Jumlah Personel
@router.get("/opd")
def get_opd_list(
    q: Optional[str] = Query(None, description="Search query by OPD name or kode"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        where_clauses = []
        params = {}

        # Secure Backend Enforced Rule: Extract role_id and id_opds directly from JWT
        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if current_user.id_opds and len(current_user.id_opds) > 0:
                where_clauses.append("o.id_sub_pd = ANY(:id_opds)")
                params["id_opds"] = current_user.id_opds
            else:
                return []

        if q and q.strip():
            where_clauses.append("(o.nama_pd ILIKE :q OR o.kode ILIKE :q OR o.nama_pd_singkat ILIKE :q)")
            params["q"] = f"%{q.strip()}%"

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        sql = text(f"""
            SELECT 
                o.id_sub_pd, 
                o.kode, 
                o.nama_pd, 
                o.nama_pd_singkat,
                COALESCE(COUNT(p.id), 0) as jumlah_personel
            FROM ta_opd o
            LEFT JOIN ta_personel p ON o.id_sub_pd = p.id_sub_pd
            {where_sql}
            GROUP BY o.id_sub_pd, o.kode, o.nama_pd, o.nama_pd_singkat
            ORDER BY o.kode ASC
        """)

        rows = db.execute(sql, params).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Endpoint Level 2: Daftar Personel (Filtered by id_sub_pd if provided)
@router.get("/")
def get_personel(
    id_sub_pd: Optional[int] = Query(None, description="Filter by OPD id_sub_pd"),
    q: Optional[str] = Query(None, description="Search query by name, NIP, or jabatan"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    offset = (page - 1) * limit
    try:
        where_clauses = []
        params = {"limit": limit, "offset": offset}

        # Secure Backend Enforced Rule: Extract role_id and id_opds directly from JWT
        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if current_user.id_opds and len(current_user.id_opds) > 0:
                if id_sub_pd is not None and id_sub_pd in current_user.id_opds:
                    where_clauses.append("p.id_sub_pd = :id_sub_pd")
                    params["id_sub_pd"] = id_sub_pd
                else:
                    where_clauses.append("p.id_sub_pd = ANY(:allowed_opds)")
                    params["allowed_opds"] = current_user.id_opds
            else:
                return {"total": 0, "page": page, "limit": limit, "data": []}
        elif id_sub_pd is not None:
            where_clauses.append("p.id_sub_pd = :id_sub_pd")
            params["id_sub_pd"] = id_sub_pd

        if q and q.strip():
            where_clauses.append("(p.nama ILIKE :q OR p.nip ILIKE :q OR p.jabatan ILIKE :q)")
            params["q"] = f"%{q.strip()}%"

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        sql = text(f"""
            SELECT p.id, p.nip, p.nama, p.jabatan, p.pangkat, p.golongan, p.tahun, p.kedudukan, p.id_sub_pd, p.foto_profil,
                   o.nama_pd, o.kode as kode_opd
            FROM ta_personel p
            LEFT JOIN ta_opd o ON p.id_sub_pd = o.id_sub_pd
            {where_sql}
            ORDER BY p.id DESC 
            LIMIT :limit OFFSET :offset
        """)

        count_sql = text(f"""
            SELECT COUNT(*) 
            FROM ta_personel p
            {where_sql}
        """)

        rows = db.execute(sql, params).mappings().all()
        total = db.execute(count_sql, params).scalar() or 0

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": [dict(r) for r in rows]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/{personel_id}")
def get_personel_by_id(personel_id: int, db: Session = Depends(get_db)):
    sql = text("""
        SELECT p.*, o.nama_pd, o.kode as kode_opd 
        FROM ta_personel p 
        LEFT JOIN ta_opd o ON p.id_sub_pd = o.id_sub_pd 
        WHERE p.id = :id
    """)
    row = db.execute(sql, {"id": personel_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personel tidak ditemukan")
    return dict(row)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_personel(payload: PersonelCreate, db: Session = Depends(get_db)):
    clean_nip = payload.nip.replace(" ", "").strip() if payload.nip else None

    try:
        sql = text("""
            INSERT INTO ta_personel (nip, nama, jabatan, pangkat, golongan, tahun, kedudukan, id_sub_pd, foto_profil)
            VALUES (:nip, :nama, :jabatan, :pangkat, :golongan, :tahun, :kedudukan, :id_sub_pd, :foto_profil)
            RETURNING id, nip, nama, jabatan, pangkat, golongan, tahun, kedudukan, id_sub_pd, foto_profil
        """)
        new_row = db.execute(sql, {
            "nip": clean_nip,
            "nama": payload.nama,
            "jabatan": payload.jabatan,
            "pangkat": payload.pangkat,
            "golongan": payload.golongan,
            "tahun": payload.tahun or 2026,
            "kedudukan": payload.kedudukan or 1,
            "id_sub_pd": payload.id_sub_pd,
            "foto_profil": payload.foto_profil
        }).mappings().first()
        db.commit()
        return dict(new_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menambah personel: {str(e)}")


@router.put("/{personel_id}")
def update_personel(personel_id: int, payload: PersonelUpdate, db: Session = Depends(get_db)):
    check_sql = text("SELECT id FROM ta_personel WHERE id = :id")
    if not db.execute(check_sql, {"id": personel_id}).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personel tidak ditemukan")

    clean_nip = payload.nip.replace(" ", "").strip() if payload.nip else None

    try:
        sql = text("""
            UPDATE ta_personel
            SET nip = COALESCE(:nip, nip),
                nama = COALESCE(:nama, nama),
                jabatan = COALESCE(:jabatan, jabatan),
                pangkat = COALESCE(:pangkat, pangkat),
                golongan = COALESCE(:golongan, golongan),
                tahun = COALESCE(:tahun, tahun),
                kedudukan = COALESCE(:kedudukan, kedudukan),
                id_sub_pd = COALESCE(:id_sub_pd, id_sub_pd),
                foto_profil = COALESCE(:foto_profil, foto_profil)
            WHERE id = :id
            RETURNING id, nip, nama, jabatan, pangkat, golongan, tahun, kedudukan, id_sub_pd, foto_profil
        """)
        updated_row = db.execute(sql, {
            "id": personel_id,
            "nip": clean_nip,
            "nama": payload.nama,
            "jabatan": payload.jabatan,
            "pangkat": payload.pangkat,
            "golongan": payload.golongan,
            "tahun": payload.tahun,
            "kedudukan": payload.kedudukan,
            "id_sub_pd": payload.id_sub_pd,
            "foto_profil": payload.foto_profil
        }).mappings().first()
        db.commit()
        return dict(updated_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal mengupdate personel: {str(e)}")


@router.delete("/{personel_id}")
def delete_personel(personel_id: int, db: Session = Depends(get_db)):
    check_sql = text("SELECT id FROM ta_personel WHERE id = :id")
    if not db.execute(check_sql, {"id": personel_id}).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personel tidak ditemukan")

    try:
        delete_sql = text("DELETE FROM ta_personel WHERE id = :id")
        db.execute(delete_sql, {"id": personel_id})
        db.commit()
        return {"message": "Personel berhasil dihapus", "id": personel_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menghapus personel: {str(e)}")
