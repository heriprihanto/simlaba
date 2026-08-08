import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.endpoints import auth, dashboard, personel, peta, pengaturan, rko

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

# Static Files for Uploads
backend_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(backend_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Register Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(personel.router, prefix=f"{settings.API_V1_STR}/personel", tags=["Personel"])
app.include_router(peta.router, prefix=f"{settings.API_V1_STR}/peta", tags=["Peta"])
app.include_router(pengaturan.router, prefix=f"{settings.API_V1_STR}/pengaturan", tags=["Pengaturan"])
app.include_router(rko.router, prefix=f"{settings.API_V1_STR}/rko", tags=["RKO"])


@app.get("/")
def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
