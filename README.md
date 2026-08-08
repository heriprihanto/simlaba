# SIMLABA — Sistem Informasi Laporan Perkembangan Pembangunan
> **Pemerintah Kota Tegal**  
> *Bagian Pengadaan Barang dan Jasa, dan Administrasi Pembangunan Setda Kota Tegal*

---

## 📌 Tentang SIMLABA

**SIMLABA (Sistem Informasi Laporan Perkembangan Pembangunan)** adalah platform web terintegrasi untuk pengelolaan, pemantauan, dan evaluasi Rencana Kerja Operasional (RKO) serta realisasi pembangunan di lingkungan Pemerintah Kota Tegal T.A. 2026.

Aplikasi ini menyediakan analisis data eksekutif secara real-time, visualisasi geospasial lokasi pekerjaan (GIS), pengelolaan hirarki cascading program hingga paket pekerjaan, serta sistem keamanan SSO berstandar tinggi.

---

## ✨ Fitur Utama

### 1. 📊 Dashboard Eksekutif Pembangunan
- **Metrics Realtime**: Menampilkan Total Anggaran DPA, Serapan Anggaran Keuangan, Capaian Realisasi Fisik (bulan berjalan), serta Deviasi (Realisasi Fisik - Target Fisik).
- **Grafik Tren RFK**: Grafik area & bar interaktif perkembangan fisik dan keuangan bulanan berbasis **ApexCharts**.
- **Donut Chart Serapan**: Distribusi proporsi metode pengadaan (Tender, Pengadaan Langsung, Swakelola, E-Purchasing).
- **Ranking Top OPD**: Peringkat kinerja realisasi fisik & keuangan antar Perangkat Daerah.

### 2. 🗂️ Rencana Kerja Operasional (RKO)
- **Treeview Cascading Grid**: Pengelolaan data hirarki **Program ➔ Kegiatan ➔ Subkegiatan ➔ Paket Pekerjaan**.
- **Formulir Pekerjaan Modern**:
  - Picker Pejabat (PPK & PPTK) terintegrasi dengan Master SDM Personel.
  - Combobox Multiselect Bulan Pelaksanaan Pekerjaan (Januari – Desember).
  - Searchable Combobox Sumber Dana terintegrasi dengan tabel `ref_sumberdana`.
  - Pilihan Jenis Paket Pekerjaan (Penyedia vs Swakelola).
- **Sistem Kunci Data & Approval RKO**:
  - Penguncian otomatis data RKO saat OPD melakukan submit.
  - Validasi aturan RKO (Alokasi Subkegiatan, Pagu DPA = Pagu Pekerjaan, Target Des 100%).
  - Status Submit & Approval Admin/Supervisor di daftar OPD.

### 3. 🗺️ Peta Lokasi Pekerjaan (GIS Integration)
- Visualisasi peta interaktif lokasi pembangunan menggunakan **Leaflet** dan **Leaflet-Geoman Free**.
- Dukungan pembuatan dan penyuntingan titik/garis/area geospasial (Point, LineString, Polygon) GeoJSON.
- Custom marker icon, tooltip, dan popup informasi detail paket pekerjaan.

### 4. 👥 Manajemen SDM Personel & Pegawai
- Pengelolaan daftar pegawai per Perangkat Daerah (OPD).
- Pemetaan otomatis Golongan ke Pangkat Pegawai Negeri Sipil (PNS).
- Upload foto profil personel.

### 5. ⚙️ Pengaturan Sistem & Manajemen User
- Kelola Hak Akses & Role User Pengguna.
- Reset Password & Kirim Notifikasi Email.
- Kelola Data Perangkat Daerah (OPD) & Referensi Tagging.
- Menu Aksi Dropdown (`MoreVertical`) pada setiap baris tabel.

### 6. 🔐 Keamanan & Authentication
- Login SSO Pemerintah Kota Tegal.
- **Visual Captcha Interaktif**: Kode keamanan 5-karakter dengan noise background dan acak dinamis untuk memproteksi serangan bot.
- Notifikasi Modern menggunakan **SweetAlert2** Toast dan Modal Dialog.

---

## 🛠️ Teknologi & Stack

### Backend
- **Framework**: FastAPI (Python 3.10+ / Python 3.14)
- **Database**: PostgreSQL (`dalev_kota_tegal_2027`)
- **ORM & Driver**: SQLAlchemy 2.0 & Psycopg3
- **Server**: Uvicorn (ASGI Engine)

### Frontend
- **Framework**: Vue 3 (Composition API / `<script setup>`)
- **Build Tool**: Vite 5
- **Styling**: Vanilla Tailwind CSS (Modern Glassmorphism & Dark Mode)
- **State Management**: Pinia Store (`authStore`)
- **Icons**: Lucide Vue Icons (`lucide-vue-next`)
- **Charts**: Vue3-ApexCharts
- **Maps**: Leaflet & @geoman-io/leaflet-geoman-free
- **Notifications**: SweetAlert2

---

## 🚀 Panduan Memulai (Getting Started)

### Prasyarat
- **Node.js**: v18.0.0 atau lebih baru
- **Python**: v3.10 atau lebih baru
- **PostgreSQL**: v13 atau lebih baru

---

### 1. Running Backend

```bash
# Masuk ke direktori Backend
cd Backend

# Mengaktifkan Virtual Environment
source venv/bin/python

# Menjalankan Uvicorn Server
sh run.sh
# Atau menjalankan langsung via Python:
# python main.py
```
*Backend API akan berjalan di: `http://localhost:8000` (Swagger UI: `http://localhost:8000/docs`)*

---

### 2. Running Frontend

```bash
# Masuk ke direktori Frontend
cd Frontend

# Install dependencies
npm install

# Menjalankan Development Server
npm run dev

# Kompilasi Production Bundle
npm run build
```
*Frontend App akan berjalan di: `http://localhost:5173`*

---

## 📄 Struktur Direktori Proyek

```
SIMLABA/
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/     # API Routes (auth, rko, dashboard, personel, pengaturan)
│   │   ├── core/              # Database Config & Security
│   │   └── main.py            # FastAPI Entry Point
│   ├── run.sh                 # Backend Startup Script
│   └── venv/                  # Python Virtual Environment
├── Frontend/
│   ├── src/
│   │   ├── assets/            # CSS & Stylesheet
│   │   ├── composables/       # Vue Composables (useTheme, etc)
│   │   ├── router/            # Vue Router Navigation Rules
│   │   ├── stores/            # Pinia Stores (auth.js)
│   │   ├── utils/             # Helper utilities (notify.js, sweetalert2)
│   │   └── views/             # Vue Pages (Dashboard, RKO, Peta, Personel, Pengaturan, Login)
│   ├── index.html             # HTML Template
│   ├── package.json           # Frontend Dependencies
│   └── vite.config.js         # Vite Configuration
├── plan_simlaba.md            # Plan & Catatan Pengembangan Project
└── README.md                  # Dokumentasi Proyek
```

---

## ⚖️ Lisensi & Hak Cipta
&copy; 2026 **Bagian Pengadaan Barang dan Jasa, dan Administrasi Pembangunan Setda Kota Tegal**.  
*Seluruh hak cipta dilindungi undang-undang.*
