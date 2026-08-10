import html
import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.deps import get_current_user_from_jwt, CurrentUser
from app.core.config import settings
from datetime import datetime

router = APIRouter()

MONTH_NAMES_IND = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
MONTH_FULL_IND = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']


class BuatLaporanRFKSchema(BaseModel):
    id_sub_pd: int
    tahun: Optional[int] = 2026


class SimpanRealisasiPekerjaanSchema(BaseModel):
    id_pekerjaan: str
    id_sub_pd: int
    bulan: int
    keuangan: float
    fisik: float
    masalah: Optional[str] = None
    upaya: Optional[str] = None


class SimpanKontrakSchema(BaseModel):
    id_pekerjaan: str
    nama_ppk: Optional[str] = None
    nama_pptk: Optional[str] = None
    nama_pokja: Optional[str] = None
    nama_pphp: Optional[str] = None
    nilai_hps: Optional[float] = 0
    nilai_kontrak: Optional[float] = 0
    sisa_anggaran: Optional[float] = 0
    nama_penyedia: Optional[str] = None
    alamat_penyedia: Optional[str] = None
    pimpinan_penyedia: Optional[str] = None
    npwp_penyedia: Optional[str] = None
    nomor_kontrak: Optional[str] = None
    tgl_kontrak_awal: Optional[str] = None
    tgl_kontrak_akhir: Optional[str] = None
    nomor_spmk: Optional[str] = None
    tgl_spmk_awal: Optional[str] = None
    tgl_spmk_akhir: Optional[str] = None
    tgl_adendum_awal: Optional[str] = None
    tgl_adendum_akhir: Optional[str] = None
    status_kontrak: Optional[str] = 'Dalam Proses'


def clean_text(text_val):
    if not text_val:
        return text_val
    return html.unescape(str(text_val)).strip()

def format_tgl_bulan(dt):
    if not dt:
        return None
    day = dt.day
    month_name = MONTH_NAMES_IND[dt.month]
    return f"{day:02d} {month_name}"

def format_tgl_full(dt):
    if not dt:
        return None
    day = dt.day
    month_name = MONTH_NAMES_IND[dt.month]
    year = dt.year
    time_str = dt.strftime("%H:%M")
    return f"{day:02d} {month_name} {year} {time_str}"


