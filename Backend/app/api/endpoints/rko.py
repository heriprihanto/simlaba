from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.deps import get_current_user_from_jwt, CurrentUser
import uuid
import json

router = APIRouter()


class LokasiItemSchema(BaseModel):
    id: Optional[str] = None
    nama_lokasi: Optional[str] = None
    jenis_geometry: Optional[str] = None
    geojson: Optional[dict] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    radius: Optional[float] = None


class PekerjaanCreate(BaseModel):
    id_sub_pd: int
    id_subkegiatan: str
    tahun: Optional[int] = 2026
    nomor_pekerjaan: Optional[int] = None
    nama_pekerjaan: str
    ket_pekerjaan: Optional[str] = None
    lokasi: Optional[str] = None
    pagu_anggaran: float
    volume: Optional[float] = None
    satuan: Optional[str] = None
    nomor_rup: Optional[str] = None
    jenis_paket: Optional[int] = 1
    jenis_pengadaan: Optional[int] = 1
    tipe_swa: Optional[int] = None
    penyelenggara_swa: Optional[str] = None
    metode: Optional[int] = None
    awal_pelaksanaan: Optional[int] = None
    akhir_pelaksanaan: Optional[int] = None
    pelaksanaan_bulan: Optional[List[int]] = None
    awal_pemilihan: Optional[int] = None
    akhir_pemilihan: Optional[int] = None
    awal_kontrak: Optional[int] = None
    akhir_kontrak: Optional[int] = None
    nama_ppk: Optional[str] = None
    nama_pptk: Optional[str] = None
    id_sumber_dana: Optional[int] = None
    sumber_dana: Optional[str] = None
    id_usulan_pokir: Optional[List[int]] = None
    id_usulan_musrenbang: Optional[List[int]] = None
    id_dak_detail_rincian: Optional[int] = None
    tags: Optional[List[str]] = None
    lokasi_list: Optional[List[LokasiItemSchema]] = None

    jan: Optional[float] = 0.0
    feb: Optional[float] = 0.0
    mar: Optional[float] = 0.0
    apr: Optional[float] = 0.0
    mei: Optional[float] = 0.0
    jun: Optional[float] = 0.0
    jul: Optional[float] = 0.0
    agu: Optional[float] = 0.0
    sep: Optional[float] = 0.0
    okt: Optional[float] = 0.0
    nov: Optional[float] = 0.0
    des: Optional[float] = 0.0

    jan_f: Optional[float] = 0.0
    feb_f: Optional[float] = 0.0
    mar_f: Optional[float] = 0.0
    apr_f: Optional[float] = 0.0
    mei_f: Optional[float] = 0.0
    jun_f: Optional[float] = 0.0
    jul_f: Optional[float] = 0.0
    agu_f: Optional[float] = 0.0
    sep_f: Optional[float] = 0.0
    okt_f: Optional[float] = 0.0
    nov_f: Optional[float] = 0.0
    des_f: Optional[float] = 0.0


class PekerjaanUpdate(BaseModel):
    nomor_pekerjaan: Optional[int] = None
    nama_pekerjaan: Optional[str] = None
    ket_pekerjaan: Optional[str] = None
    lokasi: Optional[str] = None
    pagu_anggaran: Optional[float] = None
    volume: Optional[float] = None
    satuan: Optional[str] = None
    nomor_rup: Optional[str] = None
    jenis_paket: Optional[int] = None
    jenis_pengadaan: Optional[int] = None
    tipe_swa: Optional[int] = None
    penyelenggara_swa: Optional[str] = None
    metode: Optional[int] = None
    awal_pelaksanaan: Optional[int] = None
    akhir_pelaksanaan: Optional[int] = None
    pelaksanaan_bulan: Optional[List[int]] = None
    awal_pemilihan: Optional[int] = None
    akhir_pemilihan: Optional[int] = None
    awal_kontrak: Optional[int] = None
    akhir_kontrak: Optional[int] = None
    nama_ppk: Optional[str] = None
    nama_pptk: Optional[str] = None
    id_sumber_dana: Optional[int] = None
    sumber_dana: Optional[str] = None
    id_usulan_pokir: Optional[List[int]] = None
    id_usulan_musrenbang: Optional[List[int]] = None
    id_dak_detail_rincian: Optional[int] = None
    tags: Optional[List[str]] = None
    lokasi_list: Optional[List[LokasiItemSchema]] = None

    jan: Optional[float] = None
    feb: Optional[float] = None
    mar: Optional[float] = None
    apr: Optional[float] = None
    mei: Optional[float] = None
    jun: Optional[float] = None
    jul: Optional[float] = None
    agu: Optional[float] = None
    sep: Optional[float] = None
    okt: Optional[float] = None
    nov: Optional[float] = None
    des: Optional[float] = None

    jan_f: Optional[float] = None
    feb_f: Optional[float] = None
    mar_f: Optional[float] = None
    apr_f: Optional[float] = None
    mei_f: Optional[float] = None
    jun_f: Optional[float] = None
    jul_f: Optional[float] = None
    agu_f: Optional[float] = None
    sep_f: Optional[float] = None
    okt_f: Optional[float] = None
    nov_f: Optional[float] = None
    des_f: Optional[float] = None


def normalize_targets(targets: List[float]) -> List[float]:
    """
    Enforces positive progressive targets, max 100%.
    If month A reaches 100%, all subsequent months become 100%.
    """
    result = []
    prev = 0.0
    for v in targets:
        val = max(0.0, min(100.0, float(v or 0.0)))
        if val < prev:
            val = prev
        if prev >= 100.0:
            val = 100.0
        result.append(round(val, 2))
        prev = val
    return result


def compute_monthly_rollups(children, get_pagu, get_targets):
    pagu_sum = sum(get_pagu(c) for c in children)
    result = [0.0] * 12
    if len(children) == 0:
        return result
    for m in range(12):
        if pagu_sum > 0:
            val = sum(get_pagu(c) * (get_targets(c)[m] or 0.0) for c in children) / pagu_sum
        else:
            val = sum((get_targets(c)[m] or 0.0) for c in children) / len(children)
        result[m] = round(val, 2)
    return result


