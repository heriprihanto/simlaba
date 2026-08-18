import json
import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter()

# ==================== SCHEMAS ====================

class PenjelasanVisiCreate(BaseModel):
    visi_id: Optional[str] = None
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"
    kodepenjelasan: Optional[str] = None
    pokokvisi: str
    penjelasanvisi: str
    catatan: Optional[list] = []
    no: Optional[int] = 1

class PenjelasanVisiUpdate(BaseModel):
    pokokvisi: Optional[str] = None
    penjelasanvisi: Optional[str] = None
    kodepenjelasan: Optional[str] = None
    catatan: Optional[list] = None
    no: Optional[int] = None

class VisiUpdate(BaseModel):
    uraivisi: Optional[str] = None
    visi_provinsi: Optional[str] = None
    catatan: Optional[str] = None
    status: Optional[int] = None

class SasaranVisiCreate(BaseModel):
    kode: str
    urai: str
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"
    urut: Optional[int] = 1
    no: Optional[int] = 1
    catatan: Optional[list] = []

class SasaranVisiUpdate(BaseModel):
    kode: Optional[str] = None
    urai: Optional[str] = None
    urut: Optional[int] = None
    no: Optional[int] = None
    catatan: Optional[list] = None

class IndikatorSasaranVisiCreate(BaseModel):
    kode_sasaran_visi: str
    kode_indikator: str
    urai_indikator: str
    tag_indikator_sasaran_visi_rpjpn: Optional[list] = []
    catatan_indikator: Optional[list] = []
    kondisi_awal: Optional[str] = None
    baseline: Optional[str] = None
    target_1: Optional[str] = None
    target_2: Optional[str] = None
    target_3: Optional[str] = None
    target_4: Optional[str] = None
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"

class IndikatorSasaranVisiUpdate(BaseModel):
    kode_sasaran_visi: Optional[str] = None
    kode_indikator: Optional[str] = None
    urai_indikator: Optional[str] = None
    tag_indikator_sasaran_visi_rpjpn: Optional[list] = None
    catatan_indikator: Optional[list] = None
    kondisi_awal: Optional[str] = None
    baseline: Optional[str] = None
    target_1: Optional[str] = None
    target_2: Optional[str] = None
    target_3: Optional[str] = None
    target_4: Optional[str] = None

class MisiCreate(BaseModel):
    idmisi: str
    uraimisi: str
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"
    urut: Optional[int] = 1
    no: Optional[int] = 1
    misi_provinsi: Optional[list] = []
    misi_pembangunan: Optional[str] = None
    catatan: Optional[list] = []
    tag_tujuan_rtrw: Optional[list] = []

class MisiUpdate(BaseModel):
    idmisi: Optional[str] = None
    uraimisi: Optional[str] = None
    urut: Optional[int] = None
    no: Optional[int] = None
    misi_provinsi: Optional[list] = None
    misi_pembangunan: Optional[str] = None
    catatan: Optional[list] = None
    tag_tujuan_rtrw: Optional[list] = None

class ArahKebijakanCreate(BaseModel):
    idarahkebijakan: str
    arahkebijakan: str
    idmisi: Optional[str] = None
    idtujuan: Optional[str] = None
    idsasaran: Optional[str] = None
    uraisasaran: Optional[str] = None
    periode_rpjmd_pelaksanaan: Optional[list] = []
    urut: Optional[int] = 1
    no: Optional[int] = 1
    kode: Optional[str] = None
    arah_kebijakan_provinsi: Optional[list] = []
    arah_kebijakan_rpjpn: Optional[list] = []
    catatan: Optional[list] = []
    strategi_rtrw: Optional[str] = None
    kebijakan_rtrw: Optional[str] = None
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"

class ArahKebijakanUpdate(BaseModel):
    idarahkebijakan: Optional[str] = None
    arahkebijakan: Optional[str] = None
    idmisi: Optional[str] = None
    idtujuan: Optional[str] = None
    idsasaran: Optional[str] = None
    uraisasaran: Optional[str] = None
    periode_rpjmd_pelaksanaan: Optional[list] = None
    urut: Optional[int] = None
    no: Optional[int] = None
    kode: Optional[str] = None
    arah_kebijakan_provinsi: Optional[list] = None
    arah_kebijakan_rpjpn: Optional[list] = None
    catatan: Optional[list] = None
    strategi_rtrw: Optional[str] = None
    kebijakan_rtrw: Optional[str] = None

class SasaranPokokCreate(BaseModel):
    idsasaran: str
    uraisasaran: str
    idmisi: Optional[str] = "1"
    uraimisi: Optional[str] = None
    urut: Optional[int] = 1
    no: Optional[int] = 1
    arah_pembangunan: Optional[list] = []
    catatan: Optional[list] = []
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"

class SasaranPokokUpdate(BaseModel):
    idsasaran: Optional[str] = None
    uraisasaran: Optional[str] = None
    idmisi: Optional[str] = None
    uraimisi: Optional[str] = None
    urut: Optional[int] = None
    no: Optional[int] = None
    arah_pembangunan: Optional[list] = None
    catatan: Optional[list] = None

class IndikatorSasaranPokokCreate(BaseModel):
    idsasaran: str
    idsasaran_indikator: str
    uraisasaran_indikator: str
    idmisi: Optional[str] = "1"
    idtujuan: Optional[str] = "0"
    satuan: Optional[str] = "%"
    status: Optional[str] = "positif"
    kondisi_awal: Optional[str] = None
    baseline: Optional[str] = None
    target_1: Optional[str] = None
    target_2: Optional[str] = None
    target_3: Optional[str] = None
    target_4: Optional[str] = None
    kodeindikator_master: Optional[str] = None
    indikator_utama_pembangunan: Optional[list] = []
    sasaran_pokok_provinsi: Optional[list] = []
    indikator_sasaran_pokok_provinsi: Optional[list] = []
    tag_indikator_daerah: Optional[list] = []
    catatan: Optional[list] = []
    tipe_data: Optional[str] = "numeric"
    urut: Optional[int] = 1
    kodepemda: Optional[str] = "3376"
    idperiode: Optional[str] = "20252045"

class IndikatorSasaranPokokUpdate(BaseModel):
    idsasaran: Optional[str] = None
    idsasaran_indikator: Optional[str] = None
    uraisasaran_indikator: Optional[str] = None
    idmisi: Optional[str] = None
    idtujuan: Optional[str] = None
    satuan: Optional[str] = None
    status: Optional[str] = None
    kondisi_awal: Optional[str] = None
    baseline: Optional[str] = None
    target_1: Optional[str] = None
    target_2: Optional[str] = None
    target_3: Optional[str] = None
    target_4: Optional[str] = None
    kodeindikator_master: Optional[str] = None
    indikator_utama_pembangunan: Optional[list] = None
    sasaran_pokok_provinsi: Optional[list] = None
    indikator_sasaran_pokok_provinsi: Optional[list] = None
    tag_indikator_daerah: Optional[list] = None
    catatan: Optional[list] = None
    tipe_data: Optional[str] = None
    urut: Optional[int] = None


