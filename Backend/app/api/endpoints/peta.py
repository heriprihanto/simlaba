from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.core.database import get_db
import json

router = APIRouter()


@router.get("/locations")
def get_map_locations(
    tahun: int = Query(2026),
    id_sub_pd: Optional[int] = Query(None),
    jenis_pengadaan: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        where_clauses = ["p.tahun = :tahun"]
        params = {"tahun": tahun}

        if id_sub_pd:
            where_clauses.append("p.id_sub_pd = :id_sub_pd")
            params["id_sub_pd"] = id_sub_pd

        if jenis_pengadaan:
            where_clauses.append("p.jenis_pengadaan = :jenis_pengadaan")
            params["jenis_pengadaan"] = jenis_pengadaan

        if search:
            where_clauses.append("(p.nama_pekerjaan ILIKE :search OR l.nama_lokasi ILIKE :search OR p.lokasi ILIKE :search)")
            params["search"] = f"%{search}%"

        where_sql = " AND ".join(where_clauses)

        sql = text(f"""
            SELECT 
                l.id AS id_lokasi,
                l.id_pekerjaan,
                l.nama_lokasi,
                l.jenis_geometry,
                l.geojson,
                l.lat,
                l.lng,
                l.radius,
                ST_AsGeoJSON(l.geom) AS st_geojson,
                p.nama_pekerjaan,
                p.pagu_anggaran,
                p.volume,
                p.satuan,
                p.jenis_paket,
                p.jenis_pengadaan,
                p.lokasi AS lokasi_text,
                p.ket_pekerjaan,
                o.id_sub_pd,
                o.nama_pd,
                COALESCE(r.realisasi_keuangan, 0) AS realisasi_keuangan,
                COALESCE(r.realisasi_fisik, 0) AS realisasi_fisik,
                r.bulan_terakhir
            FROM ta_pekerjaan_lokasi l
            JOIN ta_pekerjaan p ON l.id_pekerjaan = p.id
            JOIN ta_opd o ON p.id_sub_pd = o.id_sub_pd
            LEFT JOIN (
                SELECT 
                    id_pekerjaan, 
                    MAX(bulan) AS bulan_terakhir,
                    SUM(keuangan) AS realisasi_keuangan,
                    MAX(fisik) AS realisasi_fisik
                FROM ta_pekerjaan_realisasi
                GROUP BY id_pekerjaan
            ) r ON p.id = r.id_pekerjaan
            WHERE {where_sql}
            ORDER BY l.created_at DESC
        """)

        rows = db.execute(sql, params).mappings().all()

        results = []
        for r in rows:
            geojson_data = None
            if r.get("st_geojson"):
                try:
                    geojson_data = json.loads(r["st_geojson"])
                except Exception:
                    pass
            elif r.get("geojson"):
                geojson_data = r["geojson"]

            lat_val = float(r["lat"]) if r.get("lat") is not None else None
            lng_val = float(r["lng"]) if r.get("lng") is not None else None

            # Fallback coordinates if GeoJSON point exists
            if (lat_val is None or lng_val is None) and geojson_data and geojson_data.get("type") == "Point":
                coords = geojson_data.get("coordinates", [])
                if len(coords) >= 2:
                    lng_val, lat_val = coords[0], coords[1]

            results.append({
                "id_lokasi": str(r["id_lokasi"]),
                "id_pekerjaan": str(r["id_pekerjaan"]),
                "nama_lokasi": r["nama_lokasi"] or r["nama_pekerjaan"],
                "jenis_geometry": r["jenis_geometry"] or "Point",
                "geojson": geojson_data,
                "lat": lat_val,
                "lng": lng_val,
                "radius": float(r["radius"]) if r.get("radius") is not None else None,
                "nama_pekerjaan": r["nama_pekerjaan"],
                "pagu_anggaran": float(r["pagu_anggaran"] or 0),
                "volume": float(r["volume"]) if r.get("volume") is not None else None,
                "satuan": r.get("satuan") or "",
                "jenis_paket": r.get("jenis_paket") or 1,
                "jenis_pengadaan": r.get("jenis_pengadaan") or 1,
                "lokasi_text": r.get("lokasi_text") or "",
                "ket_pekerjaan": r.get("ket_pekerjaan") or "",
                "id_sub_pd": r["id_sub_pd"],
                "nama_opd": r["nama_pd"],
                "realisasi_keuangan": float(r["realisasi_keuangan"] or 0),
                "realisasi_fisik": float(r["realisasi_fisik"] or 0),
                "bulan_terakhir": r.get("bulan_terakhir")
            })

        return results
    except Exception as e:
        print("Error fetching GIS map locations:", e)
        return []


@router.get("/summary")
def get_map_summary(tahun: int = Query(2026), db: Session = Depends(get_db)):
    try:
        sql = text("""
            SELECT 
                COUNT(DISTINCT p.id) AS total_pekerjaan,
                COUNT(l.id) AS total_lokasi_gis,
                COALESCE(SUM(p.pagu_anggaran), 0) AS total_anggaran,
                COALESCE(SUM(r.realisasi_keuangan), 0) AS total_realisasi_keuangan,
                COALESCE(AVG(r.realisasi_fisik), 0) AS avg_realisasi_fisik
            FROM ta_pekerjaan p
            LEFT JOIN ta_pekerjaan_lokasi l ON p.id = l.id_pekerjaan
            LEFT JOIN (
                SELECT 
                    id_pekerjaan, 
                    SUM(keuangan) AS realisasi_keuangan,
                    MAX(fisik) AS realisasi_fisik
                FROM ta_pekerjaan_realisasi
                GROUP BY id_pekerjaan
            ) r ON p.id = r.id_pekerjaan
            WHERE p.tahun = :tahun
        """)
        row = db.execute(sql, {"tahun": tahun}).mappings().first()
        return {
            "total_pekerjaan": row["total_pekerjaan"],
            "total_lokasi_gis": row["total_lokasi_gis"],
            "total_anggaran": float(row["total_anggaran"] or 0),
            "total_realisasi_keuangan": float(row["total_realisasi_keuangan"] or 0),
            "avg_realisasi_fisik": float(row["avg_realisasi_fisik"] or 0)
        }
    except Exception as e:
        return {
            "total_pekerjaan": 0,
            "total_lokasi_gis": 0,
            "total_anggaran": 0,
            "total_realisasi_keuangan": 0,
            "avg_realisasi_fisik": 0
        }
