import uuid
import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api import deps

router = APIRouter()

# ==================== SCHEMAS ====================

class RpjmdVisiUpdate(BaseModel):
    uraivisi: str
    idperiode: Optional[str] = None
    tahunpagu: Optional[str] = None
    kodepemda: Optional[str] = None
    status: Optional[int] = None
    catatan: Optional[str] = None

class RpjmdVisiCreate(BaseModel):
    uraivisi: str
    idperiode: Optional[str] = '2025 - 2029'
    tahunpagu: Optional[str] = '2026 - 2030'
    kodepemda: Optional[str] = '3376'
    status: Optional[int] = 1
    no: Optional[int] = 1

class RpjmdMisiCreate(BaseModel):
    uraimisi: str
    urut: Optional[int] = 1

class RpjmdMisiUpdate(BaseModel):
    uraimisi: str
    urut: Optional[int] = 1

class RpjmdTujuanCreate(BaseModel):
    uraitujuan: str
    urut: Optional[int] = 1
    idmisi: Optional[str] = None
    idperiode: Optional[str] = '20252029'
    kodepemda: Optional[str] = '3376'

class RpjmdTujuanUpdate(BaseModel):
    uraitujuan: str
    urut: Optional[int] = 1
    idmisi: Optional[str] = None

class RpjmdIndikatorTujuanCreate(BaseModel):
    idtujuan: str
    uraitujuan_indikator: str
    satuan: Optional[str] = 'Angka'
    status: Optional[str] = 'positif'
    baseline: Optional[str] = ''
    target0: Optional[str] = ''
    target1: Optional[str] = ''
    target2: Optional[str] = ''
    target3: Optional[str] = ''
    target4: Optional[str] = ''
    target5: Optional[str] = ''
    tipe_data: Optional[str] = 'numeric'
    kodeindikator_master: Optional[str] = None
    sumber: Optional[str] = 'MASTER'
    iku: Optional[bool] = False
    ikd: Optional[bool] = False
    uraiaspek: Optional[str] = None
    urut: Optional[int] = 1
    idperiode: Optional[str] = '20252029'
    kodepemda: Optional[str] = '3376'

class RpjmdIndikatorTujuanUpdate(BaseModel):
    idtujuan: Optional[str] = None
    uraitujuan_indikator: str
    satuan: Optional[str] = 'Angka'
    status: Optional[str] = 'positif'
    baseline: Optional[str] = ''
    target0: Optional[str] = ''
    target1: Optional[str] = ''
    target2: Optional[str] = ''
    target3: Optional[str] = ''
    target4: Optional[str] = ''
    target5: Optional[str] = ''
    tipe_data: Optional[str] = 'numeric'
    kodeindikator_master: Optional[str] = None
    sumber: Optional[str] = 'MASTER'
    iku: Optional[bool] = False
    ikd: Optional[bool] = False
    uraiaspek: Optional[str] = None
    urut: Optional[int] = 1

class RpjmdSasaranCreate(BaseModel):
    uraisasaran: str
    urut: Optional[int] = 1
    idtujuan: Optional[str] = None
    idperiode: Optional[str] = '20252029'
    kodepemda: Optional[str] = '3376'

class RpjmdSasaranUpdate(BaseModel):
    uraisasaran: str
    urut: Optional[int] = 1
    idtujuan: Optional[str] = None

class RpjmdIndikatorSasaranCreate(BaseModel):
    idsasaran: str
    uraisasaran_indikator: str
    satuan: Optional[str] = 'Angka'
    status: Optional[str] = 'positif'
    baseline: Optional[str] = ''
    target0: Optional[str] = ''
    target1: Optional[str] = ''
    target2: Optional[str] = ''
    target3: Optional[str] = ''
    target4: Optional[str] = ''
    target5: Optional[str] = ''
    tipe_data: Optional[str] = 'numeric'
    kodeindikator_master: Optional[str] = None
    sumber: Optional[str] = 'MASTER'
    iku: Optional[bool] = False
    ikd: Optional[bool] = False
    uraiaspek: Optional[str] = None
    urut: Optional[int] = 1
    idperiode: Optional[str] = '20252029'
    kodepemda: Optional[str] = '3376'