# ==================== 1. VISI & PENJELASAN VISI ENDPOINTS ====================

@router.get("/visi")
def get_rpjpd_visi(db: Session = Depends(get_db)):
    """Mengambil data Visi RPJPD dari tabel rpjpd_visi"""
    sql = text("""
        SELECT 
            id::text, 
            idperiode, 
            status, 
            check_value, 
            uraivisi, 
            visi_provinsi, 
            catatan, 
            kodepemda, 
            no, 
            created_at
        FROM public.rpjpd_visi
        ORDER BY no ASC, created_at ASC
    """)
    result = db.execute(sql).mappings().all()
    return [dict(r) for r in result]


@router.get("/penjelasan-visi")
def get_rpjpd_penjelasan_visi(visi_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Mengambil data Penjelasan Visi RPJPD dari tabel rpjpd_penjelasan_visi"""
    if visi_id:
        sql = text("""
            SELECT 
                id::text, 
                visi_id::text, 
                kodepemda, 
                idperiode, 
                kodepenjelasan, 
                pokokvisi, 
                penjelasanvisi, 
                catatan, 
                no, 
                created_at
            FROM public.rpjpd_penjelasan_visi
            WHERE visi_id = :visi_id
            ORDER BY no ASC, created_at ASC
        """)
        result = db.execute(sql, {"visi_id": visi_id}).mappings().all()
    else:
        sql = text("""
            SELECT 
                id::text, 
                visi_id::text, 
                kodepemda, 
                idperiode, 
                kodepenjelasan, 
                pokokvisi, 
                penjelasanvisi, 
                catatan, 
                no, 
                created_at
            FROM public.rpjpd_penjelasan_visi
            ORDER BY no ASC, created_at ASC
        """)
        result = db.execute(sql).mappings().all()
    
    return [dict(r) for r in result]


@router.get("/visi-lengkap")
def get_rpjpd_visi_lengkap(db: Session = Depends(get_db)):
    """Mengambil data Visi RPJPD beserta seluruh daftar Penjelasan Visi terkait"""
    visi_sql = text("""
        SELECT 
            id::text, 
            idperiode, 
            status, 
            check_value, 
            uraivisi, 
            visi_provinsi, 
            catatan, 
            kodepemda, 
            no, 
            created_at
        FROM public.rpjpd_visi
        ORDER BY no ASC, created_at ASC
    """)
    visi_list = [dict(r) for r in db.execute(visi_sql).mappings().all()]
    
    penjelasan_sql = text("""
        SELECT 
            id::text, 
            visi_id::text, 
            kodepemda, 
            idperiode, 
            kodepenjelasan, 
            pokokvisi, 
            penjelasanvisi, 
            catatan, 
            no, 
            created_at
        FROM public.rpjpd_penjelasan_visi
        ORDER BY no ASC, created_at ASC
    """)
    penjelasan_list = [dict(r) for r in db.execute(penjelasan_sql).mappings().all()]
    
    penjelasan_by_visi = {}
    for p in penjelasan_list:
        v_id = p.get("visi_id")
        if v_id not in penjelasan_by_visi:
            penjelasan_by_visi[v_id] = []
        penjelasan_by_visi[v_id].append(p)
        
    for v in visi_list:
        v["penjelasan_list"] = penjelasan_by_visi.get(v["id"], [])
        
    return {
        "visi_utama": visi_list[0] if visi_list else None,
        "daftar_visi": visi_list,
        "daftar_penjelasan": penjelasan_list
    }


@router.put("/visi/{visi_id}")
def update_rpjpd_visi(visi_id: str, payload: VisiUpdate, db: Session = Depends(get_db)):
    """Memperbarui uraian visi RPJPD"""
    fields = []
    params = {"visi_id": visi_id}
    
    if payload.uraivisi is not None:
        fields.append("uraivisi = :uraivisi")
        params["uraivisi"] = payload.uraivisi
    if payload.visi_provinsi is not None:
        fields.append("visi_provinsi = :visi_provinsi")
        params["visi_provinsi"] = payload.visi_provinsi
    if payload.catatan is not None:
        fields.append("catatan = :catatan")
        params["catatan"] = payload.catatan
    if payload.status is not None:
        fields.append("status = :status")
        params["status"] = payload.status
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_visi SET {', '.join(fields)} WHERE id = :visi_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Visi RPJPD tidak ditemukan")
        
    return {"message": "Data Visi berhasil diperbarui", "id": res}


@router.post("/penjelasan-visi", status_code=status.HTTP_201_CREATED)
def create_rpjpd_penjelasan_visi(payload: PenjelasanVisiCreate, db: Session = Depends(get_db)):
    """Menambahkan data Penjelasan Visi baru ke tabel rpjpd_penjelasan_visi"""
    new_id = str(uuid.uuid4())
    
    if not payload.visi_id:
        first_visi = db.execute(text("SELECT id::text FROM public.rpjpd_visi LIMIT 1")).scalar()
        if not first_visi:
            raise HTTPException(status_code=400, detail="Visi induk RPJPD belum tersedia")
        visi_id = first_visi
    else:
        visi_id = payload.visi_id

    sql = text("""
        INSERT INTO public.rpjpd_penjelasan_visi (
            id, visi_id, kodepemda, idperiode, kodepenjelasan, pokokvisi, penjelasanvisi, catatan, no, created_at
        ) VALUES (
            :id, :visi_id, :kodepemda, :idperiode, :kodepenjelasan, :pokokvisi, :penjelasanvisi, :catatan::jsonb, :no, NOW()
        )
        RETURNING id::text
    """)
    
    res = db.execute(sql, {
        "id": new_id,
        "visi_id": visi_id,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode,
        "kodepenjelasan": payload.kodepenjelasan or str(uuid.uuid4())[:8],
        "pokokvisi": payload.pokokvisi,
        "penjelasanvisi": payload.penjelasanvisi,
        "catatan": json.dumps(payload.catatan or []),
        "no": payload.no
    }).scalar()
    db.commit()
    
    return {"message": "Penjelasan Visi berhasil ditambahkan", "id": res}


@router.put("/penjelasan-visi/{penjelasan_id}")
def update_rpjpd_penjelasan_visi(penjelasan_id: str, payload: PenjelasanVisiUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Penjelasan Visi di tabel rpjpd_penjelasan_visi"""
    fields = []
    params = {"penjelasan_id": penjelasan_id}
    
    if payload.pokokvisi is not None:
        fields.append("pokokvisi = :pokokvisi")
        params["pokokvisi"] = payload.pokokvisi
    if payload.penjelasanvisi is not None:
        fields.append("penjelasanvisi = :penjelasanvisi")
        params["penjelasanvisi"] = payload.penjelasanvisi
    if payload.kodepenjelasan is not None:
        fields.append("kodepenjelasan = :kodepenjelasan")
        params["kodepenjelasan"] = payload.kodepenjelasan
    if payload.catatan is not None:
        fields.append("catatan = :catatan::jsonb")
        params["catatan"] = json.dumps(payload.catatan)
    if payload.no is not None:
        fields.append("no = :no")
        params["no"] = payload.no
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_penjelasan_visi SET {', '.join(fields)} WHERE id = :penjelasan_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Penjelasan Visi tidak ditemukan")
        
    return {"message": "Penjelasan Visi berhasil diperbarui", "id": res}


@router.delete("/penjelasan-visi/{penjelasan_id}")
def delete_rpjpd_penjelasan_visi(penjelasan_id: str, db: Session = Depends(get_db)):
    """Menghapus data Penjelasan Visi dari tabel rpjpd_penjelasan_visi"""
    sql = text("DELETE FROM public.rpjpd_penjelasan_visi WHERE id = :penjelasan_id RETURNING id::text")
    res = db.execute(sql, {"penjelasan_id": penjelasan_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Penjelasan Visi tidak ditemukan")
        
    return {"message": "Penjelasan Visi berhasil dihapus", "id": res}


# ==================== 2. SASARAN VISI & INDIKATOR SASARAN VISI ENDPOINTS ====================

@router.get("/sasaran-visi")
def get_rpjpd_sasaran_visi(db: Session = Depends(get_db)):
    """Mengambil daftar Sasaran Visi RPJPD dari tabel rpjpd_sasaran_visi"""
    sql = text("""
        SELECT 
            id::text, 
            kodepemda, 
            idperiode, 
            kode, 
            urai, 
            catatan, 
            urut, 
            no, 
            created_at
        FROM public.rpjpd_sasaran_visi
        ORDER BY urut ASC, no ASC, kode ASC
    """)
    result = db.execute(sql).mappings().all()
    return [dict(r) for r in result]


@router.get("/indikator-sasaran-visi")
def get_rpjpd_indikator_sasaran_visi(kode_sasaran_visi: Optional[str] = None, db: Session = Depends(get_db)):
    """Mengambil daftar Indikator Sasaran Visi dari tabel rpjpd_indikator_sasaran_visi"""
    if kode_sasaran_visi:
        sql = text("""
            SELECT 
                id::text, 
                kode_sasaran_visi, 
                kode_indikator, 
                urai_indikator, 
                tag_indikator_sasaran_visi_rpjpn, 
                catatan_indikator, 
                kondisi_awal, 
                baseline, 
                target_1, 
                target_2, 
                target_3, 
                target_4, 
                kodepemda, 
                idperiode, 
                created_at
            FROM public.rpjpd_indikator_sasaran_visi
            WHERE kode_sasaran_visi = :kode_sasaran_visi
            ORDER BY kode_indikator ASC, created_at ASC
        """)
        result = db.execute(sql, {"kode_sasaran_visi": kode_sasaran_visi}).mappings().all()
    else:
        sql = text("""
            SELECT 
                id::text, 
                kode_sasaran_visi, 
                kode_indikator, 
                urai_indikator, 
                tag_indikator_sasaran_visi_rpjpn, 
                catatan_indikator, 
                kondisi_awal, 
                baseline, 
                target_1, 
                target_2, 
                target_3, 
                target_4, 
                kodepemda, 
                idperiode, 
                created_at
            FROM public.rpjpd_indikator_sasaran_visi
            ORDER BY kode_sasaran_visi ASC, kode_indikator ASC, created_at ASC
        """)
        result = db.execute(sql).mappings().all()
        
    return [dict(r) for r in result]


@router.get("/sasaran-visi-lengkap")
def get_rpjpd_sasaran_visi_lengkap(db: Session = Depends(get_db)):
    """Mengambil seluruh data Sasaran Visi berserta Indikator Sasaran Visi terkait secara bersarang"""
    sasaran_sql = text("""
        SELECT 
            id::text, 
            kodepemda, 
            idperiode, 
            kode, 
            urai, 
            catatan, 
            urut, 
            no, 
            created_at
        FROM public.rpjpd_sasaran_visi
        ORDER BY urut ASC, no ASC, kode ASC
    """)
    sasaran_list = [dict(r) for r in db.execute(sasaran_sql).mappings().all()]
    
    indikator_sql = text("""
        SELECT 
            id::text, 
            kode_sasaran_visi, 
            kode_indikator, 
            urai_indikator, 
            tag_indikator_sasaran_visi_rpjpn, 
            catatan_indikator, 
            kondisi_awal, 
            baseline, 
            target_1, 
            target_2, 
            target_3, 
            target_4, 
            kodepemda, 
            idperiode, 
            created_at
        FROM public.rpjpd_indikator_sasaran_visi
        ORDER BY kode_sasaran_visi ASC, kode_indikator ASC, created_at ASC
    """)
    indikator_list = [dict(r) for r in db.execute(indikator_sql).mappings().all()]
    
    # Kelompokkan indikator berdasarkan kode_sasaran_visi
    indikator_by_sasaran = {}
    for ind in indikator_list:
        k_sv = ind.get("kode_sasaran_visi")
        if k_sv not in indikator_by_sasaran:
            indikator_by_sasaran[k_sv] = []
        indikator_by_sasaran[k_sv].append(ind)
        
    for s in sasaran_list:
        s["indikator_list"] = indikator_by_sasaran.get(s["kode"], [])
        s["jumlah_indikator"] = len(s["indikator_list"])
        
    return {
        "total_sasaran_visi": len(sasaran_list),
        "total_indikator": len(indikator_list),
        "daftar_sasaran_visi": sasaran_list,
        "daftar_semua_indikator": indikator_list
    }


@router.post("/sasaran-visi", status_code=status.HTTP_201_CREATED)
def create_rpjpd_sasaran_visi(payload: SasaranVisiCreate, db: Session = Depends(get_db)):
    """Menambahkan data Sasaran Visi baru ke tabel rpjpd_sasaran_visi"""
    new_id = str(uuid.uuid4())
    sql = text("""
        INSERT INTO public.rpjpd_sasaran_visi (
            id, kodepemda, idperiode, kode, urai, catatan, urut, no, created_at
        ) VALUES (
            :id, :kodepemda, :idperiode, :kode, :urai, :catatan::jsonb, :urut, :no, NOW()
        )
        RETURNING id::text
    """)
    res = db.execute(sql, {
        "id": new_id,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode,
        "kode": payload.kode,
        "urai": payload.urai,
        "catatan": json.dumps(payload.catatan or []),
        "urut": payload.urut,
        "no": payload.no
    }).scalar()
    db.commit()
    return {"message": "Sasaran Visi berhasil ditambahkan", "id": res}


@router.put("/sasaran-visi/{sasaran_id}")
def update_rpjpd_sasaran_visi(sasaran_id: str, payload: SasaranVisiUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Sasaran Visi di tabel rpjpd_sasaran_visi"""
    fields = []
    params = {"sasaran_id": sasaran_id}
    
    if payload.kode is not None:
        fields.append("kode = :kode")
        params["kode"] = payload.kode
    if payload.urai is not None:
        fields.append("urai = :urai")
        params["urai"] = payload.urai
    if payload.urut is not None:
        fields.append("urut = :urut")
        params["urut"] = payload.urut
    if payload.no is not None:
        fields.append("no = :no")
        params["no"] = payload.no
    if payload.catatan is not None:
        fields.append("catatan = :catatan::jsonb")
        params["catatan"] = json.dumps(payload.catatan)
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_sasaran_visi SET {', '.join(fields)} WHERE id = :sasaran_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Sasaran Visi tidak ditemukan")
        
    return {"message": "Sasaran Visi berhasil diperbarui", "id": res}


@router.delete("/sasaran-visi/{sasaran_id}")
def delete_rpjpd_sasaran_visi(sasaran_id: str, db: Session = Depends(get_db)):
    """Menghapus data Sasaran Visi dari tabel rpjpd_sasaran_visi"""
    sql = text("DELETE FROM public.rpjpd_sasaran_visi WHERE id = :sasaran_id RETURNING id::text")
    res = db.execute(sql, {"sasaran_id": sasaran_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Sasaran Visi tidak ditemukan")
        
    return {"message": "Sasaran Visi berhasil dihapus", "id": res}


@router.post("/indikator-sasaran-visi", status_code=status.HTTP_201_CREATED)
def create_rpjpd_indikator_sasaran_visi(payload: IndikatorSasaranVisiCreate, db: Session = Depends(get_db)):
    """Menambahkan data Indikator Sasaran Visi ke tabel rpjpd_indikator_sasaran_visi"""
    new_id = str(uuid.uuid4())
    sql = text("""
        INSERT INTO public.rpjpd_indikator_sasaran_visi (
            id, kode_sasaran_visi, kode_indikator, urai_indikator, 
            tag_indikator_sasaran_visi_rpjpn, catatan_indikator, 
            kondisi_awal, baseline, target_1, target_2, target_3, target_4, 
            kodepemda, idperiode, created_at
        ) VALUES (
            :id, :kode_sasaran_visi, :kode_indikator, :urai_indikator, 
            :tag_indikator_sasaran_visi_rpjpn::jsonb, :catatan_indikator::jsonb, 
            :kondisi_awal, :baseline, :target_1, :target_2, :target_3, :target_4, 
            :kodepemda, :idperiode, NOW()
        )
        RETURNING id::text
    """)
    res = db.execute(sql, {
        "id": new_id,
        "kode_sasaran_visi": payload.kode_sasaran_visi,
        "kode_indikator": payload.kode_indikator,
        "urai_indikator": payload.urai_indikator,
        "tag_indikator_sasaran_visi_rpjpn": json.dumps(payload.tag_indikator_sasaran_visi_rpjpn or []),
        "catatan_indikator": json.dumps(payload.catatan_indikator or []),
        "kondisi_awal": payload.kondisi_awal,
        "baseline": payload.baseline,
        "target_1": payload.target_1,
        "target_2": payload.target_2,
        "target_3": payload.target_3,
        "target_4": payload.target_4,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode
    }).scalar()
    db.commit()
    return {"message": "Indikator Sasaran Visi berhasil ditambahkan", "id": res}


@router.put("/indikator-sasaran-visi/{indikator_id}")
def update_rpjpd_indikator_sasaran_visi(indikator_id: str, payload: IndikatorSasaranVisiUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Indikator Sasaran Visi di tabel rpjpd_indikator_sasaran_visi"""
    fields = []
    params = {"indikator_id": indikator_id}
    
    if payload.kode_sasaran_visi is not None:
        fields.append("kode_sasaran_visi = :kode_sasaran_visi")
        params["kode_sasaran_visi"] = payload.kode_sasaran_visi
    if payload.kode_indikator is not None:
        fields.append("kode_indikator = :kode_indikator")
        params["kode_indikator"] = payload.kode_indikator
    if payload.urai_indikator is not None:
        fields.append("urai_indikator = :urai_indikator")
        params["urai_indikator"] = payload.urai_indikator
    if payload.tag_indikator_sasaran_visi_rpjpn is not None:
        fields.append("tag_indikator_sasaran_visi_rpjpn = :tag_indikator_sasaran_visi_rpjpn::jsonb")
        params["tag_indikator_sasaran_visi_rpjpn"] = json.dumps(payload.tag_indikator_sasaran_visi_rpjpn)
    if payload.catatan_indikator is not None:
        fields.append("catatan_indikator = :catatan_indikator::jsonb")
        params["catatan_indikator"] = json.dumps(payload.catatan_indikator)
    if payload.kondisi_awal is not None:
        fields.append("kondisi_awal = :kondisi_awal")
        params["kondisi_awal"] = payload.kondisi_awal
    if payload.baseline is not None:
        fields.append("baseline = :baseline")
        params["baseline"] = payload.baseline
    if payload.target_1 is not None:
        fields.append("target_1 = :target_1")
        params["target_1"] = payload.target_1
    if payload.target_2 is not None:
        fields.append("target_2 = :target_2")
        params["target_2"] = payload.target_2
    if payload.target_3 is not None:
        fields.append("target_3 = :target_3")
        params["target_3"] = payload.target_3
    if payload.target_4 is not None:
        fields.append("target_4 = :target_4")
        params["target_4"] = payload.target_4
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_indikator_sasaran_visi SET {', '.join(fields)} WHERE id = :indikator_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Indikator Sasaran Visi tidak ditemukan")
        
    return {"message": "Indikator Sasaran Visi berhasil diperbarui", "id": res}


@router.delete("/indikator-sasaran-visi/{indikator_id}")
def delete_rpjpd_indikator_sasaran_visi(indikator_id: str, db: Session = Depends(get_db)):
    """Menghapus data Indikator Sasaran Visi dari tabel rpjpd_indikator_sasaran_visi"""
    sql = text("DELETE FROM public.rpjpd_indikator_sasaran_visi WHERE id = :indikator_id RETURNING id::text")
    res = db.execute(sql, {"indikator_id": indikator_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Indikator Sasaran Visi tidak ditemukan")
        
    return {"message": "Indikator Sasaran Visi berhasil dihapus", "id": res}


# ==================== 3. MISI ENDPOINTS (Tabel: rpjpd_misi) ====================

@router.get("/misi")
def get_rpjpd_misi(db: Session = Depends(get_db)):
    """Mengambil daftar Misi RPJPD dari tabel rpjpd_misi"""
    sql = text("""
        SELECT 
            id::text, 
            idmisi, 
            uraimisi, 
            kodepemda, 
            idperiode, 
            postdate, 
            urut, 
            misi_provinsi, 
            misi_pembangunan, 
            catatan, 
            tag_tujuan_rtrw, 
            no, 
            created_at
        FROM public.rpjpd_misi
        ORDER BY urut ASC, no ASC, idmisi ASC
    """)
    result = db.execute(sql).mappings().all()
    return [dict(r) for r in result]


@router.post("/misi", status_code=status.HTTP_201_CREATED)
def create_rpjpd_misi(payload: MisiCreate, db: Session = Depends(get_db)):
    """Menambahkan data Misi RPJPD baru ke tabel rpjpd_misi"""
    new_id = str(uuid.uuid4())
    sql = text("""
        INSERT INTO public.rpjpd_misi (
            id, idmisi, uraimisi, kodepemda, idperiode, postdate, urut, 
            misi_provinsi, misi_pembangunan, catatan, tag_tujuan_rtrw, no, created_at
        ) VALUES (
            :id, :idmisi, :uraimisi, :kodepemda, :idperiode, NOW(), :urut, 
            :misi_provinsi::jsonb, :misi_pembangunan, :catatan::jsonb, :tag_tujuan_rtrw::jsonb, :no, NOW()
        )
        RETURNING id::text
    """)
    res = db.execute(sql, {
        "id": new_id,
        "idmisi": payload.idmisi,
        "uraimisi": payload.uraimisi,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode,
        "urut": payload.urut,
        "misi_provinsi": json.dumps(payload.misi_provinsi or []),
        "misi_pembangunan": payload.misi_pembangunan,
        "catatan": json.dumps(payload.catatan or []),
        "tag_tujuan_rtrw": json.dumps(payload.tag_tujuan_rtrw or []),
        "no": payload.no
    }).scalar()
    db.commit()
    return {"message": "Misi RPJPD berhasil ditambahkan", "id": res}


@router.put("/misi/{misi_id}")
def update_rpjpd_misi(misi_id: str, payload: MisiUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Misi RPJPD di tabel rpjpd_misi"""
    fields = []
    params = {"misi_id": misi_id}
    
    if payload.idmisi is not None:
        fields.append("idmisi = :idmisi")
        params["idmisi"] = payload.idmisi
    if payload.uraimisi is not None:
        fields.append("uraimisi = :uraimisi")
        params["uraimisi"] = payload.uraimisi
    if payload.urut is not None:
        fields.append("urut = :urut")
        params["urut"] = payload.urut
    if payload.no is not None:
        fields.append("no = :no")
        params["no"] = payload.no
    if payload.misi_provinsi is not None:
        fields.append("misi_provinsi = :misi_provinsi::jsonb")
        params["misi_provinsi"] = json.dumps(payload.misi_provinsi)
    if payload.misi_pembangunan is not None:
        fields.append("misi_pembangunan = :misi_pembangunan")
        params["misi_pembangunan"] = payload.misi_pembangunan
    if payload.catatan is not None:
        fields.append("catatan = :catatan::jsonb")
        params["catatan"] = json.dumps(payload.catatan)
    if payload.tag_tujuan_rtrw is not None:
        fields.append("tag_tujuan_rtrw = :tag_tujuan_rtrw::jsonb")
        params["tag_tujuan_rtrw"] = json.dumps(payload.tag_tujuan_rtrw)
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_misi SET {', '.join(fields)} WHERE id = :misi_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Misi RPJPD tidak ditemukan")
        
    return {"message": "Misi RPJPD berhasil diperbarui", "id": res}


@router.delete("/misi/{misi_id}")
def delete_rpjpd_misi(misi_id: str, db: Session = Depends(get_db)):
    """Menghapus data Misi RPJPD dari tabel rpjpd_misi"""
    sql = text("DELETE FROM public.rpjpd_misi WHERE id = :misi_id RETURNING id::text")
    res = db.execute(sql, {"misi_id": misi_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Misi RPJPD tidak ditemukan")
        
    return {"message": "Misi RPJPD berhasil dihapus", "id": res}


# ==================== 4. ARAH KEBIJAKAN ENDPOINTS (Tabel: rpjpd_arah_kebijakan) ====================

@router.get("/arah-kebijakan")
def get_rpjpd_arah_kebijakan(idmisi: Optional[str] = None, db: Session = Depends(get_db)):
    """Mengambil daftar Arah Kebijakan RPJPD dari tabel rpjpd_arah_kebijakan"""
    query = """
        SELECT 
            id::text, 
            kodepemda, 
            idperiode, 
            idarahkebijakan, 
            arahkebijakan, 
            parent, 
            postdate, 
            lastupdate, 
            creator, 
            updater, 
            tris_no, 
            info, 
            periode_rpjmd_pelaksanaan, 
            idmisi, 
            idtujuan, 
            idsasaran, 
            urut, 
            arah_kebijakan_provinsi, 
            provinsi, 
            arah_kebijakan_rpjpn, 
            catatan, 
            strategi_rtrw, 
            kebijakan_rtrw, 
            kode, 
            uraisasaran, 
            no, 
            created_at
        FROM public.rpjpd_arah_kebijakan
    """
    params = {}
    if idmisi:
        query += " WHERE idmisi = :idmisi"
        params["idmisi"] = idmisi
        
    query += " ORDER BY urut ASC, no ASC, idarahkebijakan ASC"
    
    result = db.execute(text(query), params).mappings().all()
    return [dict(r) for r in result]


@router.post("/arah-kebijakan", status_code=status.HTTP_201_CREATED)
def create_rpjpd_arah_kebijakan(payload: ArahKebijakanCreate, db: Session = Depends(get_db)):
    """Menambahkan data Arah Kebijakan RPJPD baru ke tabel rpjpd_arah_kebijakan"""
    new_id = str(uuid.uuid4())
    kode = payload.kode or f"{payload.kodepemda}#{payload.idperiode}#{payload.idmisi or '1'}#{payload.idtujuan or '1'}#{payload.idsasaran or '1'}"
    
    sql = text("""
        INSERT INTO public.rpjpd_arah_kebijakan (
            id, kodepemda, idperiode, idarahkebijakan, arahkebijakan,
            idmisi, idtujuan, idsasaran, uraisasaran, periode_rpjmd_pelaksanaan,
            urut, no, kode, arah_kebijakan_provinsi, arah_kebijakan_rpjpn,
            catatan, strategi_rtrw, kebijakan_rtrw, postdate, lastupdate, created_at
        ) VALUES (
            :id, :kodepemda, :idperiode, :idarahkebijakan, :arahkebijakan,
            :idmisi, :idtujuan, :idsasaran, :uraisasaran, :periode_rpjmd_pelaksanaan::jsonb,
            :urut, :no, :kode, :arah_kebijakan_provinsi::jsonb, :arah_kebijakan_rpjpn::jsonb,
            :catatan::jsonb, :strategi_rtrw, :kebijakan_rtrw, NOW(), NOW(), NOW()
        )
        RETURNING id::text
    """)
    res = db.execute(sql, {
        "id": new_id,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode,
        "idarahkebijakan": payload.idarahkebijakan,
        "arahkebijakan": payload.arahkebijakan,
        "idmisi": payload.idmisi,
        "idtujuan": payload.idtujuan,
        "idsasaran": payload.idsasaran,
        "uraisasaran": payload.uraisasaran,
        "periode_rpjmd_pelaksanaan": json.dumps(payload.periode_rpjmd_pelaksanaan or []),
        "urut": payload.urut,
        "no": payload.no,
        "kode": kode,
        "arah_kebijakan_provinsi": json.dumps(payload.arah_kebijakan_provinsi or []),
        "arah_kebijakan_rpjpn": json.dumps(payload.arah_kebijakan_rpjpn or []),
        "catatan": json.dumps(payload.catatan or []),
        "strategi_rtrw": payload.strategi_rtrw,
        "kebijakan_rtrw": payload.kebijakan_rtrw
    }).scalar()
    db.commit()
    return {"message": "Arah Kebijakan berhasil ditambahkan", "id": res}


@router.put("/arah-kebijakan/{arah_id}")
def update_rpjpd_arah_kebijakan(arah_id: str, payload: ArahKebijakanUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Arah Kebijakan RPJPD di tabel rpjpd_arah_kebijakan"""
    fields = ["lastupdate = NOW()"]
    params = {"arah_id": arah_id}
    
    if payload.idarahkebijakan is not None:
        fields.append("idarahkebijakan = :idarahkebijakan")
        params["idarahkebijakan"] = payload.idarahkebijakan
    if payload.arahkebijakan is not None:
        fields.append("arahkebijakan = :arahkebijakan")
        params["arahkebijakan"] = payload.arahkebijakan
    if payload.idmisi is not None:
        fields.append("idmisi = :idmisi")
        params["idmisi"] = payload.idmisi
    if payload.idtujuan is not None:
        fields.append("idtujuan = :idtujuan")
        params["idtujuan"] = payload.idtujuan
    if payload.idsasaran is not None:
        fields.append("idsasaran = :idsasaran")
        params["idsasaran"] = payload.idsasaran
    if payload.uraisasaran is not None:
        fields.append("uraisasaran = :uraisasaran")
        params["uraisasaran"] = payload.uraisasaran
    if payload.periode_rpjmd_pelaksanaan is not None:
        fields.append("periode_rpjmd_pelaksanaan = :periode_rpjmd_pelaksanaan::jsonb")
        params["periode_rpjmd_pelaksanaan"] = json.dumps(payload.periode_rpjmd_pelaksanaan)
    if payload.urut is not None:
        fields.append("urut = :urut")
        params["urut"] = payload.urut
    if payload.no is not None:
        fields.append("no = :no")
        params["no"] = payload.no
    if payload.kode is not None:
        fields.append("kode = :kode")
        params["kode"] = payload.kode
    if payload.arah_kebijakan_provinsi is not None:
        fields.append("arah_kebijakan_provinsi = :arah_kebijakan_provinsi::jsonb")
        params["arah_kebijakan_provinsi"] = json.dumps(payload.arah_kebijakan_provinsi)
    if payload.arah_kebijakan_rpjpn is not None:
        fields.append("arah_kebijakan_rpjpn = :arah_kebijakan_rpjpn::jsonb")
        params["arah_kebijakan_rpjpn"] = json.dumps(payload.arah_kebijakan_rpjpn)
    if payload.catatan is not None:
        fields.append("catatan = :catatan::jsonb")
        params["catatan"] = json.dumps(payload.catatan)
    if payload.strategi_rtrw is not None:
        fields.append("strategi_rtrw = :strategi_rtrw")
        params["strategi_rtrw"] = payload.strategi_rtrw
    if payload.kebijakan_rtrw is not None:
        fields.append("kebijakan_rtrw = :kebijakan_rtrw")
        params["kebijakan_rtrw"] = payload.kebijakan_rtrw
        
    sql = text(f"UPDATE public.rpjpd_arah_kebijakan SET {', '.join(fields)} WHERE id = :arah_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Arah Kebijakan tidak ditemukan")
        
    return {"message": "Arah Kebijakan berhasil diperbarui", "id": res}


@router.delete("/arah-kebijakan/{arah_id}")
def delete_rpjpd_arah_kebijakan(arah_id: str, db: Session = Depends(get_db)):
    """Menghapus data Arah Kebijakan RPJPD dari tabel rpjpd_arah_kebijakan"""
    sql = text("DELETE FROM public.rpjpd_arah_kebijakan WHERE id = :arah_id RETURNING id::text")
    res = db.execute(sql, {"arah_id": arah_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Arah Kebijakan tidak ditemukan")
        
    return {"message": "Arah Kebijakan berhasil dihapus", "id": res}


# ==================== 5. SASARAN POKOK & INDIKATOR ENDPOINTS (Tabel: rpjpd_sasaran_pokok & rpjpd_indikator_sasaran_pokok) ====================

@router.get("/sasaran-pokok-lengkap")
def get_rpjpd_sasaran_pokok_lengkap(db: Session = Depends(get_db)):
    """Mengambil struktur Tree lengkap Sasaran Pokok beserta Indikatornya"""
    # 1. Ambil Sasaran Pokok
    sp_sql = text("""
        SELECT 
            id::text, kodepemda, idperiode, urut, idsasaran, uraisasaran,
            idmisi, uraimisi, arah_pembangunan, catatan, no, created_at
        FROM public.rpjpd_sasaran_pokok
        ORDER BY urut ASC, no ASC, idsasaran ASC
    """)
    sp_list = [dict(r) for r in db.execute(sp_sql).mappings().all()]
    
    # 2. Ambil Indikator Sasaran Pokok
    ind_sql = text("""
        SELECT 
            id::text, idsasaran, idmisi, idtujuan, idsasaran_indikator,
            uraisasaran_indikator, satuan, status, kondisi_awal, baseline,
            target_1, target_2, target_3, target_4, kodeindikator_master,
            indikator_utama_pembangunan, sasaran_pokok_provinsi,
            indikator_sasaran_pokok_provinsi, tag_indikator_daerah, catatan,
            tipe_data, kodepemda, idperiode, urut, created_at
        FROM public.rpjpd_indikator_sasaran_pokok
        ORDER BY urut ASC, idsasaran_indikator ASC
    """)
    ind_list = [dict(r) for r in db.execute(ind_sql).mappings().all()]
    
    # Kelompokkan indikator ke dalam sasaran pokok terkait berdasarkan idsasaran
    for sp in sp_list:
        sp_id = str(sp.get("idsasaran") or "").strip()
        sp["indikator_list"] = [
            ind for ind in ind_list if str(ind.get("idsasaran") or "").strip() == sp_id
        ]
        
    return {
        "total_sasaran_pokok": len(sp_list),
        "total_indikator": len(ind_list),
        "daftar_sasaran_pokok": sp_list
    }


@router.get("/sasaran-pokok")
def get_rpjpd_sasaran_pokok(db: Session = Depends(get_db)):
    """Mengambil daftar Sasaran Pokok RPJPD"""
    sql = text("""
        SELECT 
            id::text, kodepemda, idperiode, urut, idsasaran, uraisasaran,
            idmisi, uraimisi, arah_pembangunan, catatan, no, created_at
        FROM public.rpjpd_sasaran_pokok
        ORDER BY urut ASC, no ASC, idsasaran ASC
    """)
    return [dict(r) for r in db.execute(sql).mappings().all()]


@router.post("/sasaran-pokok", status_code=status.HTTP_201_CREATED)
def create_rpjpd_sasaran_pokok(payload: SasaranPokokCreate, db: Session = Depends(get_db)):
    """Menambahkan data Sasaran Pokok baru"""
    new_id = str(uuid.uuid4())
    sql = text("""
        INSERT INTO public.rpjpd_sasaran_pokok (
            id, kodepemda, idperiode, urut, idsasaran, uraisasaran,
            idmisi, uraimisi, arah_pembangunan, catatan, no, created_at
        ) VALUES (
            :id, :kodepemda, :idperiode, :urut, :idsasaran, :uraisasaran,
            :idmisi, :uraimisi, :arah_pembangunan::jsonb, :catatan::jsonb, :no, NOW()
        )
        RETURNING id::text
    """)
    res = db.execute(sql, {
        "id": new_id,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode,
        "urut": payload.urut,
        "idsasaran": payload.idsasaran,
        "uraisasaran": payload.uraisasaran,
        "idmisi": payload.idmisi,
        "uraimisi": payload.uraimisi,
        "arah_pembangunan": json.dumps(payload.arah_pembangunan or []),
        "catatan": json.dumps(payload.catatan or []),
        "no": payload.no
    }).scalar()
    db.commit()
    return {"message": "Sasaran Pokok berhasil ditambahkan", "id": res}


@router.put("/sasaran-pokok/{sp_id}")
def update_rpjpd_sasaran_pokok(sp_id: str, payload: SasaranPokokUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Sasaran Pokok"""
    fields = []
    params = {"sp_id": sp_id}
    
    if payload.idsasaran is not None:
        fields.append("idsasaran = :idsasaran")
        params["idsasaran"] = payload.idsasaran
    if payload.uraisasaran is not None:
        fields.append("uraisasaran = :uraisasaran")
        params["uraisasaran"] = payload.uraisasaran
    if payload.idmisi is not None:
        fields.append("idmisi = :idmisi")
        params["idmisi"] = payload.idmisi
    if payload.uraimisi is not None:
        fields.append("uraimisi = :uraimisi")
        params["uraimisi"] = payload.uraimisi
    if payload.urut is not None:
        fields.append("urut = :urut")
        params["urut"] = payload.urut
    if payload.no is not None:
        fields.append("no = :no")
        params["no"] = payload.no
    if payload.arah_pembangunan is not None:
        fields.append("arah_pembangunan = :arah_pembangunan::jsonb")
        params["arah_pembangunan"] = json.dumps(payload.arah_pembangunan)
    if payload.catatan is not None:
        fields.append("catatan = :catatan::jsonb")
        params["catatan"] = json.dumps(payload.catatan)
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data yang diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_sasaran_pokok SET {', '.join(fields)} WHERE id = :sp_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Sasaran Pokok tidak ditemukan")
        
    return {"message": "Sasaran Pokok berhasil diperbarui", "id": res}


@router.delete("/sasaran-pokok/{sp_id}")
def delete_rpjpd_sasaran_pokok(sp_id: str, db: Session = Depends(get_db)):
    """Menghapus data Sasaran Pokok"""
    sql = text("DELETE FROM public.rpjpd_sasaran_pokok WHERE id = :sp_id RETURNING id::text")
    res = db.execute(sql, {"sp_id": sp_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Sasaran Pokok tidak ditemukan")
        
    return {"message": "Sasaran Pokok berhasil dihapus", "id": res}


@router.get("/indikator-sasaran-pokok")
def get_rpjpd_indikator_sasaran_pokok(idsasaran: Optional[str] = None, db: Session = Depends(get_db)):
    """Mengambil daftar Indikator Sasaran Pokok"""
    query = """
        SELECT 
            id::text, idsasaran, idmisi, idtujuan, idsasaran_indikator,
            uraisasaran_indikator, satuan, status, kondisi_awal, baseline,
            target_1, target_2, target_3, target_4, kodeindikator_master,
            indikator_utama_pembangunan, sasaran_pokok_provinsi,
            indikator_sasaran_pokok_provinsi, tag_indikator_daerah, catatan,
            tipe_data, kodepemda, idperiode, urut, created_at
        FROM public.rpjpd_indikator_sasaran_pokok
    """
    params = {}
    if idsasaran:
        query += " WHERE idsasaran = :idsasaran"
        params["idsasaran"] = idsasaran
        
    query += " ORDER BY urut ASC, idsasaran_indikator ASC"
    return [dict(r) for r in db.execute(text(query), params).mappings().all()]


@router.post("/indikator-sasaran-pokok", status_code=status.HTTP_201_CREATED)
def create_rpjpd_indikator_sasaran_pokok(payload: IndikatorSasaranPokokCreate, db: Session = Depends(get_db)):
    """Menambahkan data Indikator Sasaran Pokok baru"""
    new_id = str(uuid.uuid4())
    sql = text("""
        INSERT INTO public.rpjpd_indikator_sasaran_pokok (
            id, idsasaran, idmisi, idtujuan, idsasaran_indikator,
            uraisasaran_indikator, satuan, status, kondisi_awal, baseline,
            target_1, target_2, target_3, target_4, kodeindikator_master,
            indikator_utama_pembangunan, sasaran_pokok_provinsi,
            indikator_sasaran_pokok_provinsi, tag_indikator_daerah, catatan,
            tipe_data, kodepemda, idperiode, urut, created_at
        ) VALUES (
            :id, :idsasaran, :idmisi, :idtujuan, :idsasaran_indikator,
            :uraisasaran_indikator, :satuan, :status, :kondisi_awal, :baseline,
            :target_1, :target_2, :target_3, :target_4, :kodeindikator_master,
            :indikator_utama_pembangunan::jsonb, :sasaran_pokok_provinsi::jsonb,
            :indikator_sasaran_pokok_provinsi::jsonb, :tag_indikator_daerah::jsonb, :catatan::jsonb,
            :tipe_data, :kodepemda, :idperiode, :urut, NOW()
        )
        RETURNING id::text
    """)
    res = db.execute(sql, {
        "id": new_id,
        "idsasaran": payload.idsasaran,
        "idmisi": payload.idmisi,
        "idtujuan": payload.idtujuan,
        "idsasaran_indikator": payload.idsasaran_indikator,
        "uraisasaran_indikator": payload.uraisasaran_indikator,
        "satuan": payload.satuan,
        "status": payload.status,
        "kondisi_awal": payload.kondisi_awal,
        "baseline": payload.baseline,
        "target_1": payload.target_1,
        "target_2": payload.target_2,
        "target_3": payload.target_3,
        "target_4": payload.target_4,
        "kodeindikator_master": payload.kodeindikator_master,
        "indikator_utama_pembangunan": json.dumps(payload.indikator_utama_pembangunan or []),
        "sasaran_pokok_provinsi": json.dumps(payload.sasaran_pokok_provinsi or []),
        "indikator_sasaran_pokok_provinsi": json.dumps(payload.indikator_sasaran_pokok_provinsi or []),
        "tag_indikator_daerah": json.dumps(payload.tag_indikator_daerah or []),
        "catatan": json.dumps(payload.catatan or []),
        "tipe_data": payload.tipe_data,
        "kodepemda": payload.kodepemda,
        "idperiode": payload.idperiode,
        "urut": payload.urut
    }).scalar()
    db.commit()
    return {"message": "Indikator Sasaran Pokok berhasil ditambahkan", "id": res}


@router.put("/indikator-sasaran-pokok/{ind_id}")
def update_rpjpd_indikator_sasaran_pokok(ind_id: str, payload: IndikatorSasaranPokokUpdate, db: Session = Depends(get_db)):
    """Memperbarui data Indikator Sasaran Pokok"""
    fields = []
    params = {"ind_id": ind_id}
    
    if payload.idsasaran is not None:
        fields.append("idsasaran = :idsasaran")
        params["idsasaran"] = payload.idsasaran
    if payload.idsasaran_indikator is not None:
        fields.append("idsasaran_indikator = :idsasaran_indikator")
        params["idsasaran_indikator"] = payload.idsasaran_indikator
    if payload.uraisasaran_indikator is not None:
        fields.append("uraisasaran_indikator = :uraisasaran_indikator")
        params["uraisasaran_indikator"] = payload.uraisasaran_indikator
    if payload.idmisi is not None:
        fields.append("idmisi = :idmisi")
        params["idmisi"] = payload.idmisi
    if payload.satuan is not None:
        fields.append("satuan = :satuan")
        params["satuan"] = payload.satuan
    if payload.status is not None:
        fields.append("status = :status")
        params["status"] = payload.status
    if payload.kondisi_awal is not None:
        fields.append("kondisi_awal = :kondisi_awal")
        params["kondisi_awal"] = payload.kondisi_awal
    if payload.baseline is not None:
        fields.append("baseline = :baseline")
        params["baseline"] = payload.baseline
    if payload.target_1 is not None:
        fields.append("target_1 = :target_1")
        params["target_1"] = payload.target_1
    if payload.target_2 is not None:
        fields.append("target_2 = :target_2")
        params["target_2"] = payload.target_2
    if payload.target_3 is not None:
        fields.append("target_3 = :target_3")
        params["target_3"] = payload.target_3
    if payload.target_4 is not None:
        fields.append("target_4 = :target_4")
        params["target_4"] = payload.target_4
    if payload.kodeindikator_master is not None:
        fields.append("kodeindikator_master = :kodeindikator_master")
        params["kodeindikator_master"] = payload.kodeindikator_master
    if payload.indikator_utama_pembangunan is not None:
        fields.append("indikator_utama_pembangunan = :indikator_utama_pembangunan::jsonb")
        params["indikator_utama_pembangunan"] = json.dumps(payload.indikator_utama_pembangunan)
    if payload.sasaran_pokok_provinsi is not None:
        fields.append("sasaran_pokok_provinsi = :sasaran_pokok_provinsi::jsonb")
        params["sasaran_pokok_provinsi"] = json.dumps(payload.sasaran_pokok_provinsi)
    if payload.indikator_sasaran_pokok_provinsi is not None:
        fields.append("indikator_sasaran_pokok_provinsi = :indikator_sasaran_pokok_provinsi::jsonb")
        params["indikator_sasaran_pokok_provinsi"] = json.dumps(payload.indikator_sasaran_pokok_provinsi)
    if payload.tag_indikator_daerah is not None:
        fields.append("tag_indikator_daerah = :tag_indikator_daerah::jsonb")
        params["tag_indikator_daerah"] = json.dumps(payload.tag_indikator_daerah)
    if payload.catatan is not None:
        fields.append("catatan = :catatan::jsonb")
        params["catatan"] = json.dumps(payload.catatan)
    if payload.tipe_data is not None:
        fields.append("tipe_data = :tipe_data")
        params["tipe_data"] = payload.tipe_data
    if payload.urut is not None:
        fields.append("urut = :urut")
        params["urut"] = payload.urut
        
    if not fields:
        raise HTTPException(status_code=400, detail="Tidak ada data yang diperbarui")
        
    sql = text(f"UPDATE public.rpjpd_indikator_sasaran_pokok SET {', '.join(fields)} WHERE id = :ind_id RETURNING id::text")
    res = db.execute(sql, params).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Indikator Sasaran Pokok tidak ditemukan")
        
    return {"message": "Indikator Sasaran Pokok berhasil diperbarui", "id": res}


@router.delete("/indikator-sasaran-pokok/{ind_id}")
def delete_rpjpd_indikator_sasaran_pokok(ind_id: str, db: Session = Depends(get_db)):
    """Menghapus data Indikator Sasaran Pokok"""
    sql = text("DELETE FROM public.rpjpd_indikator_sasaran_pokok WHERE id = :ind_id RETURNING id::text")
    res = db.execute(sql, {"ind_id": ind_id}).scalar()
    db.commit()
    
    if not res:
        raise HTTPException(status_code=404, detail="Data Indikator Sasaran Pokok tidak ditemukan")
        
    return {"message": "Indikator Sasaran Pokok berhasil dihapus", "id": res}