@router.get("/opd")
def get_rko_opd_list(
    q: Optional[str] = Query(None, description="Search by OPD name or kode"),
    tahun: Optional[int] = Query(2026, description="Tahun Anggaran"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        where_clauses = ["(COALESCE(p.total_anggaran_pekerjaan, 0) > 0 OR COALESCE(s.total_anggaran_renja, 0) > 0)"]
        params = {"tahun": tahun}

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
                COALESCE(s.total_anggaran_renja, 0) AS total_anggaran_renja,
                COALESCE(p.total_anggaran_pekerjaan, 0) AS total_anggaran_pekerjaan,
                COALESCE(p.total_anggaran_pekerjaan, 0) AS total_anggaran,
                ABS(COALESCE(s.total_anggaran_renja, 0) - COALESCE(p.total_anggaran_pekerjaan, 0)) AS selisih_pagu,
                (ABS(COALESCE(s.total_anggaran_renja, 0) - COALESCE(p.total_anggaran_pekerjaan, 0)) > 1.0) AS is_pagu_mismatch,
                COALESCE(s.jumlah_subkegiatan, 0) AS jumlah_subkegiatan,
                COALESCE(p.jumlah_pekerjaan, 0) AS jumlah_pekerjaan,
                COALESCE(sub.status, 'DRAFT') AS status_rko
            FROM ta_opd o
            LEFT JOIN (
                SELECT id_sub_pd, COUNT(*) AS jumlah_subkegiatan, SUM(COALESCE(anggaran, pagu_renja, 0)) AS total_anggaran_renja
                FROM renja_subkegiatan
                WHERE tahun = :tahun OR :tahun IS NULL
                GROUP BY id_sub_pd
            ) s ON o.id_sub_pd = s.id_sub_pd
            LEFT JOIN (
                SELECT id_sub_pd, SUM(pagu_anggaran) AS total_anggaran_pekerjaan, COUNT(*) AS jumlah_pekerjaan
                FROM ta_pekerjaan
                WHERE (tahun = :tahun OR :tahun IS NULL) AND pagu_anggaran > 0
                GROUP BY id_sub_pd
            ) p ON o.id_sub_pd = p.id_sub_pd
            LEFT JOIN ta_rko_submission sub ON o.id_sub_pd = sub.id_sub_pd AND sub.tahun = :tahun
            {where_sql}
            ORDER BY o.kode ASC
        """)

        rows = db.execute(sql, params).mappings().all()
        results = []
        for r in rows:
            d = dict(r)
            d["total_anggaran_renja"] = float(d["total_anggaran_renja"] or 0)
            d["total_anggaran_pekerjaan"] = float(d["total_anggaran_pekerjaan"] or 0)
            d["total_anggaran"] = float(d["total_anggaran"] or 0)
            d["selisih_pagu"] = float(d["selisih_pagu"] or 0)
            d["is_pagu_mismatch"] = bool(d["is_pagu_mismatch"])
            results.append(d)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/summary")
def get_rko_summary(
    tahun: Optional[int] = Query(2026, description="Tahun Anggaran"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        where_clauses = ["COALESCE(p.total_anggaran, 0) > 0"]
        params = {"tahun": tahun}

        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if current_user.id_opds and len(current_user.id_opds) > 0:
                where_clauses.append("o.id_sub_pd = ANY(:id_opds)")
                params["id_opds"] = current_user.id_opds
            else:
                return {
                    "total_opd": 0,
                    "total_anggaran": 0,
                    "total_subkegiatan": 0,
                    "total_pekerjaan": 0
                }

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        sql = text(f"""
            SELECT 
                COUNT(o.id_sub_pd) AS total_opd,
                COALESCE(SUM(p.total_anggaran), 0) AS total_anggaran,
                COALESCE(SUM(s.jumlah_subkegiatan), 0) AS total_subkegiatan,
                COALESCE(SUM(p.jumlah_pekerjaan), 0) AS total_pekerjaan
            FROM ta_opd o
            LEFT JOIN (
                SELECT id_sub_pd, COUNT(*) AS jumlah_subkegiatan
                FROM renja_subkegiatan
                WHERE tahun = :tahun OR :tahun IS NULL
                GROUP BY id_sub_pd
            ) s ON o.id_sub_pd = s.id_sub_pd
            LEFT JOIN (
                SELECT id_sub_pd, SUM(pagu_anggaran) AS total_anggaran, COUNT(*) AS jumlah_pekerjaan
                FROM ta_pekerjaan
                WHERE (tahun = :tahun OR :tahun IS NULL) AND pagu_anggaran > 0
                GROUP BY id_sub_pd
            ) p ON o.id_sub_pd = p.id_sub_pd
            {where_sql}
        """)

        row = db.execute(sql, params).mappings().first()
        return dict(row) if row else {
            "total_opd": 0,
            "total_anggaran": 0,
            "total_subkegiatan": 0,
            "total_pekerjaan": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/detail/{id_sub_pd}")
def get_rko_opd_detail(
    id_sub_pd: int,
    tahun: Optional[int] = Query(2026, description="Tahun Anggaran"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke OPD ini")

    try:
        opd_sql = text("SELECT id_sub_pd, kode, nama_pd, nama_pd_singkat FROM ta_opd WHERE id_sub_pd = :id_sub_pd")
        opd_row = db.execute(opd_sql, {"id_sub_pd": id_sub_pd}).mappings().first()
        if not opd_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perangkat Daerah tidak ditemukan")

        sub_status_sql = text("SELECT status, submitted_at, submitted_by, approved_at, approved_by, notes FROM ta_rko_submission WHERE id_sub_pd = :id_sub_pd AND tahun = :tahun")
        sub_status_row = db.execute(sub_status_sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().first()
        status_rko = sub_status_row["status"] if sub_status_row else "DRAFT"
        submitted_at = sub_status_row["submitted_at"] if sub_status_row else None
        submitted_by = sub_status_row["submitted_by"] if sub_status_row else None
        approved_at = sub_status_row["approved_at"] if sub_status_row else None
        approved_by = sub_status_row["approved_by"] if sub_status_row else None
        notes = sub_status_row["notes"] if sub_status_row else None
        
        is_user_opd = (current_user is not None and current_user.role_id is not None and current_user.role_id > 5)
        is_locked = (status_rko in ("SUBMITTED", "APPROVED")) and is_user_opd

        detail_sql = text("""
            SELECT 
                s.kode_program,
                s.nm_program,
                s.kode_kegiatan,
                s.nm_kegiatan,
                s.idsubkegiatan,
                s.kode_sub_kegiatan,
                s.nm_sub_kegiatan,
                COALESCE(s.anggaran, 0) AS anggaran_renja,
                p.id AS id_pekerjaan,
                p.nama_pekerjaan,
                COALESCE(p.pagu_anggaran, 0) AS pagu_anggaran,
                p.jenis_paket,
                p.nomor_rup,
                p.nama_ppk,
                p.nama_pptk,
                p.id_usulan_pokir,
                p.id_usulan_musrenbang,
                p.id_dak_detail_rincian,
                COALESCE(p.jan, 0) AS jan_k, COALESCE(p.feb, 0) AS feb_k, COALESCE(p.mar, 0) AS mar_k,
                COALESCE(p.apr, 0) AS apr_k, COALESCE(p.mei, 0) AS mei_k, COALESCE(p.jun, 0) AS jun_k,
                COALESCE(p.jul, 0) AS jul_k, COALESCE(p.agu, 0) AS agu_k, COALESCE(p.sep, 0) AS sep_k,
                COALESCE(p.okt, 0) AS okt_k, COALESCE(p.nov, 0) AS nov_k, COALESCE(p.des, 0) AS des_k,
                COALESCE(p.jan_f, 0) AS jan_f, COALESCE(p.feb_f, 0) AS feb_f, COALESCE(p.mar_f, 0) AS mar_f,
                COALESCE(p.apr_f, 0) AS apr_f, COALESCE(p.mei_f, 0) AS mei_f, COALESCE(p.jun_f, 0) AS jun_f,
                COALESCE(p.jul_f, 0) AS jul_f, COALESCE(p.agu_f, 0) AS agu_f, COALESCE(p.sep_f, 0) AS sep_f,
                COALESCE(p.okt_f, 0) AS okt_f, COALESCE(p.nov_f, 0) AS nov_f, COALESCE(p.des_f, 0) AS des_f
            FROM renja_subkegiatan s
            LEFT JOIN ta_pekerjaan p ON s.id_sub_pd = p.id_sub_pd AND s.idsubkegiatan = p.id_subkegiatan
            WHERE s.id_sub_pd = :id_sub_pd AND (s.tahun = :tahun OR :tahun IS NULL)
            ORDER BY s.kode_program ASC, s.kode_kegiatan ASC, s.kode_sub_kegiatan ASC, p.id ASC
        """)
        rows = db.execute(detail_sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()

        programs_dict = {}
        subkegiatan_seen = set()
        total_anggaran_renja = 0.0
        total_anggaran_pekerjaan = 0.0
        total_pekerjaan_count = 0

        for r in rows:
            kd_prog = r["kode_program"] or "0.00"
            nm_prog = r["nm_program"] or "Program Tanpa Nama"
            kd_keg = r["kode_kegiatan"] or "0.00.00"
            nm_keg = r["nm_kegiatan"] or "Kegiatan Tanpa Nama"
            id_sub_uuid = str(r["idsubkegiatan"]) if r["idsubkegiatan"] else ""
            kd_sub = r["kode_sub_kegiatan"] or "0.00.00.0000"
            nm_sub = r["nm_sub_kegiatan"] or "Subkegiatan Tanpa Nama"
            anggaran_renja = float(r["anggaran_renja"] or 0)
            pagu_pek = float(r["pagu_anggaran"] or 0)

            target_k = normalize_targets([float(r[f"{m}_k"] or 0) for m in ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "sep", "okt", "nov", "des"]])
            target_f = normalize_targets([float(r[f"{m}_f"] or 0) for m in ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "sep", "okt", "nov", "des"]])

            if kd_prog not in programs_dict:
                programs_dict[kd_prog] = {
                    "kode": kd_prog,
                    "nama": nm_prog,
                    "anggaran_renja": 0.0,
                    "anggaran_pekerjaan": 0.0,
                    "kegiatan_dict": {}
                }

            prog = programs_dict[kd_prog]

            if kd_keg not in prog["kegiatan_dict"]:
                prog["kegiatan_dict"][kd_keg] = {
                    "kode": kd_keg,
                    "nama": nm_keg,
                    "anggaran_renja": 0.0,
                    "anggaran_pekerjaan": 0.0,
                    "subkegiatan_dict": {}
                }

            keg = prog["kegiatan_dict"][kd_keg]

            if kd_sub not in keg["subkegiatan_dict"]:
                keg["subkegiatan_dict"][kd_sub] = {
                    "idsubkegiatan": id_sub_uuid,
                    "kode": kd_sub,
                    "nama": nm_sub,
                    "anggaran_renja": anggaran_renja,
                    "anggaran_pekerjaan": 0.0,
                    "pekerjaan": []
                }
                keg["anggaran_renja"] += anggaran_renja
                prog["anggaran_renja"] += anggaran_renja
                total_anggaran_renja += anggaran_renja
                subkegiatan_seen.add(kd_sub)

            sub = keg["subkegiatan_dict"][kd_sub]

            if r["id_pekerjaan"]:
                sub["pekerjaan"].append({
                    "id": str(r["id_pekerjaan"]),
                    "nama_pekerjaan": r["nama_pekerjaan"],
                    "pagu_anggaran": pagu_pek,
                    "jenis_paket": r["jenis_paket"],
                    "nomor_rup": r["nomor_rup"],
                    "nama_ppk": r["nama_ppk"],
                    "nama_pptk": r["nama_pptk"],
                    "id_usulan_pokir": r["id_usulan_pokir"],
                    "id_usulan_musrenbang": r["id_usulan_musrenbang"],
                    "id_dak_detail_rincian": r["id_dak_detail_rincian"],
                    "target_keuangan": target_k,
                    "target_fisik": target_f
                })
                sub["anggaran_pekerjaan"] += pagu_pek
                keg["anggaran_pekerjaan"] += pagu_pek
                prog["anggaran_pekerjaan"] += pagu_pek
                total_anggaran_pekerjaan += pagu_pek
                total_pekerjaan_count += 1

        programs_list = []
        for prog in programs_dict.values():
            kegiatan_list = []
            for keg in prog["kegiatan_dict"].values():
                subkegiatan_list = []
                for sub in keg["subkegiatan_dict"].values():
                    sub_tf = compute_monthly_rollups(sub["pekerjaan"], lambda x: x["pagu_anggaran"], lambda x: x["target_fisik"])
                    sub_tk = compute_monthly_rollups(sub["pekerjaan"], lambda x: x["pagu_anggaran"], lambda x: x["target_keuangan"])
                    subkegiatan_list.append({
                        "idsubkegiatan": sub["idsubkegiatan"],
                        "kode": sub["kode"],
                        "nama": sub["nama"],
                        "anggaran_renja": sub["anggaran_renja"],
                        "anggaran_pekerjaan": sub["anggaran_pekerjaan"],
                        "target_fisik": sub_tf,
                        "target_keuangan": sub_tk,
                        "pekerjaan": sub["pekerjaan"]
                    })

                keg_tf = compute_monthly_rollups(subkegiatan_list, lambda x: x["anggaran_pekerjaan"], lambda x: x["target_fisik"])
                keg_tk = compute_monthly_rollups(subkegiatan_list, lambda x: x["anggaran_pekerjaan"], lambda x: x["target_keuangan"])
                kegiatan_list.append({
                    "kode": keg["kode"],
                    "nama": keg["nama"],
                    "anggaran_renja": keg["anggaran_renja"],
                    "anggaran_pekerjaan": keg["anggaran_pekerjaan"],
                    "target_fisik": keg_tf,
                    "target_keuangan": keg_tk,
                    "subkegiatan": subkegiatan_list
                })

            prog_tf = compute_monthly_rollups(kegiatan_list, lambda x: x["anggaran_pekerjaan"], lambda x: x["target_fisik"])
            prog_tk = compute_monthly_rollups(kegiatan_list, lambda x: x["anggaran_pekerjaan"], lambda x: x["target_keuangan"])
            programs_list.append({
                "kode": prog["kode"],
                "nama": prog["nama"],
                "anggaran_renja": prog["anggaran_renja"],
                "anggaran_pekerjaan": prog["anggaran_pekerjaan"],
                "target_fisik": prog_tf,
                "target_keuangan": prog_tk,
                "kegiatan": kegiatan_list
            })

        opd_dict = dict(opd_row)
        opd_dict["status_rko"] = status_rko
        opd_dict["submitted_at"] = submitted_at
        opd_dict["submitted_by"] = submitted_by
        opd_dict["approved_at"] = approved_at
        opd_dict["approved_by"] = approved_by
        opd_dict["notes"] = notes
        opd_dict["is_locked"] = is_locked

        return {
            "opd": opd_dict,
            "tahun": tahun,
            "status_rko": status_rko,
            "submitted_at": submitted_at,
            "submitted_by": submitted_by,
            "approved_at": approved_at,
            "approved_by": approved_by,
            "notes": notes,
            "is_locked": is_locked,
            "total_anggaran_renja": total_anggaran_renja,
            "total_anggaran_pekerjaan": total_anggaran_pekerjaan,
            "total_program": len(programs_list),
            "total_subkegiatan": len(subkegiatan_seen),
            "total_pekerjaan": total_pekerjaan_count,
            "programs": programs_list
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ════════════════════════════════════════════════════════════════════
# PEKERJAAN CRUD ENDPOINTS WITH TARGET VALIDATION
# ════════════════════════════════════════════════════════════════════

def check_rko_unlocked(id_sub_pd: int, tahun: int, db: Session, current_user: Optional[CurrentUser]):
    if current_user and current_user.role_id is not None and current_user.role_id <= 5:
        return  # Admin is allowed to edit

    sql = text("SELECT status FROM ta_rko_submission WHERE id_sub_pd = :id_sub_pd AND tahun = :tahun")
    row = db.execute(sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().first()
    if row and row["status"] in ("SUBMITTED", "APPROVED"):
        status_label = "Disubmit OPD" if row["status"] == "SUBMITTED" else "Disetujui Admin"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Data RKO OPD ini telah {status_label} dan TERKUNCI. Anda tidak dapat menambah, mengubah, atau menghapus pekerjaan. Hubungi Admin BAPPEDA untuk membuka kuncian RKO."
        )


@router.post("/pekerjaan", status_code=status.HTTP_201_CREATED)
def create_pekerjaan(
    payload: PekerjaanCreate,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or payload.id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke OPD ini")

    check_rko_unlocked(payload.id_sub_pd, payload.tahun or 2026, db, current_user)

    try:
        new_id = str(uuid.uuid4())
        tk = normalize_targets([payload.jan, payload.feb, payload.mar, payload.apr, payload.mei, payload.jun, payload.jul, payload.agu, payload.sep, payload.okt, payload.nov, payload.des])
        tf = normalize_targets([payload.jan_f, payload.feb_f, payload.mar_f, payload.apr_f, payload.mei_f, payload.jun_f, payload.jul_f, payload.agu_f, payload.sep_f, payload.okt_f, payload.nov_f, payload.des_f])

        tags_list = payload.tags or []
        tg1 = tags_list[0] if len(tags_list) > 0 else None
        tg2 = tags_list[1] if len(tags_list) > 1 else None
        tg3 = tags_list[2] if len(tags_list) > 2 else None
        tg4 = tags_list[3] if len(tags_list) > 3 else None
        tg5 = tags_list[4] if len(tags_list) > 4 else None

        p_bulan = payload.pelaksanaan_bulan or []
        awal_p = min(p_bulan) if p_bulan else payload.awal_pelaksanaan
        akhir_p = max(p_bulan) if p_bulan else payload.akhir_pelaksanaan

        sql = text("""
            INSERT INTO ta_pekerjaan (
                id, id_sub_pd, id_subkegiatan, tahun, nomor_pekerjaan, nama_pekerjaan, ket_pekerjaan, lokasi, pagu_anggaran,
                volume, satuan, nomor_rup, jenis_paket, jenis_pengadaan, tipe_swa, penyelenggara_swa, metode,
                awal_pelaksanaan, akhir_pelaksanaan, pelaksanaan_bulan, awal_pemilihan, akhir_pemilihan, awal_kontrak, akhir_kontrak,
                nama_ppk, nama_pptk, id_sumber_dana, sumber_dana, id_usulan_pokir, id_usulan_musrenbang, id_dak_detail_rincian,
                tg1, tg2, tg3, tg4, tg5,
                jan, feb, mar, apr, mei, jun, jul, agu, sep, okt, nov, des,
                jan_f, feb_f, mar_f, apr_f, mei_f, jun_f, jul_f, agu_f, sep_f, okt_f, nov_f, des_f
            ) VALUES (
                :id, :id_sub_pd, :id_subkegiatan, :tahun, :nomor_pekerjaan, :nama_pekerjaan, :ket_pekerjaan, :lokasi, :pagu_anggaran,
                :volume, :satuan, :nomor_rup, :jenis_paket, :jenis_pengadaan, :tipe_swa, :penyelenggara_swa, :metode,
                :awal_pelaksanaan, :akhir_pelaksanaan, :pelaksanaan_bulan, :awal_pemilihan, :akhir_pemilihan, :awal_kontrak, :akhir_kontrak,
                :nama_ppk, :nama_pptk, :id_sumber_dana, :sumber_dana, :id_usulan_pokir, :id_usulan_musrenbang, :id_dak_detail_rincian,
                :tg1, :tg2, :tg3, :tg4, :tg5,
                :jan, :feb, :mar, :apr, :mei, :jun, :jul, :agu, :sep, :okt, :nov, :des,
                :jan_f, :feb_f, :mar_f, :apr_f, :mei_f, :jun_f, :jul_f, :agu_f, :sep_f, :okt_f, :nov_f, :des_f
            )
            RETURNING id, id_sub_pd, id_subkegiatan, tahun, nama_pekerjaan, pagu_anggaran
        """)
        new_row = db.execute(sql, {
            "id": new_id,
            "id_sub_pd": payload.id_sub_pd,
            "id_subkegiatan": payload.id_subkegiatan,
            "tahun": payload.tahun or 2026,
            "nomor_pekerjaan": payload.nomor_pekerjaan,
            "nama_pekerjaan": payload.nama_pekerjaan,
            "ket_pekerjaan": payload.ket_pekerjaan,
            "lokasi": payload.lokasi,
            "pagu_anggaran": payload.pagu_anggaran,
            "volume": payload.volume,
            "satuan": payload.satuan,
            "nomor_rup": payload.nomor_rup,
            "jenis_paket": payload.jenis_paket or 1,
            "jenis_pengadaan": payload.jenis_pengadaan or 1,
            "tipe_swa": payload.tipe_swa,
            "penyelenggara_swa": payload.penyelenggara_swa,
            "metode": payload.metode,
            "awal_pelaksanaan": awal_p,
            "akhir_pelaksanaan": akhir_p,
            "pelaksanaan_bulan": p_bulan if p_bulan else None,
            "awal_pemilihan": payload.awal_pemilihan,
            "akhir_pemilihan": payload.akhir_pemilihan,
            "awal_kontrak": payload.awal_kontrak,
            "akhir_kontrak": payload.akhir_kontrak,
            "nama_ppk": payload.nama_ppk,
            "nama_pptk": payload.nama_pptk,
            "id_sumber_dana": payload.id_sumber_dana,
            "sumber_dana": payload.sumber_dana,
            "id_usulan_pokir": payload.id_usulan_pokir,
            "id_usulan_musrenbang": payload.id_usulan_musrenbang,
            "id_dak_detail_rincian": payload.id_dak_detail_rincian,
            "tg1": tg1, "tg2": tg2, "tg3": tg3, "tg4": tg4, "tg5": tg5,
            "jan": tk[0], "feb": tk[1], "mar": tk[2], "apr": tk[3], "mei": tk[4], "jun": tk[5],
            "jul": tk[6], "agu": tk[7], "sep": tk[8], "okt": tk[9], "nov": tk[10], "des": tk[11],
            "jan_f": tf[0], "feb_f": tf[1], "mar_f": tf[2], "apr_f": tf[3], "mei_f": tf[4], "jun_f": tf[5],
            "jul_f": tf[6], "agu_f": tf[7], "sep_f": tf[8], "okt_f": tf[9], "nov_f": tf[10], "des_f": tf[11]
        }).mappings().first()
        db.commit()
        res = dict(new_row)
        res["id"] = str(res["id"])
        res["id_subkegiatan"] = str(res["id_subkegiatan"])

        # Insert multiple locations if provided
        if payload.lokasi_list:
            for loc in payload.lokasi_list:
                loc_id = loc.id or str(uuid.uuid4())
                geojson_obj = loc.geojson or {}
                geojson_str = json.dumps(geojson_obj) if geojson_obj else "{}"

                if geojson_obj and "type" in geojson_obj:
                    sql_loc = text("""
                        INSERT INTO ta_pekerjaan_lokasi (
                            id, id_pekerjaan, nama_lokasi, jenis_geometry, geojson, geom, lat, lng, radius
                        ) VALUES (
                            :id, :id_pekerjaan, :nama_lokasi, :jenis_geometry, CAST(:geojson AS jsonb),
                            ST_SetSRID(ST_GeomFromGeoJSON(:geojson_str), 4326), :lat, :lng, :radius
                        )
                    """)
                else:
                    sql_loc = text("""
                        INSERT INTO ta_pekerjaan_lokasi (
                            id, id_pekerjaan, nama_lokasi, jenis_geometry, geojson, geom, lat, lng, radius
                        ) VALUES (
                            :id, :id_pekerjaan, :nama_lokasi, :jenis_geometry, CAST(:geojson AS jsonb),
                            NULL, :lat, :lng, :radius
                        )
                    """)
                db.execute(sql_loc, {
                    "id": loc_id,
                    "id_pekerjaan": new_id,
                    "nama_lokasi": loc.nama_lokasi or payload.nama_pekerjaan,
                    "jenis_geometry": loc.jenis_geometry or "Point",
                    "geojson": json.dumps(geojson_obj),
                    "geojson_str": geojson_str,
                    "lat": loc.lat,
                    "lng": loc.lng,
                    "radius": loc.radius
                })

        db.commit()
        return res
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal membuat pekerjaan: {str(e)}")


@router.get("/pekerjaan/{pekerjaan_id}")
def get_pekerjaan_by_id(pekerjaan_id: str, db: Session = Depends(get_db)):
    sql = text("SELECT * FROM ta_pekerjaan WHERE id = :id")
    row = db.execute(sql, {"id": pekerjaan_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pekerjaan tidak ditemukan")
    res = dict(row)
    res["id"] = str(res["id"])
    if res.get("id_subkegiatan"):
        res["id_subkegiatan"] = str(res["id_subkegiatan"])
    
    # Compile tags array from tg1..tg5
    tags = [r for r in [res.get("tg1"), res.get("tg2"), res.get("tg3"), res.get("tg4"), res.get("tg5")] if r]
    res["tags"] = tags

    # Fetch multiple PostGIS locations
    loc_sql = text("""
        SELECT id, id_pekerjaan, nama_lokasi, jenis_geometry, geojson, lat, lng, radius,
               ST_AsGeoJSON(geom) AS st_geojson
        FROM ta_pekerjaan_lokasi
        WHERE id_pekerjaan = :id
        ORDER BY created_at ASC
    """)
    loc_rows = db.execute(loc_sql, {"id": pekerjaan_id}).mappings().all()
    res["lokasi_list"] = [dict(r) for r in loc_rows]
    return res


@router.put("/pekerjaan/{pekerjaan_id}")
def update_pekerjaan(
    pekerjaan_id: str,
    payload: PekerjaanUpdate,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    check_sql = text("SELECT * FROM ta_pekerjaan WHERE id = :id")
    row = db.execute(check_sql, {"id": pekerjaan_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pekerjaan tidak ditemukan")

    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or row["id_sub_pd"] not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke OPD ini")

    check_rko_unlocked(row["id_sub_pd"], row["tahun"] if "tahun" in row and row["tahun"] else 2026, db, current_user)

    try:
        month_keys = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "sep", "okt", "nov", "des"]
        
        raw_tk = [getattr(payload, m) if getattr(payload, m) is not None else float(row[m] or 0) for m in month_keys]
        raw_tf = [getattr(payload, m + "_f") if getattr(payload, m + "_f") is not None else float(row[m + "_f"] or 0) for m in month_keys]

        tk = normalize_targets(raw_tk)
        tf = normalize_targets(raw_tf)

        tags_list = payload.tags if payload.tags is not None else [row["tg1"], row["tg2"], row["tg3"], row["tg4"], row["tg5"]]
        tags_list = [t for t in tags_list if t]
        tg1 = tags_list[0] if len(tags_list) > 0 else None
        tg2 = tags_list[1] if len(tags_list) > 1 else None
        tg3 = tags_list[2] if len(tags_list) > 2 else None
        tg4 = tags_list[3] if len(tags_list) > 3 else None
        tg5 = tags_list[4] if len(tags_list) > 4 else None

        p_bulan = payload.pelaksanaan_bulan if payload.pelaksanaan_bulan is not None else row.get("pelaksanaan_bulan")
        if p_bulan:
            awal_p = min(p_bulan)
            akhir_p = max(p_bulan)
        else:
            awal_p = payload.awal_pelaksanaan if payload.awal_pelaksanaan is not None else row.get("awal_pelaksanaan")
            akhir_p = payload.akhir_pelaksanaan if payload.akhir_pelaksanaan is not None else row.get("akhir_pelaksanaan")

        sql = text("""
            UPDATE ta_pekerjaan
            SET nomor_pekerjaan = COALESCE(:nomor_pekerjaan, nomor_pekerjaan),
                nama_pekerjaan = COALESCE(:nama_pekerjaan, nama_pekerjaan),
                ket_pekerjaan = COALESCE(:ket_pekerjaan, ket_pekerjaan),
                lokasi = COALESCE(:lokasi, lokasi),
                pagu_anggaran = COALESCE(:pagu_anggaran, pagu_anggaran),
                volume = COALESCE(:volume, volume),
                satuan = COALESCE(:satuan, satuan),
                nomor_rup = COALESCE(:nomor_rup, nomor_rup),
                jenis_paket = COALESCE(:jenis_paket, jenis_paket),
                jenis_pengadaan = COALESCE(:jenis_pengadaan, jenis_pengadaan),
                tipe_swa = COALESCE(:tipe_swa, tipe_swa),
                penyelenggara_swa = COALESCE(:penyelenggara_swa, penyelenggara_swa),
                metode = COALESCE(:metode, metode),
                awal_pelaksanaan = :awal_pelaksanaan,
                akhir_pelaksanaan = :akhir_pelaksanaan,
                pelaksanaan_bulan = :pelaksanaan_bulan,
                awal_pemilihan = COALESCE(:awal_pemilihan, awal_pemilihan),
                akhir_pemilihan = COALESCE(:akhir_pemilihan, akhir_pemilihan),
                awal_kontrak = COALESCE(:awal_kontrak, awal_kontrak),
                akhir_kontrak = COALESCE(:akhir_kontrak, akhir_kontrak),
                nama_ppk = COALESCE(:nama_ppk, nama_ppk),
                nama_pptk = COALESCE(:nama_pptk, nama_pptk),
                id_sumber_dana = COALESCE(:id_sumber_dana, id_sumber_dana),
                sumber_dana = COALESCE(:sumber_dana, sumber_dana),
                id_usulan_pokir = :id_usulan_pokir,
                id_usulan_musrenbang = :id_usulan_musrenbang,
                id_dak_detail_rincian = :id_dak_detail_rincian,
                tg1 = :tg1, tg2 = :tg2, tg3 = :tg3, tg4 = :tg4, tg5 = :tg5,
                jan = :jan, feb = :feb, mar = :mar, apr = :apr, mei = :mei, jun = :jun,
                jul = :jul, agu = :agu, sep = :sep, okt = :okt, nov = :nov, des = :des,
                jan_f = :jan_f, feb_f = :feb_f, mar_f = :mar_f, apr_f = :apr_f, mei_f = :mei_f, jun_f = :jun_f,
                jul_f = :jul_f, agu_f = :agu_f, sep_f = :sep_f, okt_f = :okt_f, nov_f = :nov_f, des_f = :des_f
            WHERE id = :id
            RETURNING id, nama_pekerjaan, pagu_anggaran
        """)
        updated_row = db.execute(sql, {
            "id": pekerjaan_id,
            "nomor_pekerjaan": payload.nomor_pekerjaan,
            "nama_pekerjaan": payload.nama_pekerjaan,
            "ket_pekerjaan": payload.ket_pekerjaan,
            "lokasi": payload.lokasi,
            "pagu_anggaran": payload.pagu_anggaran,
            "volume": payload.volume,
            "satuan": payload.satuan,
            "nomor_rup": payload.nomor_rup,
            "jenis_paket": payload.jenis_paket,
            "jenis_pengadaan": payload.jenis_pengadaan,
            "tipe_swa": payload.tipe_swa,
            "penyelenggara_swa": payload.penyelenggara_swa,
            "metode": payload.metode,
            "awal_pelaksanaan": awal_p,
            "akhir_pelaksanaan": akhir_p,
            "pelaksanaan_bulan": p_bulan if p_bulan else None,
            "awal_pemilihan": payload.awal_pemilihan,
            "akhir_pemilihan": payload.akhir_pemilihan,
            "awal_kontrak": payload.awal_kontrak,
            "akhir_kontrak": payload.akhir_kontrak,
            "nama_ppk": payload.nama_ppk,
            "nama_pptk": payload.nama_pptk,
            "id_sumber_dana": payload.id_sumber_dana,
            "sumber_dana": payload.sumber_dana,
            "id_usulan_pokir": payload.id_usulan_pokir if payload.id_usulan_pokir is not None else row.get("id_usulan_pokir"),
            "id_usulan_musrenbang": payload.id_usulan_musrenbang if payload.id_usulan_musrenbang is not None else row.get("id_usulan_musrenbang"),
            "id_dak_detail_rincian": payload.id_dak_detail_rincian if payload.id_dak_detail_rincian is not None else row.get("id_dak_detail_rincian"),
            "tg1": tg1, "tg2": tg2, "tg3": tg3, "tg4": tg4, "tg5": tg5,
            "jan": tk[0], "feb": tk[1], "mar": tk[2], "apr": tk[3], "mei": tk[4], "jun": tk[5],
            "jul": tk[6], "agu": tk[7], "sep": tk[8], "okt": tk[9], "nov": tk[10], "des": tk[11],
            "jan_f": tf[0], "feb_f": tf[1], "mar_f": tf[2], "apr_f": tf[3], "mei_f": tf[4], "jun_f": tf[5],
            "jul_f": tf[6], "agu_f": tf[7], "sep_f": tf[8], "okt_f": tf[9], "nov_f": tf[10], "des_f": tf[11]
        }).mappings().first()

        # Replace locations if lokasi_list provided
        if payload.lokasi_list is not None:
            db.execute(text("DELETE FROM ta_pekerjaan_lokasi WHERE id_pekerjaan = :id"), {"id": pekerjaan_id})
            for loc in payload.lokasi_list:
                loc_id = loc.id or str(uuid.uuid4())
                geojson_obj = loc.geojson or {}
                geojson_str = json.dumps(geojson_obj) if geojson_obj else "{}"

                if geojson_obj and "type" in geojson_obj:
                    sql_loc = text("""
                        INSERT INTO ta_pekerjaan_lokasi (
                            id, id_pekerjaan, nama_lokasi, jenis_geometry, geojson, geom, lat, lng, radius
                        ) VALUES (
                            :id, :id_pekerjaan, :nama_lokasi, :jenis_geometry, CAST(:geojson AS jsonb),
                            ST_SetSRID(ST_GeomFromGeoJSON(:geojson_str), 4326), :lat, :lng, :radius
                        )
                    """)
                else:
                    sql_loc = text("""
                        INSERT INTO ta_pekerjaan_lokasi (
                            id, id_pekerjaan, nama_lokasi, jenis_geometry, geojson, geom, lat, lng, radius
                        ) VALUES (
                            :id, :id_pekerjaan, :nama_lokasi, :jenis_geometry, CAST(:geojson AS jsonb),
                            NULL, :lat, :lng, :radius
                        )
                    """)
                db.execute(sql_loc, {
                    "id": loc_id,
                    "id_pekerjaan": pekerjaan_id,
                    "nama_lokasi": loc.nama_lokasi or (row["nama_pekerjaan"] if row else "Lokasi Pekerjaan"),
                    "jenis_geometry": loc.jenis_geometry or "Point",
                    "geojson": json.dumps(geojson_obj),
                    "geojson_str": geojson_str,
                    "lat": loc.lat,
                    "lng": loc.lng,
                    "radius": loc.radius
                })

        db.commit()
        res = dict(updated_row)
        res["id"] = str(res["id"])
        return res
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal mengupdate pekerjaan: {str(e)}")


@router.delete("/pekerjaan/{pekerjaan_id}")
def delete_pekerjaan(
    pekerjaan_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    check_sql = text("SELECT id, id_sub_pd FROM ta_pekerjaan WHERE id = :id")
    row = db.execute(check_sql, {"id": pekerjaan_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pekerjaan tidak ditemukan")

    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or row["id_sub_pd"] not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke OPD ini")

    check_rko_unlocked(row["id_sub_pd"], row.get("tahun") or 2026, db, current_user)

    try:
        delete_sql = text("DELETE FROM ta_pekerjaan WHERE id = :id")
        db.execute(delete_sql, {"id": pekerjaan_id})
        db.commit()
        return {"message": "Paket Pekerjaan berhasil dihapus", "id": pekerjaan_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Gagal menghapus pekerjaan: {str(e)}")


# ════════════════════════════════════════════════════════════════════
# PROSEDUR SUBMIT RKO & VALIDASI 3 ATURAN KELAYAKAN
# ════════════════════════════════════════════════════════════════════

@router.get("/submission-status/{id_sub_pd}")
def get_submission_status(id_sub_pd: int, tahun: int = Query(2026), db: Session = Depends(get_db)):
    sql = text("""
        SELECT status, submitted_at, submitted_by, notes
        FROM ta_rko_submission
        WHERE id_sub_pd = :id_sub_pd AND tahun = :tahun
    """)
    row = db.execute(sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().first()
    if row:
        return dict(row)
    return {"status": "DRAFT", "submitted_at": None, "submitted_by": None, "notes": None}


@router.get("/validate-submit/{id_sub_pd}")
def validate_rko_submission(
    id_sub_pd: int,
    tahun: int = Query(2026),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke OPD ini")

    # Rule 1: Minimal 1 Pekerjaan pada setiap Subkegiatan (Khusus OPD id_sub_pd)
    sql_rule1 = text("""
        SELECT s.idsubkegiatan, s.kode_sub_kegiatan, s.nm_sub_kegiatan, COUNT(p.id) AS total_pek
        FROM renja_subkegiatan s
        LEFT JOIN ta_pekerjaan p ON s.idsubkegiatan = p.id_subkegiatan AND p.tahun = :tahun
        WHERE s.id_sub_pd = :id_sub_pd AND s.tahun = :tahun
        GROUP BY s.idsubkegiatan, s.kode_sub_kegiatan, s.nm_sub_kegiatan
        HAVING COUNT(p.id) = 0;
    """)
    rule1_rows = db.execute(sql_rule1, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()
    rule1_failed = [
        {"kode": r["kode_sub_kegiatan"], "nama": r["nm_sub_kegiatan"]} for r in rule1_rows
    ]

    # Rule 2: Tidak ada selisih pagu anggaran renja subkegiatan dan total pagu pekerjaan
    sql_rule2 = text("""
        SELECT s.idsubkegiatan, s.kode_sub_kegiatan, s.nm_sub_kegiatan,
               COALESCE(s.anggaran, s.pagu_renja, 0) AS pagu_renja,
               COALESCE(SUM(p.pagu_anggaran), 0) AS total_pagu_pek,
               ABS(COALESCE(s.anggaran, s.pagu_renja, 0) - COALESCE(SUM(p.pagu_anggaran), 0)) AS selisih
        FROM renja_subkegiatan s
        LEFT JOIN ta_pekerjaan p ON s.idsubkegiatan = p.id_subkegiatan AND p.tahun = :tahun
        WHERE s.id_sub_pd = :id_sub_pd AND s.tahun = :tahun
        GROUP BY s.idsubkegiatan, s.kode_sub_kegiatan, s.nm_sub_kegiatan, s.anggaran, s.pagu_renja
        HAVING ABS(COALESCE(s.anggaran, s.pagu_renja, 0) - COALESCE(SUM(p.pagu_anggaran), 0)) > 1.0;
    """)
    rule2_rows = db.execute(sql_rule2, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()
    rule2_failed = [
        {
            "kode": r["kode_sub_kegiatan"],
            "nama": r["nm_sub_kegiatan"],
            "pagu_renja": float(r["pagu_renja"]),
            "pagu_pekerjaan": float(r["total_pagu_pek"]),
            "selisih": float(r["selisih"])
        } for r in rule2_rows
    ]

    # Rule 3: Target Keuangan dan Fisik pada bulan Desember sudah 100%
    sql_rule3 = text("""
        SELECT id, nomor_pekerjaan, nama_pekerjaan, des, des_f
        FROM ta_pekerjaan
        WHERE id_sub_pd = :id_sub_pd AND tahun = :tahun AND (des < 100 OR des_f < 100);
    """)
    rule3_rows = db.execute(sql_rule3, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()
    rule3_failed = [
        {
            "id": str(r["id"]),
            "nama_pekerjaan": r["nama_pekerjaan"],
            "target_keuangan_des": float(r["des"]),
            "target_fisik_des": float(r["des_f"])
        } for r in rule3_rows
    ]

    checklist = [
        {
            "id": "rule_1",
            "title": "Minimal 1 Pekerjaan per Subkegiatan",
            "passed": len(rule1_failed) == 0,
            "message": "Semua subkegiatan memiliki minimal 1 pekerjaan" if len(rule1_failed) == 0 else f"Ada {len(rule1_failed)} subkegiatan yang belum memiliki pekerjaan",
            "items": rule1_failed
        },
        {
            "id": "rule_2",
            "title": "Tidak Ada Perbedaan Pagu Anggaran",
            "passed": len(rule2_failed) == 0,
            "message": "Total pagu pekerjaan sesuai dengan pagu renja subkegiatan" if len(rule2_failed) == 0 else f"Ada {len(rule2_failed)} subkegiatan dengan selisih pagu anggaran",
            "items": rule2_failed
        },
        {
            "id": "rule_3",
            "title": "Target Fisik & Keuangan Desember 100%",
            "passed": len(rule3_failed) == 0,
            "message": "Target fisik dan keuangan bulan Desember seluruh pekerjaan sudah 100%" if len(rule3_failed) == 0 else f"Ada {len(rule3_failed)} pekerjaan yang target Desember belum 100%",
            "items": rule3_failed
        }
    ]

    is_valid = (len(rule1_failed) == 0 and len(rule2_failed) == 0 and len(rule3_failed) == 0)

    return {
        "is_valid": is_valid,
        "checklist": checklist
    }


@router.post("/submit/{id_sub_pd}")
def submit_rko(
    id_sub_pd: int,
    tahun: int = Query(2026),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses untuk submit RKO OPD ini")

    validation = validate_rko_submission(id_sub_pd=id_sub_pd, tahun=tahun, db=db, current_user=current_user)
    if not validation["is_valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "RKO belum memenuhi syarat untuk disubmit",
                "checklist": validation["checklist"]
            }
        )

    submitter_name = (current_user.nama or current_user.username) if current_user and (getattr(current_user, 'nama', None) or getattr(current_user, 'username', None)) else "Operator OPD"

    sql = text("""
        INSERT INTO ta_rko_submission (id_sub_pd, tahun, status, submitted_at, submitted_by)
        VALUES (:id_sub_pd, :tahun, 'SUBMITTED', NOW(), :submitted_by)
        ON CONFLICT (id_sub_pd, tahun)
        DO UPDATE SET status = 'SUBMITTED', submitted_at = NOW(), submitted_by = :submitted_by, updated_at = NOW()
        RETURNING id_sub_pd, status, submitted_at, submitted_by
    """)
    row = db.execute(sql, {"id_sub_pd": id_sub_pd, "tahun": tahun, "submitted_by": submitter_name}).mappings().first()
    db.commit()

    return {
        "message": "RKO Berhasil Disubmit!",
        "submission": dict(row)
    }


class RejectPayload(BaseModel):
    notes: Optional[str] = None


@router.post("/approve/{id_sub_pd}")
def approve_rko(
    id_sub_pd: int,
    tahun: int = Query(2026),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hanya Admin BAPPEDA / Kota yang berhak menyetujui (Approve) RKO")

    approver_name = (current_user.nama or current_user.username) if current_user and (getattr(current_user, 'nama', None) or getattr(current_user, 'username', None)) else "Admin Bappeda"

    sql = text("""
        INSERT INTO ta_rko_submission (id_sub_pd, tahun, status, approved_at, approved_by)
        VALUES (:id_sub_pd, :tahun, 'APPROVED', NOW(), :approved_by)
        ON CONFLICT (id_sub_pd, tahun)
        DO UPDATE SET status = 'APPROVED', approved_at = NOW(), approved_by = :approved_by, updated_at = NOW()
        RETURNING id_sub_pd, status, approved_at, approved_by
    """)
    row = db.execute(sql, {"id_sub_pd": id_sub_pd, "tahun": tahun, "approved_by": approver_name}).mappings().first()
    db.commit()

    return {
        "message": "RKO Berhasil Disetujui (Approved)!",
        "submission": dict(row)
    }


@router.post("/reject/{id_sub_pd}")
def reject_or_unlock_rko(
    id_sub_pd: int,
    payload: Optional[RejectPayload] = None,
    tahun: int = Query(2026),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hanya Admin BAPPEDA / Kota yang berhak mengembalikan / membuka kuncian RKO")

    notes_val = payload.notes if payload and payload.notes else "Dikembalikan oleh Admin untuk revisi."

    sql = text("""
        INSERT INTO ta_rko_submission (id_sub_pd, tahun, status, notes)
        VALUES (:id_sub_pd, :tahun, 'DRAFT', :notes)
        ON CONFLICT (id_sub_pd, tahun)
        DO UPDATE SET status = 'DRAFT', notes = :notes, updated_at = NOW()
        RETURNING id_sub_pd, status, notes
    """)
    row = db.execute(sql, {"id_sub_pd": id_sub_pd, "tahun": tahun, "notes": notes_val}).mappings().first()
    db.commit()

    return {
        "message": "Kuncian RKO Berhasil Dibuka (Dikembalikan ke Status DRAFT)",
        "submission": dict(row)
    }


@router.get("/personel-options/{id_sub_pd}")
def get_personel_options_for_rko(id_sub_pd: int, db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT id, nip, nama, jabatan, pangkat, golongan
            FROM ta_personel
            WHERE id_sub_pd = :id_sub_pd
            ORDER BY nama ASC
        """)
        rows = db.execute(sql, {"id_sub_pd": id_sub_pd}).mappings().all()

        if not rows:
            sql_all = text("""
                SELECT id, nip, nama, jabatan, pangkat, golongan
                FROM ta_personel
                ORDER BY nama ASC
            """)
            rows = db.execute(sql_all).mappings().all()

        return [dict(r) for r in rows]
    except Exception as e:
        print("Error fetching personel options for RKO:", e)
        return []


@router.get("/ref-sumberdana")
def get_ref_sumberdana(db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT id_dana, kode_dana, nama_dana, sumber_dana, set_input
            FROM ref_sumberdana
            ORDER BY kode_dana ASC
        """)
        rows = db.execute(sql).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        print("Error fetching ref_sumberdana:", e)
        return []


@router.get("/pokir-options")
def get_pokir_options(
    q: Optional[str] = Query(None, description="Search by nama_kamus, usulan, or nama_pengusul"),
    tahun: Optional[int] = Query(2026, description="Tahun"),
    db: Session = Depends(get_db)
):
    try:
        where_clauses = ["(tahun = :tahun OR :tahun IS NULL)"]
        params = {"tahun": tahun}
        
        if q and q.strip():
            where_clauses.append("(nama_kamus ILIKE :q OR usulan ILIKE :q OR nama_pengusul ILIKE :q OR alamat_teks ILIKE :q)")
            params["q"] = f"%{q.strip()}%"
            
        where_sql = "WHERE " + " AND ".join(where_clauses)
        
        sql = text(f"""
            SELECT id_usulan, nama_kamus, usulan, nama_pengusul, alamat_teks, tahun, anggaran, volume, satuan, nama_skpd_awal
            FROM ta_pokir
            {where_sql}
            ORDER BY nama_pengusul ASC, id_usulan DESC
            LIMIT 500
        """)
        rows = db.execute(sql, params).mappings().all()
        results = []
        for r in rows:
            d = dict(r)
            d["anggaran"] = float(d["anggaran"] or 0)
            results.append(d)
        return results
    except Exception as e:
        print("Error fetching pokir options:", e)
        return []


@router.get("/musrenbang-options")
def get_musrenbang_options(
    q: Optional[str] = Query(None, description="Search by nama_kamus, usulan, nama_pengusul, or alamat_teks"),
    tahun: Optional[int] = Query(2026, description="Tahun"),
    db: Session = Depends(get_db)
):
    try:
        where_clauses = ["(tahun = :tahun OR :tahun IS NULL)"]
        params = {"tahun": tahun}
        
        if q and q.strip():
            where_clauses.append("(nama_kamus ILIKE :q OR usulan ILIKE :q OR nama_pengusul ILIKE :q OR alamat_teks ILIKE :q)")
            params["q"] = f"%{q.strip()}%"
            
        where_sql = "WHERE " + " AND ".join(where_clauses)
        
        sql = text(f"""
            SELECT id_usulan, nama_kamus, usulan, nama_pengusul, alamat_teks, tahun, anggaran, volume, satuan, nama_skpd_awal, lurah_teks, camat_teks
            FROM ta_musrenbang
            {where_sql}
            ORDER BY nama_pengusul ASC, id_usulan DESC
            LIMIT 500
        """)
        rows = db.execute(sql, params).mappings().all()
        results = []
        for r in rows:
            d = dict(r)
            d["anggaran"] = float(d["anggaran"] or 0)
            results.append(d)
        return results
    except Exception as e:
        print("Error fetching musrenbang options:", e)
        return []


@router.get("/dak-options")
def get_dak_options(
    id_sub_pd: Optional[int] = Query(None, description="Filter by id_sub_pd"),
    q: Optional[str] = Query(None, description="Search term"),
    tahun: Optional[int] = Query(2026, description="Tahun"),
    db: Session = Depends(get_db)
):
    try:
        where_clauses = ["(tahun = :tahun OR :tahun IS NULL)"]
        params = {"tahun": tahun}
        
        if id_sub_pd:
            where_clauses.append("(id_sub_pd = :id_sub_pd OR id_sub_pd IS NULL)")
            params["id_sub_pd"] = id_sub_pd

        if q and q.strip():
            where_clauses.append("""(
                t1_nama ILIKE :q OR t2_nama ILIKE :q OR t3_nama ILIKE :q OR 
                t4_nama ILIKE :q OR t5_nama ILIKE :q OR jenis ILIKE :q
            )""")
            params["q"] = f"%{q.strip()}%"
            
        where_sql = "WHERE " + " AND ".join(where_clauses)
        
        sql = text(f"""
            SELECT id, id_sub_pd, jenis, 
                   t1_kode, t1_nama, 
                   t2_kode, t2_nama, 
                   t3_kode, t3_nama, 
                   t4_kode, t4_nama, 
                   t5_kode, t5_nama 
            FROM dak_detail_rincian
            {where_sql}
            ORDER BY id_sub_pd ASC, t1_nama ASC, id ASC
            LIMIT 500
        """)
        rows = db.execute(sql, params).mappings().all()
        results = []
        for r in rows:
            d = dict(r)
            d["t1_nama"] = (d["t1_nama"] or "").strip()
            d["t2_nama"] = (d["t2_nama"] or "").strip()
            d["t3_nama"] = (d["t3_nama"] or "").strip()
            d["t4_nama"] = (d["t4_nama"] or "").strip()
            d["t5_nama"] = (d["t5_nama"] or "").strip()
            parts = [p for p in [d["t1_nama"], d["t2_nama"], d["t3_nama"], d["t4_nama"], d["t5_nama"]] if p]
            d["nama_full"] = " > ".join(parts)
            results.append(d)
        return results
    except Exception as e:
        print("Error fetching dak options:", e)
        return []



