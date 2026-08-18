import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.endpoints import auth, dashboard, personel, peta, pengaturan, rko, rfk, rpjpd, rpjmd
from app.pages.page_router import page_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="API Server SIMLABA (Sistem Informasi Laporan Perkembangan Pembangunan Kota Tegal)"
)

# CORS Configuration
origins = settings.cors_origins
if not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files for Uploads (Configured via UPLOAD_PATH in .env)
clean_upload_path = settings.UPLOAD_PATH.strip('"/\\') if settings.UPLOAD_PATH else "BERKAS_UPLOAD"
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
uploads_dir = os.path.join(project_dir, clean_upload_path)
os.makedirs(uploads_dir, exist_ok=True)

app.mount(f"/{clean_upload_path}", StaticFiles(directory=uploads_dir), name=clean_upload_path)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Register Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(personel.router, prefix=f"{settings.API_V1_STR}/personel", tags=["Personel"])
app.include_router(peta.router, prefix=f"{settings.API_V1_STR}/peta", tags=["Peta"])
app.include_router(pengaturan.router, prefix=f"{settings.API_V1_STR}/pengaturan", tags=["Pengaturan"])
app.include_router(rko.router, prefix=f"{settings.API_V1_STR}/rko", tags=["RKO"])
app.include_router(rfk.router, prefix=f"{settings.API_V1_STR}/rfk", tags=["RFK"])
app.include_router(rpjpd.router, prefix=f"{settings.API_V1_STR}/rpjpd", tags=["RPJPD"])
app.include_router(rpjmd.router, prefix=f"{settings.API_V1_STR}/rpjmd", tags=["RPJMD"])


@app.get("/")
def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs_url": "/docs"
    }

app.include_router(page_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