class RpjmdIndikatorSasaranUpdate(BaseModel):
    idsasaran: Optional[str] = None
    uraisasaran_indikator: str
    satuan: Optional[str] = 'Angka'
    status: Optional[str] = 'positif'
    baseline: Optional[str] = ''
    target0: Optional[str] = ''
    target1: Optional[str] = ''
    target2: Optional[str] = ''
    target3: Optional[str] = ''
    target4: Optional[str] = ''
    target5: Optional[str] = ''
    tipe_data: Optional[str] = 'numeric'
    kodeindikator_master: Optional[str] = None
    sumber: Optional[str] = 'MASTER'
    iku: Optional[bool] = False
    ikd: Optional[bool] = False
    uraiaspek: Optional[str] = None
    urut: Optional[int] = 1


# ==================== 1. VISI RPJMD ====================

@router.get("/visi")
def get_rpjmd_visi(db: Session = Depends(deps.get_db)) -> Any:
    """
    Mengambil data Visi RPJMD dari tabel rpjmd_visi.
    """
    try:
        sql = text("SELECT * FROM rpjmd_visi ORDER BY no ASC, id ASC LIMIT 1;")
        res = db.execute(sql).mappings().first()
        if res:
            return dict(res)
        
        default_id = str(uuid.uuid4())
        insert_sql = text("""
            INSERT INTO rpjmd_visi (id, idperiode, tahunpagu, status, uraivisi, kodepemda, no, created_at)
            VALUES (:id, '2025 - 2029', '2026 - 2030', 1, 'Tegal Berdikari Dan Sejahtera, Menjadi Kota Idaman', '3376', 1, NOW())
            RETURNING *;
        """)
        new_row = db.execute(insert_sql, {"id": default_id}).mappings().first()
        db.commit()
        return dict(new_row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Visi: {str(e)}")

@router.put("/visi/{visi_id}")
def update_rpjmd_visi(
    visi_id: str,
    visi_in: RpjmdVisiUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengupdate data Visi RPJMD di tabel rpjmd_visi.
    """
    try:
        sql = text("""
            UPDATE rpjmd_visi
            SET uraivisi = :uraivisi,
                idperiode = COALESCE(:idperiode, idperiode),
                tahunpagu = COALESCE(:tahunpagu, tahunpagu)
            WHERE id = :id
            RETURNING *;
        """)
        res = db.execute(sql, {
            "id": visi_id,
            "uraivisi": visi_in.uraivisi,
            "idperiode": visi_in.idperiode,
            "tahunpagu": visi_in.tahunpagu
        }).mappings().first()
        db.commit()
        if not res:
            raise HTTPException(status_code=404, detail="Data Visi RPJMD tidak ditemukan")
        return dict(res)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating RPJMD Visi: {str(e)}")


# ==================== 2. MISI RPJMD ====================

@router.get("/misi")
def get_rpjmd_misi_list(db: Session = Depends(deps.get_db)) -> Any:
    """
    Mengambil seluruh data Misi RPJMD dari tabel rpjmd_misi.
    """
    try:
        sql = text("SELECT * FROM rpjmd_misi ORDER BY urut ASC, idmisi ASC;")
        rows = db.execute(sql).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Misi: {str(e)}")

@router.post("/misi")
def create_rpjmd_misi(
    misi_in: RpjmdMisiCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menambahkan data Misi RPJMD baru ke tabel rpjmd_misi.
    """
    try:
        new_id = str(uuid.uuid4())
        sql = text("""
            INSERT INTO rpjmd_misi (idmisi, uraimisi, urut, postdate)
            VALUES (:idmisi, :uraimisi, :urut, NOW())
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idmisi": new_id,
            "uraimisi": misi_in.uraimisi,
            "urut": misi_in.urut
        }).mappings().first()
        db.commit()
        return dict(row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating RPJMD Misi: {str(e)}")

@router.put("/misi/{idmisi}")
def update_rpjmd_misi(
    idmisi: str,
    misi_in: RpjmdMisiUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengupdate data Misi RPJMD di tabel rpjmd_misi.
    """
    try:
        sql = text("""
            UPDATE rpjmd_misi
            SET uraimisi = :uraimisi,
                urut = :urut,
                postdate = NOW()
            WHERE idmisi = :idmisi
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idmisi": idmisi,
            "uraimisi": misi_in.uraimisi,
            "urut": misi_in.urut
        }).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Misi RPJMD tidak ditemukan")
        return dict(row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating RPJMD Misi: {str(e)}")

@router.delete("/misi/{idmisi}")
def delete_rpjmd_misi(
    idmisi: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menghapus data Misi RPJMD dari tabel rpjmd_misi.
    """
    try:
        sql = text("DELETE FROM rpjmd_misi WHERE idmisi = :idmisi RETURNING *;")
        row = db.execute(sql, {"idmisi": idmisi}).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Misi RPJMD tidak ditemukan")
        return {"status": "success", "message": "Misi RPJMD berhasil dihapus", "deleted": dict(row)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting RPJMD Misi: {str(e)}")


# ==================== 3. TUJUAN & INDIKATOR TUJUAN RPJMD (TREE AGGREGATION) ====================

@router.get("/tujuan-lengkap")
def get_rpjmd_tujuan_lengkap(db: Session = Depends(deps.get_db)) -> Any:
    """
    Mengambil data lengkap Tree Tujuan dan Indikator Tujuan RPJMD beserta relasi Misi.
    """
    try:
        tujuan_sql = text("""
            SELECT 
                t.*,
                tm.idmisi,
                m.urut AS urut_misi,
                m.uraimisi
            FROM rpjmd_tujuan t
            LEFT JOIN rpjmd_tujuan_misi tm ON t.idtujuan = tm.idtujuan
            LEFT JOIN rpjmd_misi m ON tm.idmisi = m.idmisi
            ORDER BY t.urut ASC, t.idtujuan ASC;
        """)
        tujuan_rows = db.execute(tujuan_sql).mappings().all()

        ind_sql = text("""
            SELECT * FROM rpjmd_indikator_tujuan 
            ORDER BY urut ASC, idtujuan_indikator ASC;
        """)
        ind_rows = db.execute(ind_sql).mappings().all()

        ind_map = {}
        for ind in ind_rows:
            t_id = str(ind.get("idtujuan") or "").strip()
            if t_id not in ind_map:
                ind_map[t_id] = []
            ind_map[t_id].append(dict(ind))

        result_tujuan = []
        for t in tujuan_rows:
            t_dict = dict(t)
            t_id = str(t.get("idtujuan") or "").strip()
            t_dict["indikator_list"] = ind_map.get(t_id, [])
            result_tujuan.append(t_dict)

        return {
            "total_tujuan": len(result_tujuan),
            "total_indikator": len(ind_rows),
            "daftar_tujuan": result_tujuan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Tujuan Lengkap: {str(e)}")

@router.get("/tujuan")
def get_rpjmd_tujuan_list(db: Session = Depends(deps.get_db)) -> Any:
    """
    Mengambil daftar Tujuan RPJMD beserta info Misi terkait.
    """
    try:
        sql = text("""
            SELECT 
                t.*,
                tm.idmisi,
                m.urut AS urut_misi,
                m.uraimisi
            FROM rpjmd_tujuan t
            LEFT JOIN rpjmd_tujuan_misi tm ON t.idtujuan = tm.idtujuan
            LEFT JOIN rpjmd_misi m ON tm.idmisi = m.idmisi
            ORDER BY t.urut ASC, t.idtujuan ASC;
        """)
        rows = db.execute(sql).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Tujuan: {str(e)}")

@router.post("/tujuan")
def create_rpjmd_tujuan(
    tujuan_in: RpjmdTujuanCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menambahkan data Tujuan RPJMD baru dan relasi ke tabel rpjmd_tujuan_misi.
    """
    try:
        new_id = str(uuid.uuid4())
        sql = text("""
            INSERT INTO rpjmd_tujuan (idtujuan, uraitujuan, urut, idperiode, kodepemda, created_at)
            VALUES (:idtujuan, :uraitujuan, :urut, :idperiode, :kodepemda, NOW())
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idtujuan": new_id,
            "uraitujuan": tujuan_in.uraitujuan,
            "urut": tujuan_in.urut,
            "idperiode": tujuan_in.idperiode or '20252029',
            "kodepemda": tujuan_in.kodepemda or '3376'
        }).mappings().first()

        if tujuan_in.idmisi:
            db.execute(text("""
                INSERT INTO rpjmd_tujuan_misi (idtujuan, idmisi)
                VALUES (:idtujuan, :idmisi);
            """), {"idtujuan": new_id, "idmisi": tujuan_in.idmisi})

        db.commit()
        return dict(row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating RPJMD Tujuan: {str(e)}")

@router.put("/tujuan/{idtujuan}")
def update_rpjmd_tujuan(
    idtujuan: str,
    tujuan_in: RpjmdTujuanUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengupdate data Tujuan RPJMD dan relasi Misi.
    """
    try:
        sql = text("""
            UPDATE rpjmd_tujuan
            SET uraitujuan = :uraitujuan,
                urut = :urut
            WHERE idtujuan = :idtujuan
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idtujuan": idtujuan,
            "uraitujuan": tujuan_in.uraitujuan,
            "urut": tujuan_in.urut
        }).mappings().first()

        if tujuan_in.idmisi is not None:
            db.execute(text("DELETE FROM rpjmd_tujuan_misi WHERE idtujuan = :idtujuan;"), {"idtujuan": idtujuan})
            if tujuan_in.idmisi != "":
                db.execute(text("""
                    INSERT INTO rpjmd_tujuan_misi (idtujuan, idmisi)
                    VALUES (:idtujuan, :idmisi);
                """), {"idtujuan": idtujuan, "idmisi": tujuan_in.idmisi})

        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Tujuan RPJMD tidak ditemukan")
        return dict(row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating RPJMD Tujuan: {str(e)}")

@router.delete("/tujuan/{idtujuan}")
def delete_rpjmd_tujuan(
    idtujuan: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menghapus data Tujuan RPJMD beserta indikator dan relasi misi terkait.
    """
    try:
        db.execute(text("DELETE FROM rpjmd_tujuan_misi WHERE idtujuan = :idtujuan;"), {"idtujuan": idtujuan})
        db.execute(text("DELETE FROM rpjmd_indikator_tujuan WHERE idtujuan = :idtujuan;"), {"idtujuan": idtujuan})
        sql = text("DELETE FROM rpjmd_tujuan WHERE idtujuan = :idtujuan RETURNING *;")
        row = db.execute(sql, {"idtujuan": idtujuan}).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Tujuan RPJMD tidak ditemukan")
        return {"status": "success", "message": "Tujuan RPJMD berhasil dihapus", "deleted": dict(row)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting RPJMD Tujuan: {str(e)}")


# ==================== 4. INDIKATOR TUJUAN RPJMD ====================

@router.get("/indikator-tujuan")
def get_rpjmd_indikator_tujuan_list(
    idtujuan: Optional[str] = None,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengambil daftar Indikator Tujuan RPJMD.
    """
    try:
        if idtujuan:
            sql = text("SELECT * FROM rpjmd_indikator_tujuan WHERE idtujuan = :idtujuan ORDER BY urut ASC, idtujuan_indikator ASC;")
            rows = db.execute(sql, {"idtujuan": idtujuan}).mappings().all()
        else:
            sql = text("SELECT * FROM rpjmd_indikator_tujuan ORDER BY urut ASC, idtujuan_indikator ASC;")
            rows = db.execute(sql).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Indikator Tujuan: {str(e)}")

@router.post("/indikator-tujuan")
def create_rpjmd_indikator_tujuan(
    ind_in: RpjmdIndikatorTujuanCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menambahkan data Indikator Tujuan RPJMD baru.
    """
    try:
        new_id = str(uuid.uuid4())
        sql = text("""
            INSERT INTO rpjmd_indikator_tujuan (
                idtujuan_indikator, kodepemda, idperiode, idtujuan, uraitujuan_indikator,
                satuan, status, baseline, target0, target1, target2, target3, target4, target5,
                tipe_data, kodeindikator_master, sumber, iku, ikd, uraiaspek, urut, created_at, postdate
            ) VALUES (
                :idtujuan_indikator, :kodepemda, :idperiode, :idtujuan, :uraitujuan_indikator,
                :satuan, :status, :baseline, :target0, :target1, :target2, :target3, :target4, :target5,
                :tipe_data, :kodeindikator_master, :sumber, :iku, :ikd, :uraiaspek, :urut, NOW(), NOW()
            ) RETURNING *;
        """)
        row = db.execute(sql, {
            "idtujuan_indikator": new_id,
            "kodepemda": ind_in.kodepemda or '3376',
            "idperiode": ind_in.idperiode or '20252029',
            "idtujuan": ind_in.idtujuan,
            "uraitujuan_indikator": ind_in.uraitujuan_indikator,
            "satuan": ind_in.satuan or 'Angka',
            "status": ind_in.status or 'positif',
            "baseline": ind_in.baseline or '',
            "target0": ind_in.target0 or '',
            "target1": ind_in.target1 or '',
            "target2": ind_in.target2 or '',
            "target3": ind_in.target3 or '',
            "target4": ind_in.target4 or '',
            "target5": ind_in.target5 or '',
            "tipe_data": ind_in.tipe_data or 'numeric',
            "kodeindikator_master": ind_in.kodeindikator_master,
            "sumber": ind_in.sumber or 'MASTER',
            "iku": ind_in.iku or False,
            "ikd": ind_in.ikd or False,
            "uraiaspek": ind_in.uraiaspek,
            "urut": ind_in.urut or 1
        }).mappings().first()
        db.commit()
        return dict(row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating RPJMD Indikator Tujuan: {str(e)}")

@router.put("/indikator-tujuan/{idtujuan_indikator}")
def update_rpjmd_indikator_tujuan(
    idtujuan_indikator: str,
    ind_in: RpjmdIndikatorTujuanUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengupdate data Indikator Tujuan RPJMD.
    """
    try:
        sql = text("""
            UPDATE rpjmd_indikator_tujuan
            SET uraitujuan_indikator = :uraitujuan_indikator,
                satuan = :satuan,
                status = :status,
                baseline = :baseline,
                target0 = :target0,
                target1 = :target1,
                target2 = :target2,
                target3 = :target3,
                target4 = :target4,
                target5 = :target5,
                tipe_data = :tipe_data,
                kodeindikator_master = :kodeindikator_master,
                sumber = :sumber,
                iku = :iku,
                ikd = :ikd,
                uraiaspek = :uraiaspek,
                urut = :urut,
                lastupdate = NOW()
            WHERE idtujuan_indikator = :idtujuan_indikator
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idtujuan_indikator": idtujuan_indikator,
            "uraitujuan_indikator": ind_in.uraitujuan_indikator,
            "satuan": ind_in.satuan or 'Angka',
            "status": ind_in.status or 'positif',
            "baseline": ind_in.baseline or '',
            "target0": ind_in.target0 or '',
            "target1": ind_in.target1 or '',
            "target2": ind_in.target2 or '',
            "target3": ind_in.target3 or '',
            "target4": ind_in.target4 or '',
            "target5": ind_in.target5 or '',
            "tipe_data": ind_in.tipe_data or 'numeric',
            "kodeindikator_master": ind_in.kodeindikator_master,
            "sumber": ind_in.sumber or 'MASTER',
            "iku": ind_in.iku or False,
            "ikd": ind_in.ikd or False,
            "uraiaspek": ind_in.uraiaspek,
            "urut": ind_in.urut or 1
        }).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Indikator Tujuan RPJMD tidak ditemukan")
        return dict(row)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating RPJMD Indikator Tujuan: {str(e)}")

@router.delete("/indikator-tujuan/{idtujuan_indikator}")
def delete_rpjmd_indikator_tujuan(
    idtujuan_indikator: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menghapus data Indikator Tujuan RPJMD.
    """
    try:
        sql = text("DELETE FROM rpjmd_indikator_tujuan WHERE idtujuan_indikator = :idtujuan_indikator RETURNING *;")
        row = db.execute(sql, {"idtujuan_indikator": idtujuan_indikator}).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Indikator Tujuan RPJMD tidak ditemukan")
        return {"status": "success", "message": "Indikator Tujuan RPJMD berhasil dihapus", "deleted": dict(row)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting RPJMD Indikator Tujuan: {str(e)}")


# ==================== 4. SASARAN & INDIKATOR SASARAN RPJMD (TREE AGGREGATION) ====================

@router.get("/sasaran-lengkap")
def get_rpjmd_sasaran_lengkap(db: Session = Depends(deps.get_db)) -> Any:
    """
    Mengambil data lengkap Tree Sasaran dan Indikator Sasaran RPJMD beserta relasi Tujuan & Misi.
    """
    try:
        sasaran_sql = text("""
            SELECT s.idsasaran, s.kodepemda, s.idperiode, s.idtujuan, s.uraisasaran, s.urut,
                   t.uraitujuan, t.urut as urut_tujuan,
                   m.idmisi, m.urut as urut_misi, m.uraimisi
            FROM rpjmd_sasaran s
            LEFT JOIN rpjmd_tujuan t ON s.idtujuan = t.idtujuan
            LEFT JOIN rpjmd_tujuan_misi tm ON t.idtujuan = tm.idtujuan
            LEFT JOIN rpjmd_misi m ON tm.idmisi = m.idmisi
            ORDER BY s.urut ASC, s.idsasaran ASC;
        """)
        sasaran_rows = db.execute(sasaran_sql).mappings().all()

        indikator_sql = text("""
            SELECT * FROM rpjmd_indikator_sasaran
            ORDER BY urut ASC, idsasaran_indikator ASC;
        """)
        indikator_rows = db.execute(indikator_sql).mappings().all()

        ind_map = {}
        for ind in indikator_rows:
            sid = str(ind['idsasaran'])
            if sid not in ind_map:
                ind_map[sid] = []
            ind_dict = dict(ind)
            if isinstance(ind_dict.get('idsasaran_indikator'), uuid.UUID):
                ind_dict['idsasaran_indikator'] = str(ind_dict['idsasaran_indikator'])
            if isinstance(ind_dict.get('idsasaran'), uuid.UUID):
                ind_dict['idsasaran'] = str(ind_dict['idsasaran'])
            if isinstance(ind_dict.get('aspek'), uuid.UUID):
                ind_dict['aspek'] = str(ind_dict['aspek'])
            ind_map[sid].append(ind_dict)

        result = []
        for s in sasaran_rows:
            s_dict = dict(s)
            sid = str(s_dict['idsasaran'])
            if isinstance(s_dict.get('idsasaran'), uuid.UUID):
                s_dict['idsasaran'] = str(s_dict['idsasaran'])
            if isinstance(s_dict.get('idtujuan'), uuid.UUID):
                s_dict['idtujuan'] = str(s_dict['idtujuan'])
            s_dict['indikator_list'] = ind_map.get(sid, [])
            result.append(s_dict)

        return {
            "status": "success",
            "total_sasaran": len(result),
            "total_indikator": len(indikator_rows),
            "daftar_sasaran": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Sasaran lengkap: {str(e)}")

@router.get("/sasaran")
def get_rpjmd_sasaran_list(db: Session = Depends(deps.get_db)) -> Any:
    """
    Mengambil data list Sasaran RPJMD dari tabel rpjmd_sasaran.
    """
    try:
        sql = text("""
            SELECT s.*, t.uraitujuan, t.urut as urut_tujuan, m.urut as urut_misi, m.uraimisi
            FROM rpjmd_sasaran s
            LEFT JOIN rpjmd_tujuan t ON s.idtujuan = t.idtujuan
            LEFT JOIN rpjmd_tujuan_misi tm ON t.idtujuan = tm.idtujuan
            LEFT JOIN rpjmd_misi m ON tm.idmisi = m.idmisi
            ORDER BY s.urut ASC, s.idsasaran ASC;
        """)
        rows = db.execute(sql).mappings().all()
        result = []
        for r in rows:
            rd = dict(r)
            if isinstance(rd.get('idsasaran'), uuid.UUID):
                rd['idsasaran'] = str(rd['idsasaran'])
            if isinstance(rd.get('idtujuan'), uuid.UUID):
                rd['idtujuan'] = str(rd['idtujuan'])
            result.append(rd)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Sasaran list: {str(e)}")

@router.post("/sasaran")
def create_rpjmd_sasaran(
    sasaran_in: RpjmdSasaranCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menambahkan data Sasaran RPJMD baru ke tabel rpjmd_sasaran.
    """
    try:
        new_id = str(uuid.uuid4())
        sql = text("""
            INSERT INTO rpjmd_sasaran (
                idsasaran, kodepemda, idperiode, idtujuan, uraisasaran, urut, created_at
            ) VALUES (
                :idsasaran, :kodepemda, :idperiode, :idtujuan, :uraisasaran, :urut, NOW()
            ) RETURNING *;
        """)
        row = db.execute(sql, {
            "idsasaran": new_id,
            "kodepemda": sasaran_in.kodepemda or '3376',
            "idperiode": sasaran_in.idperiode or '20252029',
            "idtujuan": sasaran_in.idtujuan or None,
            "uraisasaran": sasaran_in.uraisasaran,
            "urut": sasaran_in.urut or 1
        }).mappings().first()
        db.commit()
        rd = dict(row)
        if isinstance(rd.get('idsasaran'), uuid.UUID):
            rd['idsasaran'] = str(rd['idsasaran'])
        if isinstance(rd.get('idtujuan'), uuid.UUID):
            rd['idtujuan'] = str(rd['idtujuan'])
        return rd
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating RPJMD Sasaran: {str(e)}")

@router.put("/sasaran/{idsasaran}")
def update_rpjmd_sasaran(
    idsasaran: str,
    sasaran_in: RpjmdSasaranUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengupdate data Sasaran RPJMD di tabel rpjmd_sasaran.
    """
    try:
        sql = text("""
            UPDATE rpjmd_sasaran
            SET uraisasaran = :uraisasaran,
                urut = :urut,
                idtujuan = :idtujuan
            WHERE idsasaran = :idsasaran
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idsasaran": idsasaran,
            "uraisasaran": sasaran_in.uraisasaran,
            "urut": sasaran_in.urut or 1,
            "idtujuan": sasaran_in.idtujuan or None
        }).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Sasaran RPJMD tidak ditemukan")
        rd = dict(row)
        if isinstance(rd.get('idsasaran'), uuid.UUID):
            rd['idsasaran'] = str(rd['idsasaran'])
        if isinstance(rd.get('idtujuan'), uuid.UUID):
            rd['idtujuan'] = str(rd['idtujuan'])
        return rd
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating RPJMD Sasaran: {str(e)}")

@router.delete("/sasaran/{idsasaran}")
def delete_rpjmd_sasaran(
    idsasaran: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menghapus data Sasaran RPJMD dan seluruh Indikator Sasaran di bawahnya.
    """
    try:
        db.execute(text("DELETE FROM rpjmd_indikator_sasaran WHERE idsasaran = :idsasaran;"), {"idsasaran": idsasaran})
        sql = text("DELETE FROM rpjmd_sasaran WHERE idsasaran = :idsasaran RETURNING *;")
        row = db.execute(sql, {"idsasaran": idsasaran}).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Sasaran RPJMD tidak ditemukan")
        rd = dict(row)
        if isinstance(rd.get('idsasaran'), uuid.UUID):
            rd['idsasaran'] = str(rd['idsasaran'])
        return {"status": "success", "message": "Sasaran RPJMD berhasil dihapus", "deleted": rd}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting RPJMD Sasaran: {str(e)}")

# --- Indikator Sasaran Endpoints ---

@router.get("/indikator-sasaran")
def get_rpjmd_indikator_sasaran_list(
    idsasaran: Optional[str] = Query(None, description="Filter by idsasaran"),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengambil data Indikator Sasaran RPJMD.
    """
    try:
        if idsasaran:
            sql = text("SELECT * FROM rpjmd_indikator_sasaran WHERE idsasaran = :idsasaran ORDER BY urut ASC, idsasaran_indikator ASC;")
            rows = db.execute(sql, {"idsasaran": idsasaran}).mappings().all()
        else:
            sql = text("SELECT * FROM rpjmd_indikator_sasaran ORDER BY urut ASC, idsasaran_indikator ASC;")
            rows = db.execute(sql).mappings().all()
        result = []
        for r in rows:
            rd = dict(r)
            if isinstance(rd.get('idsasaran_indikator'), uuid.UUID):
                rd['idsasaran_indikator'] = str(rd['idsasaran_indikator'])
            if isinstance(rd.get('idsasaran'), uuid.UUID):
                rd['idsasaran'] = str(rd['idsasaran'])
            if isinstance(rd.get('aspek'), uuid.UUID):
                rd['aspek'] = str(rd['aspek'])
            result.append(rd)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching RPJMD Indikator Sasaran: {str(e)}")

@router.post("/indikator-sasaran")
def create_rpjmd_indikator_sasaran(
    ind_in: RpjmdIndikatorSasaranCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menambahkan data Indikator Sasaran RPJMD baru ke tabel rpjmd_indikator_sasaran.
    """
    try:
        new_id = str(uuid.uuid4())
        sql = text("""
            INSERT INTO rpjmd_indikator_sasaran (
                idsasaran_indikator, kodepemda, idperiode, idsasaran,
                uraisasaran_indikator, satuan, status, baseline,
                target0, target1, target2, target3, target4, target5,
                tipe_data, kodeindikator_master, sumber, iku, ikd,
                uraiaspek, urut, created_at, postdate
            ) VALUES (
                :idsasaran_indikator, :kodepemda, :idperiode, :idsasaran,
                :uraisasaran_indikator, :satuan, :status, :baseline,
                :target0, :target1, :target2, :target3, :target4, :target5,
                :tipe_data, :kodeindikator_master, :sumber, :iku, :ikd,
                :uraiaspek, :urut, NOW(), NOW()
            ) RETURNING *;
        """)
        row = db.execute(sql, {
            "idsasaran_indikator": new_id,
            "kodepemda": ind_in.kodepemda or '3376',
            "idperiode": ind_in.idperiode or '20252029',
            "idsasaran": ind_in.idsasaran,
            "uraisasaran_indikator": ind_in.uraisasaran_indikator,
            "satuan": ind_in.satuan or 'Angka',
            "status": ind_in.status or 'positif',
            "baseline": ind_in.baseline or '',
            "target0": ind_in.target0 or '',
            "target1": ind_in.target1 or '',
            "target2": ind_in.target2 or '',
            "target3": ind_in.target3 or '',
            "target4": ind_in.target4 or '',
            "target5": ind_in.target5 or '',
            "tipe_data": ind_in.tipe_data or 'numeric',
            "kodeindikator_master": ind_in.kodeindikator_master,
            "sumber": ind_in.sumber or 'MASTER',
            "iku": '1' if ind_in.iku else None,
            "ikd": '1' if ind_in.ikd else None,
            "uraiaspek": ind_in.uraiaspek,
            "urut": ind_in.urut or 1
        }).mappings().first()
        db.commit()
        rd = dict(row)
        if isinstance(rd.get('idsasaran_indikator'), uuid.UUID):
            rd['idsasaran_indikator'] = str(rd['idsasaran_indikator'])
        if isinstance(rd.get('idsasaran'), uuid.UUID):
            rd['idsasaran'] = str(rd['idsasaran'])
        return rd
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating RPJMD Indikator Sasaran: {str(e)}")

@router.put("/indikator-sasaran/{idsasaran_indikator}")
def update_rpjmd_indikator_sasaran(
    idsasaran_indikator: str,
    ind_in: RpjmdIndikatorSasaranUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Mengupdate data Indikator Sasaran RPJMD.
    """
    try:
        sql = text("""
            UPDATE rpjmd_indikator_sasaran
            SET uraisasaran_indikator = :uraisasaran_indikator,
                satuan = :satuan,
                status = :status,
                baseline = :baseline,
                target0 = :target0,
                target1 = :target1,
                target2 = :target2,
                target3 = :target3,
                target4 = :target4,
                target5 = :target5,
                tipe_data = :tipe_data,
                kodeindikator_master = :kodeindikator_master,
                sumber = :sumber,
                iku = :iku,
                ikd = :ikd,
                uraiaspek = :uraiaspek,
                urut = :urut,
                lastupdate = NOW()
            WHERE idsasaran_indikator = :idsasaran_indikator
            RETURNING *;
        """)
        row = db.execute(sql, {
            "idsasaran_indikator": idsasaran_indikator,
            "uraisasaran_indikator": ind_in.uraisasaran_indikator,
            "satuan": ind_in.satuan or 'Angka',
            "status": ind_in.status or 'positif',
            "baseline": ind_in.baseline or '',
            "target0": ind_in.target0 or '',
            "target1": ind_in.target1 or '',
            "target2": ind_in.target2 or '',
            "target3": ind_in.target3 or '',
            "target4": ind_in.target4 or '',
            "target5": ind_in.target5 or '',
            "tipe_data": ind_in.tipe_data or 'numeric',
            "kodeindikator_master": ind_in.kodeindikator_master,
            "sumber": ind_in.sumber or 'MASTER',
            "iku": '1' if ind_in.iku else None,
            "ikd": '1' if ind_in.ikd else None,
            "uraiaspek": ind_in.uraiaspek,
            "urut": ind_in.urut or 1
        }).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Indikator Sasaran RPJMD tidak ditemukan")
        rd = dict(row)
        if isinstance(rd.get('idsasaran_indikator'), uuid.UUID):
            rd['idsasaran_indikator'] = str(rd['idsasaran_indikator'])
        if isinstance(rd.get('idsasaran'), uuid.UUID):
            rd['idsasaran'] = str(rd['idsasaran'])
        return rd
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating RPJMD Indikator Sasaran: {str(e)}")

@router.delete("/indikator-sasaran/{idsasaran_indikator}")
def delete_rpjmd_indikator_sasaran(
    idsasaran_indikator: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Menghapus data Indikator Sasaran RPJMD.
    """
    try:
        sql = text("DELETE FROM rpjmd_indikator_sasaran WHERE idsasaran_indikator = :idsasaran_indikator RETURNING *;")
        row = db.execute(sql, {"idsasaran_indikator": idsasaran_indikator}).mappings().first()
        db.commit()
        if not row:
            raise HTTPException(status_code=404, detail="Data Indikator Sasaran RPJMD tidak ditemukan")
        rd = dict(row)
        if isinstance(rd.get('idsasaran_indikator'), uuid.UUID):
            rd['idsasaran_indikator'] = str(rd['idsasaran_indikator'])
        return {"status": "success", "message": "Indikator Sasaran RPJMD berhasil dihapus", "deleted": rd}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting RPJMD Indikator Sasaran: {str(e)}")