@router.get("/opd-laporan")
def get_rfk_opd_laporan(
    q: Optional[str] = Query(None, description="Cari nama OPD atau kode"),
    is_pd: Optional[int] = Query(None, description="Filter 1=PD Utama, 0=Sub PD/Sekolah/Kelurahan"),
    tahun: Optional[int] = Query(2026, description="Tahun"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        where_clauses = ["o.aktif = 1", "o.kode != '0.00.0.00.000'"]
        params = {"tahun": tahun}

        if is_pd is not None:
            if is_pd == 1:
                where_clauses.append("o.is_pd = 1")
            elif is_pd == 0:
                where_clauses.append("(o.is_pd = 0 OR o.is_pd IS NULL)")

        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if current_user.id_opds and len(current_user.id_opds) > 0:
                where_clauses.append("o.id_sub_pd = ANY(:id_opds)")
                params["id_opds"] = current_user.id_opds
            else:
                return {"summary": {}, "opd_list": []}

        if q and q.strip():
            where_clauses.append("(o.nama_pd ILIKE :q OR o.kode ILIKE :q OR o.nama_pd_singkat ILIKE :q)")
            params["q"] = f"%{q.strip()}%"

        where_sql = "WHERE " + " AND ".join(where_clauses)

        opd_sql = text(f"""
            SELECT 
                o.id_sub_pd,
                o.id_pd,
                o.kode,
                o.nama_pd,
                o.nama_pd_singkat,
                o.is_pd,
                o.aktif,
                COALESCE(sub.status, 'DRAFT') AS status_rko
            FROM ta_opd o
            LEFT JOIN ta_rko_submission sub ON o.id_sub_pd = sub.id_sub_pd AND (sub.tahun = :tahun OR :tahun IS NULL)
            {where_sql}
            ORDER BY o.kode ASC
        """)
        opd_rows = db.execute(opd_sql, params).mappings().all()

        if not opd_rows:
            return {
                "summary": {
                    "total_opd": 0,
                    "total_laporan_terkirim": 0,
                    "bulan_terkirim": {m: 0 for m in range(1, 13)}
                },
                "opd_list": []
            }

        opd_ids = [r["id_sub_pd"] for r in opd_rows]

        rfk_sql = text("""
            SELECT 
                id,
                id_sub_pd,
                bulan,
                str_bulan,
                tgl_buat,
                tgl_kirim,
                tgl_verify,
                lock,
                user_buat,
                user_kirim,
                verified,
                user_verify,
                kd_perubahan
            FROM ta_laporan_rfk
            WHERE id_sub_pd = ANY(:opd_ids)
              AND (EXTRACT(YEAR FROM COALESCE(tgl_kirim, tgl_buat)) = :tahun OR :tahun IS NULL)
            ORDER BY id_sub_pd ASC, bulan DESC
        """)
        rfk_rows = db.execute(rfk_sql, {"opd_ids": opd_ids, "tahun": tahun}).mappings().all()

        rfk_map = {}
        total_laporan_terkirim = 0
        bulan_terkirim_count = {m: 0 for m in range(1, 13)}

        for r in rfk_rows:
            key = (r["id_sub_pd"], r["bulan"])
            rfk_map[key] = dict(r)

        opd_list = []
        for o in opd_rows:
            opd_id = o["id_sub_pd"]
            laporan_bulanan = {}
            total_sent_opd = 0
            max_created_bulan = 0

            for m in range(1, 13):
                rep = rfk_map.get((opd_id, m))
                if rep:
                    max_created_bulan = max(max_created_bulan, m)
                    tgl_kirim_dt = rep.get("tgl_kirim")
                    tgl_kirim_fmt = format_tgl_bulan(tgl_kirim_dt)
                    if tgl_kirim_fmt:
                        total_sent_opd += 1
                        total_laporan_terkirim += 1
                        bulan_terkirim_count[m] += 1

                    laporan_bulanan[str(m)] = {
                        "id": rep["id"],
                        "bulan": m,
                        "str_bulan": rep["str_bulan"] or MONTH_FULL_IND[m],
                        "tgl_kirim_fmt": tgl_kirim_fmt,
                        "tgl_buat_fmt": format_tgl_full(rep.get("tgl_buat")),
                        "tgl_kirim_full": format_tgl_full(tgl_kirim_dt),
                        "tgl_verify_fmt": format_tgl_full(rep.get("tgl_verify")),
                        "lock": rep.get("lock") or 0,
                        "user_buat": clean_text(rep.get("user_buat")),
                        "user_kirim": clean_text(rep.get("user_kirim")),
                        "verified": rep.get("verified") or 0,
                        "user_verify": clean_text(rep.get("user_verify")),
                        "kd_perubahan": rep.get("kd_perubahan")
                    }
                else:
                    laporan_bulanan[str(m)] = None

            opd_list.append({
                "id_sub_pd": o["id_sub_pd"],
                "id_pd": o["id_pd"],
                "kode": o["kode"],
                "nama_pd": clean_text(o["nama_pd"]),
                "nama_pd_singkat": clean_text(o["nama_pd_singkat"]),
                "is_pd": o["is_pd"],
                "status_rko": o["status_rko"],
                "total_laporan_terkirim": total_sent_opd,
                "max_created_bulan": max_created_bulan,
                "laporan_bulanan": laporan_bulanan
            })

        summary = {
            "total_opd": len(opd_rows),
            "total_laporan_terkirim": total_laporan_terkirim,
            "bulan_terkirim": bulan_terkirim_count
        }

        return {
            "summary": summary,
            "opd_list": opd_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/laporan/buat")
def buat_laporan_rfk(
    payload: BuatLaporanRFKSchema,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        id_sub_pd = payload.id_sub_pd
        tahun = payload.tahun or 2026

        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if not current_user.id_opds or id_sub_pd not in current_user.id_opds:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke Perangkat Daerah ini")

        # 1. Validation Rule: RKO must be APPROVED by Admin
        rko_sql = text("SELECT status FROM ta_rko_submission WHERE id_sub_pd = :id_sub_pd AND (tahun = :tahun OR :tahun IS NULL)")
        rko_row = db.execute(rko_sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().first()
        status_rko = rko_row["status"] if rko_row else "DRAFT"

        if status_rko != "APPROVED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Laporan RFK tidak dapat dibuat karena RKO Perangkat Daerah belum disetujui (APPROVED) oleh Admin. Status RKO: {status_rko}."
            )

        # Query existing reports for this OPD
        existing_sql = text("""
            SELECT bulan, tgl_kirim
            FROM ta_laporan_rfk
            WHERE id_sub_pd = :id_sub_pd
              AND (EXTRACT(YEAR FROM COALESCE(tgl_kirim, tgl_buat)) = :tahun OR :tahun IS NULL)
            ORDER BY bulan ASC
        """)
        existing_rows = db.execute(existing_sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()

        existing_map = {r["bulan"]: r for r in existing_rows}
        existing_months = set(existing_map.keys())

        if not existing_months:
            next_month = 1
        else:
            max_m = max(existing_months)
            next_month = max_m + 1

        if next_month > 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Seluruh Laporan RFK bulanan (Januari - Desember) untuk tahun ini telah dibuat."
            )

        # 2. Validation Rule: Previous month must be sent
        if next_month > 1:
            prev_m = next_month - 1
            prev_rep = existing_map.get(prev_m)
            if not prev_rep or not prev_rep["tgl_kirim"]:
                prev_month_name = MONTH_FULL_IND[prev_m]
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Laporan RFK bulan {MONTH_FULL_IND[next_month]} tidak dapat dibuat karena Laporan RFK bulan sebelumnya ({prev_month_name}) belum dikirim."
                )

        user_name = current_user.name if (current_user and current_user.name) else (current_user.username if current_user else "System")
        str_bulan = MONTH_FULL_IND[next_month]

        insert_sql = text("""
            INSERT INTO ta_laporan_rfk (
                id_sub_pd, bulan, str_bulan, tgl_buat, lock, user_buat, verified, kd_perubahan
            ) VALUES (
                :id_sub_pd, :bulan, :str_bulan, NOW(), 0, :user_buat, 0, 1
            )
            RETURNING id, id_sub_pd, bulan, str_bulan, tgl_buat, user_buat
        """)
        new_row = db.execute(insert_sql, {
            "id_sub_pd": id_sub_pd,
            "bulan": next_month,
            "str_bulan": str_bulan,
            "user_buat": user_name
        }).mappings().first()

        # Populate / copy ta_pekerjaan_realisasi entries for the newly created month
        pekerjaan_sql = text("SELECT id FROM ta_pekerjaan WHERE id_sub_pd = :id_sub_pd")
        pek_rows = db.execute(pekerjaan_sql, {"id_sub_pd": id_sub_pd}).mappings().all()

        for pek in pek_rows:
            pek_id = pek["id"]
            
            prev_sql = text("""
                SELECT SUM(COALESCE(keuangan, 0)) AS tot_keu_lalu, MAX(COALESCE(fisik, 0)) AS max_fisik_lalu
                FROM ta_pekerjaan_realisasi
                WHERE id_pekerjaan = :id_pekerjaan AND bulan < :next_month
            """)
            prev_res = db.execute(prev_sql, {"id_pekerjaan": pek_id, "next_month": next_month}).mappings().first()
            keuangan_lalu = float(prev_res["tot_keu_lalu"] or 0) if (prev_res and prev_res["tot_keu_lalu"] is not None) else 0.0
            fisik_lalu = float(prev_res["max_fisik_lalu"] or 0) if (prev_res and prev_res["max_fisik_lalu"] is not None) else 0.0

            initial_fisik = fisik_lalu

            chk_real_sql = text("SELECT id FROM ta_pekerjaan_realisasi WHERE id_pekerjaan = :id_pekerjaan AND bulan = :bulan")
            chk_row = db.execute(chk_real_sql, {"id_pekerjaan": pek_id, "bulan": next_month}).mappings().first()

            if not chk_row:
                ins_real_sql = text("""
                    INSERT INTO ta_pekerjaan_realisasi (
                        id, id_sub_pd, id_pekerjaan, bulan, keuangan, fisik, keuangan_lalu, fisik_lalu
                    ) VALUES (
                        gen_random_uuid(), :id_sub_pd, :id_pekerjaan, :bulan, 0, :fisik, :keuangan_lalu, :fisik_lalu
                    )
                """)
                db.execute(ins_real_sql, {
                    "id_sub_pd": id_sub_pd,
                    "id_pekerjaan": pek_id,
                    "bulan": next_month,
                    "fisik": initial_fisik,
                    "keuangan_lalu": keuangan_lalu,
                    "fisik_lalu": fisik_lalu
                })
            else:
                upd_real_sql = text("""
                    UPDATE ta_pekerjaan_realisasi
                    SET keuangan_lalu = :keuangan_lalu,
                        fisik_lalu = :fisik_lalu,
                        fisik = GREATEST(COALESCE(fisik, 0), :fisik_lalu)
                    WHERE id_pekerjaan = :id_pekerjaan AND bulan = :bulan
                """)
                db.execute(upd_real_sql, {
                    "id_pekerjaan": pek_id,
                    "bulan": next_month,
                    "keuangan_lalu": keuangan_lalu,
                    "fisik_lalu": fisik_lalu
                })

        db.commit()

        return {
            "message": f"Berhasil membuat Draf Laporan RFK bulan {str_bulan} {tahun}",
            "laporan": dict(new_row)
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Gagal membuat Laporan RFK: {str(e)}")


@router.get("/laporan-detail/{id_sub_pd}/{bulan}")
def get_rfk_laporan_bulanan_detail(
    id_sub_pd: int,
    bulan: int,
    tahun: Optional[int] = Query(2026, description="Tahun Anggaran"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke Perangkat Daerah ini")

    try:
        opd_sql = text("SELECT id_sub_pd, kode, nama_pd, nama_pd_singkat FROM ta_opd WHERE id_sub_pd = :id_sub_pd")
        opd_row = db.execute(opd_sql, {"id_sub_pd": id_sub_pd}).mappings().first()
        if not opd_row:
            raise HTTPException(status_code=404, detail="Perangkat Daerah tidak ditemukan")

        rfk_sql = text("""
            SELECT id, bulan, str_bulan, tgl_buat, tgl_kirim, tgl_verify, lock, user_buat, user_kirim, verified, user_verify
            FROM ta_laporan_rfk
            WHERE id_sub_pd = :id_sub_pd AND bulan = :bulan
        """)
        rfk_row = db.execute(rfk_sql, {"id_sub_pd": id_sub_pd, "bulan": bulan}).mappings().first()
        rfk_dict = dict(rfk_row) if rfk_row else None
        if rfk_dict:
            rfk_dict["tgl_buat_fmt"] = format_tgl_full(rfk_dict.get("tgl_buat"))
            rfk_dict["tgl_kirim_full"] = format_tgl_full(rfk_dict.get("tgl_kirim"))
            rfk_dict["tgl_verify_fmt"] = format_tgl_full(rfk_dict.get("tgl_verify"))
            rfk_dict["user_buat"] = clean_text(rfk_dict.get("user_buat"))
            rfk_dict["user_kirim"] = clean_text(rfk_dict.get("user_kirim"))
            rfk_dict["user_verify"] = clean_text(rfk_dict.get("user_verify"))

        tree_sql = text("""
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
                p.nomor_pekerjaan,
                p.nama_pekerjaan,
                COALESCE(p.pagu_anggaran, 0) AS pagu_anggaran
            FROM renja_subkegiatan s
            LEFT JOIN ta_pekerjaan p ON s.id_sub_pd = p.id_sub_pd AND s.idsubkegiatan = p.id_subkegiatan
            WHERE s.id_sub_pd = :id_sub_pd AND (s.tahun = :tahun OR :tahun IS NULL)
            ORDER BY s.kode_program ASC, s.kode_kegiatan ASC, s.kode_sub_kegiatan ASC, p.id ASC
        """)
        tree_rows = db.execute(tree_sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()

        realisasi_sql = text("""
            SELECT id_pekerjaan, bulan, COALESCE(keuangan, 0) AS keuangan, COALESCE(fisik, 0) AS fisik
            FROM ta_pekerjaan_realisasi
            WHERE id_sub_pd = :id_sub_pd
        """)
        realisasi_rows = db.execute(realisasi_sql, {"id_sub_pd": id_sub_pd}).mappings().all()

        pek_real_map = {}
        for r in realisasi_rows:
            pek_id_str = str(r["id_pekerjaan"])
            m_val = r["bulan"]
            pek_real_map[(pek_id_str, m_val)] = {
                "keuangan": float(r["keuangan"] or 0),
                "fisik": float(r["fisik"] or 0)
            }

        programs_dict = {}
        subkegiatan_seen = set()

        for r in tree_rows:
            kd_prog = r["kode_program"] or "0.00"
            nm_prog = r["nm_program"] or "Program Tanpa Nama"
            kd_keg = r["kode_kegiatan"] or "0.00.00"
            nm_keg = r["nm_kegiatan"] or "Kegiatan Tanpa Nama"
            id_sub_uuid = str(r["idsubkegiatan"]) if r["idsubkegiatan"] else ""
            kd_sub = r["kode_sub_kegiatan"] or "0.00.00.0000"
            nm_sub = r["nm_sub_kegiatan"] or "Subkegiatan Tanpa Nama"
            anggaran_renja = float(r["anggaran_renja"] or 0)
            pagu_pek = float(r["pagu_anggaran"] or 0)

            if kd_prog not in programs_dict:
                programs_dict[kd_prog] = {
                    "kode": kd_prog,
                    "nama": nm_prog,
                    "anggaran": 0.0,
                    "kegiatan_dict": {}
                }

            prog = programs_dict[kd_prog]

            if kd_keg not in prog["kegiatan_dict"]:
                prog["kegiatan_dict"][kd_keg] = {
                    "kode": kd_keg,
                    "nama": nm_keg,
                    "anggaran": 0.0,
                    "subkegiatan_dict": {}
                }

            keg = prog["kegiatan_dict"][kd_keg]

            if kd_sub not in keg["subkegiatan_dict"]:
                keg["subkegiatan_dict"][kd_sub] = {
                    "idsubkegiatan": id_sub_uuid,
                    "kode": kd_sub,
                    "nama": nm_sub,
                    "anggaran": anggaran_renja,
                    "pekerjaan": []
                }
                keg["anggaran"] += anggaran_renja
                prog["anggaran"] += anggaran_renja
                subkegiatan_seen.add(kd_sub)

            sub = keg["subkegiatan_dict"][kd_sub]

            if r["id_pekerjaan"]:
                pek_id_str = str(r["id_pekerjaan"])
                keuangan_per_bulan = [0.0] * 12
                fisik_per_bulan = [0.0] * 12
                keuangan_sd_selected = 0.0
                keuangan_sipd = 0.0
                fisik_selected = 0.0
                keuangan_selected = 0.0

                for m_idx in range(1, 13):
                    entry = pek_real_map.get((pek_id_str, m_idx))
                    if entry:
                        k_val = entry["keuangan"]
                        f_val = entry["fisik"]
                        keuangan_per_bulan[m_idx - 1] = k_val
                        fisik_per_bulan[m_idx - 1] = f_val
                        keuangan_sipd += k_val
                        if m_idx <= bulan:
                            keuangan_sd_selected += k_val
                        if m_idx == bulan:
                            keuangan_selected = k_val
                            fisik_selected = f_val

                sub["pekerjaan"].append({
                    "id": pek_id_str,
                    "nomor_pekerjaan": r["nomor_pekerjaan"],
                    "nama_pekerjaan": clean_text(r["nama_pekerjaan"]),
                    "anggaran": pagu_pek,
                    "realisasi_fisik": round(fisik_selected, 2),
                    "keuangan_bulan_ini": round(keuangan_selected, 2),
                    "keuangan_total_sd_bulan_ini": round(keuangan_sd_selected, 2),
                    "keuangan_total_sipd": round(keuangan_sipd, 2),
                    "keuangan_per_bulan": [round(x, 2) for x in keuangan_per_bulan]
                })

        def rollup_items(children, get_anggaran, get_fisik, get_keu_bln, get_keu_sd, get_keu_sipd, get_keu_list):
            tot_anggaran = sum(get_anggaran(c) for c in children)
            tot_bln = sum(get_keu_bln(c) for c in children)
            tot_sd = sum(get_keu_sd(c) for c in children)
            tot_sipd = sum(get_keu_sipd(c) for c in children)
            tot_list = [sum(get_keu_list(c)[m] for c in children) for m in range(12)]
            
            if tot_anggaran > 0:
                tot_fisik = sum(get_anggaran(c) * get_fisik(c) for c in children) / tot_anggaran
            elif len(children) > 0:
                tot_fisik = sum(get_fisik(c) for c in children) / len(children)
            else:
                tot_fisik = 0.0

            return round(tot_anggaran, 2), round(tot_fisik, 2), round(tot_bln, 2), round(tot_sd, 2), round(tot_sipd, 2), [round(x, 2) for x in tot_list]

        programs_list = []
        for prog in programs_dict.values():
            kegiatan_list = []
            for keg in prog["kegiatan_dict"].values():
                subkegiatan_list = []
                for sub in keg["subkegiatan_dict"].values():
                    if sub["pekerjaan"]:
                        s_ang, s_fis, s_bln, s_sd, s_sipd, s_list = rollup_items(
                            sub["pekerjaan"],
                            lambda x: x["anggaran"],
                            lambda x: x["realisasi_fisik"],
                            lambda x: x["keuangan_bulan_ini"],
                            lambda x: x["keuangan_total_sd_bulan_ini"],
                            lambda x: x["keuangan_total_sipd"],
                            lambda x: x["keuangan_per_bulan"]
                        )
                    else:
                        s_ang, s_fis, s_bln, s_sd, s_sipd, s_list = sub["anggaran"], 0.0, 0.0, 0.0, 0.0, [0.0]*12

                    subkegiatan_list.append({
                        "idsubkegiatan": sub["idsubkegiatan"],
                        "kode": sub["kode"],
                        "nama": sub["nama"],
                        "anggaran": s_ang,
                        "realisasi_fisik": s_fis,
                        "keuangan_bulan_ini": s_bln,
                        "keuangan_total_sd_bulan_ini": s_sd,
                        "keuangan_total_sipd": s_sipd,
                        "keuangan_per_bulan": s_list,
                        "pekerjaan": sub["pekerjaan"]
                    })

                k_ang, k_fis, k_bln, k_sd, k_sipd, k_list = rollup_items(
                    subkegiatan_list,
                    lambda x: x["anggaran"],
                    lambda x: x["realisasi_fisik"],
                    lambda x: x["keuangan_bulan_ini"],
                    lambda x: x["keuangan_total_sd_bulan_ini"],
                    lambda x: x["keuangan_total_sipd"],
                    lambda x: x["keuangan_per_bulan"]
                )
                kegiatan_list.append({
                    "kode": keg["kode"],
                    "nama": keg["nama"],
                    "anggaran": k_ang,
                    "realisasi_fisik": k_fis,
                    "keuangan_bulan_ini": k_bln,
                    "keuangan_total_sd_bulan_ini": k_sd,
                    "keuangan_total_sipd": k_sipd,
                    "keuangan_per_bulan": k_list,
                    "subkegiatan": subkegiatan_list
                })

            p_ang, p_fis, p_bln, p_sd, p_sipd, p_list = rollup_items(
                kegiatan_list,
                lambda x: x["anggaran"],
                lambda x: x["realisasi_fisik"],
                lambda x: x["keuangan_bulan_ini"],
                lambda x: x["keuangan_total_sd_bulan_ini"],
                lambda x: x["keuangan_total_sipd"],
                lambda x: x["keuangan_per_bulan"]
            )
            programs_list.append({
                "kode": prog["kode"],
                "nama": prog["nama"],
                "anggaran": p_ang,
                "realisasi_fisik": p_fis,
                "keuangan_bulan_ini": p_bln,
                "keuangan_total_sd_bulan_ini": p_sd,
                "keuangan_total_sipd": p_sipd,
                "keuangan_per_bulan": p_list,
                "kegiatan": kegiatan_list
            })

        return {
            "opd": dict(opd_row),
            "bulan": bulan,
            "str_bulan": MONTH_FULL_IND[bulan] if 1 <= bulan <= 12 else str(bulan),
            "tahun": tahun,
            "laporan_rfk": rfk_dict,
            "programs": programs_list
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memuat detail laporan RFK: {str(e)}")


@router.delete("/laporan/{id_sub_pd}/{bulan}")
def delete_laporan_rfk(
    id_sub_pd: int,
    bulan: int,
    tahun: Optional[int] = Query(2026, description="Tahun Anggaran"),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya Admin yang berhak menghapus Laporan RFK Perangkat Daerah"
        )

    try:
        months_sql = text("""
            SELECT bulan, str_bulan 
            FROM ta_laporan_rfk 
            WHERE id_sub_pd = :id_sub_pd 
              AND (EXTRACT(YEAR FROM COALESCE(tgl_kirim, tgl_buat)) = :tahun OR :tahun IS NULL)
        """)
        m_rows = db.execute(months_sql, {"id_sub_pd": id_sub_pd, "tahun": tahun}).mappings().all()
        existing_m_list = [r["bulan"] for r in m_rows]

        if not existing_m_list or bulan not in existing_m_list:
            raise HTTPException(status_code=404, detail="Laporan RFK bulan ini tidak ditemukan")

        max_m = max(existing_m_list)
        if bulan != max_m:
            max_m_name = MONTH_FULL_IND[max_m] if 1 <= max_m <= 12 else str(max_m)
            target_m_name = MONTH_FULL_IND[bulan] if 1 <= bulan <= 12 else str(bulan)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Laporan RFK bulan {target_m_name} tidak dapat dihapus. Penghapusan harus berurutan mulai dari bulan terbaru ({max_m_name})."
            )

        row_map = {r["bulan"]: r for r in m_rows}
        str_bln = row_map[bulan]["str_bulan"] or (MONTH_FULL_IND[bulan] if 1 <= bulan <= 12 else str(bulan))

        del_sql = text("DELETE FROM ta_laporan_rfk WHERE id_sub_pd = :id_sub_pd AND bulan = :bulan")
        db.execute(del_sql, {"id_sub_pd": id_sub_pd, "bulan": bulan})
        db.commit()

        return {
            "message": f"Berhasil menghapus Laporan RFK bulan {str_bln} {tahun}"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menghapus Laporan RFK: {str(e)}")


@router.get("/realisasi/{id_pekerjaan}/{bulan}")
def get_pekerjaan_realisasi_detail(
    id_pekerjaan: str,
    bulan: int,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        pek_sql = text("""
            SELECT p.id, p.id_sub_pd, p.nomor_pekerjaan, p.nama_pekerjaan, COALESCE(p.pagu_anggaran, 0) AS pagu_anggaran,
                   p.jan_f, p.feb_f, p.mar_f, p.apr_f, p.mei_f, p.jun_f, p.jul_f, p.agu_f, p.sep_f, p.okt_f, p.nov_f, p.des_f,
                   p.tg1, p.tg2, p.tg3, p.tg4, p.tg5, p.sumber_dana, p.lokasi,
                   o.nama_pd, o.kode AS kode_opd
            FROM ta_pekerjaan p
            JOIN ta_opd o ON p.id_sub_pd = o.id_sub_pd
            WHERE p.id = :id_pekerjaan
        """)
        pek_row = db.execute(pek_sql, {"id_pekerjaan": id_pekerjaan}).mappings().first()
        if not pek_row:
            raise HTTPException(status_code=404, detail="Pekerjaan tidak ditemukan")

        pek_dict = dict(pek_row)
        pek_dict["id"] = str(pek_dict["id"])
        pek_dict["nama_pekerjaan"] = clean_text(pek_dict["nama_pekerjaan"])
        pek_dict["nama_pd"] = clean_text(pek_dict["nama_pd"])
        pek_dict["lokasi"] = clean_text(pek_dict.get("lokasi"))

        # Fetch locations list from ta_pekerjaan_lokasi
        loc_sql = text("""
            SELECT id, id_pekerjaan, nama_lokasi, jenis_geometry, geojson, lat, lng, radius
            FROM ta_pekerjaan_lokasi
            WHERE id_pekerjaan = :id_pekerjaan
        """)
        loc_rows = db.execute(loc_sql, {"id_pekerjaan": id_pekerjaan}).mappings().all()
        lokasi_list = []
        for lr in loc_rows:
            l_dict = dict(lr)
            l_dict["id"] = str(l_dict["id"])
            l_dict["id_pekerjaan"] = str(l_dict["id_pekerjaan"])
            l_dict["nama_lokasi"] = clean_text(l_dict["nama_lokasi"])
            if l_dict.get("lat") is not None:
                l_dict["lat"] = float(l_dict["lat"])
            if l_dict.get("lng") is not None:
                l_dict["lng"] = float(l_dict["lng"])
            if l_dict.get("radius") is not None:
                l_dict["radius"] = float(l_dict["radius"])
            lokasi_list.append(l_dict)

        # Determine target_fisik_bulan_ini for requested month (1..12)
        target_cols = ['jan_f', 'feb_f', 'mar_f', 'apr_f', 'mei_f', 'jun_f', 'jul_f', 'agu_f', 'sep_f', 'okt_f', 'nov_f', 'des_f']
        target_col = target_cols[bulan - 1] if 1 <= bulan <= 12 else 'jan_f'
        target_fisik_bulan_ini = float(pek_dict.get(target_col) or 0)

        # Collect tagging badges
        tagging_list = []
        for tg_key in ['tg1', 'tg2', 'tg3', 'tg4', 'tg5', 'sumber_dana']:
            t_val = clean_text(pek_dict.get(tg_key))
            if t_val and t_val not in tagging_list:
                tagging_list.append(t_val)

        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if not current_user.id_opds or pek_dict["id_sub_pd"] not in current_user.id_opds:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke Perangkat Daerah ini")

        real_sql = text("""
            SELECT id, id_sub_pd, id_pekerjaan, bulan, COALESCE(keuangan, 0) AS keuangan, COALESCE(fisik, 0) AS fisik,
                   masalah, upaya, COALESCE(keuangan_lalu, 0) AS keuangan_lalu, COALESCE(fisik_lalu, 0) AS fisik_lalu
            FROM ta_pekerjaan_realisasi
            WHERE id_pekerjaan = :id_pekerjaan AND bulan = :bulan
        """)
        real_row = db.execute(real_sql, {"id_pekerjaan": id_pekerjaan, "bulan": bulan}).mappings().first()
        real_dict = dict(real_row) if real_row else None
        if real_dict:
            real_dict["id"] = str(real_dict["id"])
            real_dict["id_pekerjaan"] = str(real_dict["id_pekerjaan"])
            real_dict["keuangan"] = float(real_dict["keuangan"] or 0)
            real_dict["fisik"] = float(real_dict["fisik"] or 0)
            real_dict["masalah"] = clean_text(real_dict["masalah"])
            real_dict["upaya"] = clean_text(real_dict["upaya"])

        prev_sql = text("""
            SELECT SUM(COALESCE(keuangan, 0)) AS tot_keu_lalu, MAX(COALESCE(fisik, 0)) AS max_fisik_lalu
            FROM ta_pekerjaan_realisasi
            WHERE id_pekerjaan = :id_pekerjaan AND bulan < :bulan
        """)
        prev_row = db.execute(prev_sql, {"id_pekerjaan": id_pekerjaan, "bulan": bulan}).mappings().first()
        keuangan_lalu = float(prev_row["tot_keu_lalu"] or 0) if (prev_row and prev_row["tot_keu_lalu"] is not None) else 0.0
        fisik_lalu = float(prev_row["max_fisik_lalu"] or 0) if (prev_row and prev_row["max_fisik_lalu"] is not None) else 0.0

        if real_dict and real_dict.get("fisik_lalu"):
            fisik_lalu = float(real_dict["fisik_lalu"])

        # Fetch contract info from ta_pekerjaan_kontrak
        kontrak_dict = None
        try:
            kontrak_sql = text("""
                SELECT id, id_pekerjaan, nama_ppk, nama_pptk, nama_pokja, nama_pphp,
                       COALESCE(nilai_hps, 0) AS nilai_hps, COALESCE(nilai_kontrak, 0) AS nilai_kontrak, COALESCE(sisa_anggaran, 0) AS sisa_anggaran,
                       nama_penyedia, alamat_penyedia, pimpinan_penyedia, npwp_penyedia, nomor_kontrak,
                       tgl_kontrak_awal, tgl_kontrak_akhir, nomor_spmk, tgl_spmk_awal, tgl_spmk_akhir,
                       tgl_adendum_awal, tgl_adendum_akhir, COALESCE(status_kontrak, 'Dalam Proses') AS status_kontrak
                FROM ta_pekerjaan_kontrak
                WHERE id_pekerjaan = :id_pekerjaan
            """)
            kontrak_row = db.execute(kontrak_sql, {"id_pekerjaan": id_pekerjaan}).mappings().first()
            if kontrak_row:
                kontrak_dict = dict(kontrak_row)
        except Exception:
            db.rollback()

        if not kontrak_dict:
            kontrak_dict = {
                "nama_ppk": clean_text(pek_dict.get("nama_ppk")) or "",
                "nama_pptk": clean_text(pek_dict.get("nama_pptk")) or "",
                "nama_pokja": "",
                "nama_pphp": "",
                "nilai_hps": 0.0,
                "nilai_kontrak": 0.0,
                "sisa_anggaran": float(pek_dict.get("pagu_anggaran") or 0),
                "nama_penyedia": "",
                "alamat_penyedia": "",
                "pimpinan_penyedia": "",
                "npwp_penyedia": "",
                "nomor_kontrak": "",
                "tgl_kontrak_awal": None,
                "tgl_kontrak_akhir": None,
                "nomor_spmk": "",
                "tgl_spmk_awal": None,
                "tgl_spmk_akhir": None,
                "tgl_adendum_awal": None,
                "tgl_adendum_akhir": None,
                "status_kontrak": "Dalam Proses"
            }
        
        if kontrak_dict.get("id"):
            kontrak_dict["id"] = str(kontrak_dict["id"])
            kontrak_dict["id_pekerjaan"] = str(kontrak_dict["id_pekerjaan"])
        for d_key in ["tgl_kontrak_awal", "tgl_kontrak_akhir", "tgl_spmk_awal", "tgl_spmk_akhir", "tgl_adendum_awal", "tgl_adendum_akhir"]:
            if kontrak_dict.get(d_key):
                kontrak_dict[d_key] = str(kontrak_dict[d_key])

        return {
            "pekerjaan": pek_dict,
            "bulan": bulan,
            "str_bulan": MONTH_FULL_IND[bulan] if 1 <= bulan <= 12 else str(bulan),
            "realisasi": real_dict,
            "keuangan_lalu": round(keuangan_lalu, 2),
            "fisik_lalu": round(fisik_lalu, 2),
            "target_fisik_bulan_ini": round(target_fisik_bulan_ini, 2),
            "tagging": tagging_list,
            "lokasi": pek_dict.get("lokasi") or "",
            "lokasi_list": lokasi_list,
            "kontrak": kontrak_dict
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil detail realisasi pekerjaan: {str(e)}")


@router.post("/kontrak/simpan")
def simpan_pekerjaan_kontrak(
    payload: SimpanKontrakSchema,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        pek_sql = text("SELECT id, id_sub_pd, pagu_anggaran FROM ta_pekerjaan WHERE id = :id_pekerjaan")
        pek_row = db.execute(pek_sql, {"id_pekerjaan": payload.id_pekerjaan}).mappings().first()
        if not pek_row:
            raise HTTPException(status_code=404, detail="Pekerjaan tidak ditemukan")

        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if not current_user.id_opds or pek_row["id_sub_pd"] not in current_user.id_opds:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke Perangkat Daerah ini")

        pagu = float(pek_row["pagu_anggaran"] or 0)
        nil_kontrak = float(payload.nilai_kontrak or 0)
        sisa = pagu - nil_kontrak if (payload.sisa_anggaran is None or payload.sisa_anggaran == 0) else float(payload.sisa_anggaran)

        def parse_date(d_str):
            if not d_str or not d_str.strip():
                return None
            try:
                return datetime.strptime(d_str.strip(), "%Y-%m-%d").date()
            except ValueError:
                return None

        chk_sql = text("SELECT id FROM ta_pekerjaan_kontrak WHERE id_pekerjaan = :id_pekerjaan")
        chk_row = db.execute(chk_sql, {"id_pekerjaan": payload.id_pekerjaan}).mappings().first()

        params = {
            "id_pekerjaan": payload.id_pekerjaan,
            "nama_ppk": clean_text(payload.nama_ppk),
            "nama_pptk": clean_text(payload.nama_pptk),
            "nama_pokja": clean_text(payload.nama_pokja),
            "nama_pphp": clean_text(payload.nama_pphp),
            "nilai_hps": float(payload.nilai_hps or 0),
            "nilai_kontrak": nil_kontrak,
            "sisa_anggaran": sisa,
            "nama_penyedia": clean_text(payload.nama_penyedia),
            "alamat_penyedia": clean_text(payload.alamat_penyedia),
            "pimpinan_penyedia": clean_text(payload.pimpinan_penyedia),
            "npwp_penyedia": clean_text(payload.npwp_penyedia),
            "nomor_kontrak": clean_text(payload.nomor_kontrak),
            "tgl_kontrak_awal": parse_date(payload.tgl_kontrak_awal),
            "tgl_kontrak_akhir": parse_date(payload.tgl_kontrak_akhir),
            "nomor_spmk": clean_text(payload.nomor_spmk),
            "tgl_spmk_awal": parse_date(payload.tgl_spmk_awal),
            "tgl_spmk_akhir": parse_date(payload.tgl_spmk_akhir),
            "tgl_adendum_awal": parse_date(payload.tgl_adendum_awal),
            "tgl_adendum_akhir": parse_date(payload.tgl_adendum_akhir),
            "status_kontrak": payload.status_kontrak or 'Dalam Proses'
        }

        if chk_row:
            update_sql = text("""
                UPDATE ta_pekerjaan_kontrak
                SET nama_ppk = :nama_ppk,
                    nama_pptk = :nama_pptk,
                    nama_pokja = :nama_pokja,
                    nama_pphp = :nama_pphp,
                    nilai_hps = :nilai_hps,
                    nilai_kontrak = :nilai_kontrak,
                    sisa_anggaran = :sisa_anggaran,
                    nama_penyedia = :nama_penyedia,
                    alamat_penyedia = :alamat_penyedia,
                    pimpinan_penyedia = :pimpinan_penyedia,
                    npwp_penyedia = :npwp_penyedia,
                    nomor_kontrak = :nomor_kontrak,
                    tgl_kontrak_awal = :tgl_kontrak_awal,
                    tgl_kontrak_akhir = :tgl_kontrak_akhir,
                    nomor_spmk = :nomor_spmk,
                    tgl_spmk_awal = :tgl_spmk_awal,
                    tgl_spmk_akhir = :tgl_spmk_akhir,
                    tgl_adendum_awal = :tgl_adendum_awal,
                    tgl_adendum_akhir = :tgl_adendum_akhir,
                    status_kontrak = :status_kontrak,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_pekerjaan = :id_pekerjaan
            """)
            db.execute(update_sql, params)
        else:
            params["id"] = str(uuid.uuid4())
            insert_sql = text("""
                INSERT INTO ta_pekerjaan_kontrak (
                    id, id_pekerjaan, nama_ppk, nama_pptk, nama_pokja, nama_pphp,
                    nilai_hps, nilai_kontrak, sisa_anggaran, nama_penyedia, alamat_penyedia,
                    pimpinan_penyedia, npwp_penyedia, nomor_kontrak, tgl_kontrak_awal, tgl_kontrak_akhir,
                    nomor_spmk, tgl_spmk_awal, tgl_spmk_akhir, tgl_adendum_awal, tgl_adendum_akhir, status_kontrak
                ) VALUES (
                    :id, :id_pekerjaan, :nama_ppk, :nama_pptk, :nama_pokja, :nama_pphp,
                    :nilai_hps, :nilai_kontrak, :sisa_anggaran, :nama_penyedia, :alamat_penyedia,
                    :pimpinan_penyedia, :npwp_penyedia, :nomor_kontrak, :tgl_kontrak_awal, :tgl_kontrak_akhir,
                    :nomor_spmk, :tgl_spmk_awal, :tgl_spmk_akhir, :tgl_adendum_awal, :tgl_adendum_akhir, :status_kontrak
                )
            """)
            db.execute(insert_sql, params)

        db.execute(text("UPDATE ta_pekerjaan SET nama_ppk = COALESCE(:nama_ppk, nama_ppk), nama_pptk = COALESCE(:nama_pptk, nama_pptk) WHERE id = :id_pekerjaan"), {
            "id_pekerjaan": payload.id_pekerjaan,
            "nama_ppk": clean_text(payload.nama_ppk),
            "nama_pptk": clean_text(payload.nama_pptk)
        })

        db.commit()
        return {"status": "success", "message": "Berhasil menyimpan data kontrak / SPK pekerjaan"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan data kontrak / SPK: {str(e)}")


@router.post("/realisasi/simpan")
def simpan_pekerjaan_realisasi(
    payload: SimpanRealisasiPekerjaanSchema,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or payload.id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke Perangkat Daerah ini")

    try:
        check_sql = text("""
            SELECT id FROM ta_pekerjaan_realisasi
            WHERE id_pekerjaan = :id_pekerjaan AND bulan = :bulan
        """)
        row = db.execute(check_sql, {"id_pekerjaan": payload.id_pekerjaan, "bulan": payload.bulan}).mappings().first()

        prev_sql = text("""
            SELECT SUM(COALESCE(keuangan, 0)) AS tot_keu_lalu, MAX(COALESCE(fisik, 0)) AS max_fisik_lalu
            FROM ta_pekerjaan_realisasi
            WHERE id_pekerjaan = :id_pekerjaan AND bulan < :bulan
        """)
        prev_row = db.execute(prev_sql, {"id_pekerjaan": payload.id_pekerjaan, "bulan": payload.bulan}).mappings().first()
        keuangan_lalu = float(prev_row["tot_keu_lalu"] or 0) if (prev_row and prev_row["tot_keu_lalu"] is not None) else 0.0
        fisik_lalu = float(prev_row["max_fisik_lalu"] or 0) if (prev_row and prev_row["max_fisik_lalu"] is not None) else 0.0

        masalah_clean = payload.masalah[:500] if payload.masalah else None
        upaya_clean = payload.upaya[:500] if payload.upaya else None

        if row:
            update_sql = text("""
                UPDATE ta_pekerjaan_realisasi
                SET keuangan = :keuangan,
                    fisik = :fisik,
                    masalah = :masalah,
                    upaya = :upaya,
                    keuangan_lalu = :keuangan_lalu,
                    fisik_lalu = :fisik_lalu
                WHERE id_pekerjaan = :id_pekerjaan AND bulan = :bulan
                RETURNING id
            """)
            db.execute(update_sql, {
                "id_pekerjaan": payload.id_pekerjaan,
                "bulan": payload.bulan,
                "keuangan": payload.keuangan,
                "fisik": payload.fisik,
                "masalah": masalah_clean,
                "upaya": upaya_clean,
                "keuangan_lalu": keuangan_lalu,
                "fisik_lalu": fisik_lalu
            })
        else:
            insert_sql = text("""
                INSERT INTO ta_pekerjaan_realisasi (
                    id, id_sub_pd, id_pekerjaan, bulan, keuangan, fisik, masalah, upaya, keuangan_lalu, fisik_lalu
                ) VALUES (
                    gen_random_uuid(), :id_sub_pd, :id_pekerjaan, :bulan, :keuangan, :fisik, :masalah, :upaya, :keuangan_lalu, :fisik_lalu
                )
                RETURNING id
            """)
            db.execute(insert_sql, {
                "id_sub_pd": payload.id_sub_pd,
                "id_pekerjaan": payload.id_pekerjaan,
                "bulan": payload.bulan,
                "keuangan": payload.keuangan,
                "fisik": payload.fisik,
                "masalah": masalah_clean,
                "upaya": upaya_clean,
                "keuangan_lalu": keuangan_lalu,
                "fisik_lalu": fisik_lalu
            })

        db.commit()
        str_bln = MONTH_FULL_IND[payload.bulan] if 1 <= payload.bulan <= 12 else str(payload.bulan)
        return {
            "message": f"Berhasil menyimpan realisasi pekerjaan bulan {str_bln}"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan realisasi pekerjaan: {str(e)}")


@router.get("/realisasi-dokumen/{id_pekerjaan}/{bulan}")
def get_realisasi_dokumen_list(
    id_pekerjaan: str,
    bulan: int,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        sql = text("""
            SELECT id, id_pekerjaan, id_sub_pd, bulan, nama_file, file_path, tipe_file, keterangan,
                   ukuran_file, tgl_upload, user_upload
            FROM ta_pekerjaan_realisasi_dokumen
            WHERE id_pekerjaan = :id_pekerjaan AND bulan = :bulan
            ORDER BY tgl_upload DESC
        """)
        rows = db.execute(sql, {"id_pekerjaan": id_pekerjaan, "bulan": bulan}).mappings().all()
        result = []
        for r in rows:
            d = dict(r)
            d["id"] = str(d["id"])
            d["id_pekerjaan"] = str(d["id_pekerjaan"])
            d["nama_file"] = clean_text(d["nama_file"])
            d["keterangan"] = clean_text(d["keterangan"])
            if d.get("tgl_upload"):
                d["tgl_upload_fmt"] = d["tgl_upload"].strftime("%d %b %Y %H:%M")
            else:
                d["tgl_upload_fmt"] = None
            result.append(d)

        return {
            "dokumen_list": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil daftar dokumen pendukung: {str(e)}")


@router.post("/realisasi-dokumen/upload")
def upload_realisasi_dokumen(
    file: UploadFile = File(...),
    id_pekerjaan: str = Form(...),
    id_sub_pd: int = Form(...),
    bulan: int = Form(...),
    tipe_file: Optional[str] = Form("dokumen"),
    keterangan: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    if current_user and current_user.role_id is not None and current_user.role_id > 5:
        if not current_user.id_opds or id_sub_pd not in current_user.id_opds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses ke Perangkat Daerah ini")

    try:
        clean_upload_path = settings.UPLOAD_PATH.strip('"/\\') if settings.UPLOAD_PATH else "BERKAS_UPLOAD"
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        
        target_dir = os.path.join(project_root, clean_upload_path, "rfk", str(id_sub_pd), str(bulan))
        os.makedirs(target_dir, exist_ok=True)

        fallback_dir = os.path.join(project_root, "app", "uploads", "rfk", str(id_sub_pd), str(bulan))
        os.makedirs(fallback_dir, exist_ok=True)

        original_filename = file.filename or "dokumen"
        ext = os.path.splitext(original_filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        file_path_disk = os.path.join(target_dir, unique_name)
        fallback_path_disk = os.path.join(fallback_dir, unique_name)

        with open(file_path_disk, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        shutil.copyfile(file_path_disk, fallback_path_disk)

        file_size = os.path.getsize(file_path_disk)
        rel_file_path = f"/{clean_upload_path}/rfk/{id_sub_pd}/{bulan}/{unique_name}"

        mime = file.content_type or ""
        if "image" in mime or ext.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            tipe_file_final = "foto"
        else:
            tipe_file_final = tipe_file or "dokumen"

        user_name = current_user.name if (current_user and current_user.name) else (current_user.username if current_user else "System")

        ins_sql = text("""
            INSERT INTO ta_pekerjaan_realisasi_dokumen (
                id, id_pekerjaan, id_sub_pd, bulan, nama_file, file_path, tipe_file, keterangan, ukuran_file, tgl_upload, user_upload
            ) VALUES (
                gen_random_uuid(), :id_pekerjaan, :id_sub_pd, :bulan, :nama_file, :file_path, :tipe_file, :keterangan, :ukuran_file, NOW(), :user_upload
            )
            RETURNING id, nama_file, file_path, tipe_file, keterangan, ukuran_file, tgl_upload, user_upload
        """)
        new_row = db.execute(ins_sql, {
            "id_pekerjaan": id_pekerjaan,
            "id_sub_pd": id_sub_pd,
            "bulan": bulan,
            "nama_file": original_filename[:255],
            "file_path": rel_file_path,
            "tipe_file": tipe_file_final,
            "keterangan": (keterangan[:500] if keterangan else None),
            "ukuran_file": file_size,
            "user_upload": user_name
        }).mappings().first()

        db.commit()
        res_dict = dict(new_row)
        res_dict["id"] = str(res_dict["id"])
        res_dict["tgl_upload_fmt"] = res_dict["tgl_upload"].strftime("%d %b %Y %H:%M") if res_dict.get("tgl_upload") else None

        return {
            "message": "Berhasil mengunggah data dukung realisasi",
            "dokumen": res_dict
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal mengunggah file data dukung: {str(e)}")


@router.delete("/realisasi-dokumen/{dok_id}")
def delete_realisasi_dokumen(
    dok_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[CurrentUser] = Depends(get_current_user_from_jwt)
):
    try:
        check_sql = text("SELECT id, id_sub_pd, file_path FROM ta_pekerjaan_realisasi_dokumen WHERE id = :dok_id")
        row = db.execute(check_sql, {"dok_id": dok_id}).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Dokumen data dukung tidak ditemukan")

        if current_user and current_user.role_id is not None and current_user.role_id > 5:
            if not current_user.id_opds or row["id_sub_pd"] not in current_user.id_opds:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki hak akses untuk menghapus dokumen ini")

        rel_path = row["file_path"]
        if rel_path:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            full_disk_path = os.path.join(project_root, rel_path.lstrip("/"))
            if os.path.exists(full_disk_path):
                try:
                    os.remove(full_disk_path)
                except Exception as ex:
                    print("Warning: failed removing file from disk:", ex)

        del_sql = text("DELETE FROM ta_pekerjaan_realisasi_dokumen WHERE id = :dok_id")
        db.execute(del_sql, {"dok_id": dok_id})
        db.commit()

        return {
            "message": "Berhasil menghapus dokumen data dukung"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menghapus dokumen data dukung: {str(e)}")




