SIMLABA (Sistem Informasi Laporan Perkembangan Pembangunan  )

Sistem ini digunakan untuk memonitor dan mengevaluasi pelaksanaan pembangunan di Kota Tegal.

Fitur
- Monitoring pelaksanaan pembangunan
- Pelaporan perkembangan pembangunan
- Evaluasi pelaksanaan pembangunan
- Laporan pelaksanaan pembangunan

Stack
- Python
- FastAPI, SqlAlchemy, SqlModel, psycopg3
- PostgreSQL
- Vue 3
- Pinia
- Shadcn UI
- Vite

warna 
--theme-default #308e87
--theme-secondary #f39159;

top horizontal navigation menu 

## Menu 
- Dashboard 
- Personel
- RKO (Rencana Kerja Operasional)
- RFK (Realisasi Fisik & Keuangan)
- Laporan
- Pengaturan
- Peta

## Dashboard
- Card  Total Anggaran, Serapan Anggaran, Realisasi Fisik, Deviasi
- Line Grafik RFK Per Bulan
- Bar Grafik Target vs Realisasi
- Pie Grafik Total Serapan Anggaran
- Ranking OPD dengan Realisasi Fisik dan Keuangan


## Personel
- Tabel ta_personel

## RKO
- Halaman Kosong dulu

## RFK
- Halaman Kosong dulu

## Laporan
- Halaman Kosong dulu

## PEngaturan
- Halaman Kosong dulu


Login JWT dengan SQL "SELECT * 
            FROM public.sso_users u 
            WHERE u.username = username 
              AND password = encode_passwd(username, password)"


revamp tampilan  modern, fancy, corporate, responsive, tambah button toggle mode dark / light

## REVISI HALAMAN PERSONEL
tampilan pertama tampilkan OPD dari tabel ta_opd order by kode
kode | nama OPD | Jumlah Personel
klik OPD, tampilkan personel dari ta_personel yang memiliki id_sub_pd sesuai yang diklik


revamp tampilan lebih modern, full color, corporate style, default font tambah 2 point

Buat halaman Pengaturan 
Buat Tab  User | Perangkat Daerah  
Pengaturan Perangkat Daerah  tabel ta_opd  order by kode
Pengaturan User  tabel sso_users
  - field id_opds id_sub_pd (pada tabel ta_opd) array bisa lebih dari satu OPD
  - id_sub_pd bisa null, jika null maka user bisa mengakses semua OPD
  - role_id  1 User Admin
              2 Admin Bidang
              3 Supervisor
              4 Auditor
              5 Verifikator
              6 Kepala OPD
              7 Kepala Bidang OPD
              8 Kepala Sub Bidang OPD
              9 Staff OPD
              
Buat CRUD pada pengaturan perangkat daerah
Pengaturan User, tambah aktif / tidak aktif, reset password

Reset password menggunakan 8 karakter acak, huruf besar, huruf kecil, angka. terkirim ke email user tersebut


reset pas dulu, sword, kirim ke  email user, gunakan SMTP_HOST pada file .env

Buat Tampilan dulu,  halaman Laporan 
Dua kolom
kolom kiri 
Jenis Laporan
treeview 
RKO 
  - RKO (Semua)
  - RKO Bagian I-III (Visi Misi, Alokasi Anggaran, Struktur Organisasi)
  - RKO Bagian IV (Tabel Program dan Kegiatan yang dilaksanakan)
  - RKO Bagian V (Paket Pekerjaan dan Jadwal Pelaksanaan)
  - RKO Bagian VI (Rencana Pengeluaran Anggaran)
  - RKO Bagian VII (Target Fisik Kegiatan yang dilaksanakan)
  - RKO Bagian VIII (Penutup)
RFK 
  - RFK 1
  - RFK 2
  - RFK 3
  - ProSN
  - Progres Kegiatan Pokir
  - Progres Kegiatan Musrenbang
Rekapitulasi
  - Rekap Bulanan
  - Rekap Pengiriman Laporan
  - Peringkat Realisasi
  - Laporan Deviasi
  - Rekapitulasi Anggaran Berdasarkan Bidang
kolom kanan  
Form parameter filter sesuai jenis laporan 
- OPD (combobox pilih OPD)
- Tahun
- BUlan 
- Footer text
- Format (Web, PDF, Excel, Word)


User role_id > 5 hanya menampilkan OPD sesuai id_opds
id_opds array id_sub_pd pada tabel ta_opd

filter data by opd sebaiknya di backend,by jwt.  jangan lewatkan parameter di client

Form Personel
Tambah upload foto profil
Golongan   Pangkat
II/a Pengatur Muda 
II/b Pengatur Muda Tingkat I 
II/c Pengatur 
II/d Pengatur Tingkat I
III/a Penata Muda 
III/b Penata Muda Tingkat I 
III/c Penata 
III/d Penata Tingkat I
IV/a Pembina
IV/b Pembina Tingkat II
IV/c Pembina Utama Muda
IV/d Pembina Utama Madya
IV/e Pembina Utama

## RKO
- Tampilan Awal OPD List
- Kolom  Kode OPD | Nama OPD | Total Anggaran | Jumlah Subkegiatan | Jumlah Pekerjaan
tabel terkait  ta_opd, renja_subkegiatan, ta_pekerjaan

## RKO
  Form Pekerjaan
  
LAbel | fieldName

Nomor  | nomor_pekerjaan 
Nama Pekerjaan  | nama_pekerjaan
Keterangan  | ket_pekerjaan
Anggaran  | pagu_anggaran
Volume  | volume
Satuan  | satuan
Jenis Paket  | jenis_paket | combobox :1 Penyedia 2 Swakelola 
Jenis Pekerjaan  | jenis_pengadaan | combobox :1 Pengadaan Barang, 2 Jasa Konsultasi, 3 Jasa Lainnya, 4 Konstruksi
Tipe Swakelola  | tipe_swa | combobox :1 Tipe 1, 2 Tipe 2, 3 Tipe 3, 4 Tipe 4
Penyelenggara Swakelola  | penyelenggara_swa 
Metode Pemilihan Penyedia  | metode | combobox :1 Lelang, 2 Seleksi Umum, 3 Lelang Sederhana, 4 Pengadaan Langsung, 5 Penunjukan Langsung, 6 E-Purchasing, 7 Swakelola
Pelaksanaan Pekerjaan  (Awal) | awal_pelaksanaan  | combobox bulan Januari - Desember
Pelaksanaan Pekerjaan  (Akhir) | akhir_pelaksanaan | combobox bulan Januari - Desember
Pemilihan Penyedia  (Awal) | awal_pemilihan    | combobox bulan Januari - Desember
Pemilihan Penyedia  (Akhir) | akhir_pemilihan   | combobox bulan Januari - Desember
Pelaksanaan Kontrak  (Awal) | awal_kontrak      | combobox bulan Januari - Desember
Pelaksanaan Kontrak  (Akhir) | akhir_kontrak     | combobox bulan Januari - Desember
Tagging  | tags              | multiselect combobox dari tabel ref_tagging


## RKO
  Form Pekerjaan

  Tambah text Lokasi Pekerjaan, bisa lebih dari satu lokasi
  tambahkan maps,leaflet js, pilih lokasi di peta, simpan koordinat 
  koordinat bisa titik, polygon, line, square, bundar
  Pakai postgis

  ## Peta
  Halaman menu peta dari Lokasi Pekerjaan
  tabel terkait ta_pekerjaan,ta_pekerjaan_lokasi, ta_pekerjaan_realisasi


## RKO
  Form Pekerjaan
  Jika Jenis Paket swakelola, sembunyikan 
Pemilihan Penyedia
Pelaksanaan Kontrak


## RKO
Buat Prosedur Submit RKO
Sudah ada Pekerjaan pada semua SUbkegiatan, minimal satu pekerjaan
Tidak ada perbedaan jumlah pagu pekerjaan dan pagu anggaran renja subkegiatan
Target Keuangan dan Fisik pada bulan desember sudah 100 % 

## RKO
OPD List, Total Anggaran Berwarna Merah jika Total anggaran renja_subkegiatan dengan ta_pekerjaan

## RKO
Setelah OPD SUbmit RKO, Data RKO terkunci, OPD tidak bisa membuka.
 Admin melalukan approve RKO, 
tampilkan Status submit dan approve admin di OPD List


## RKO
Form Pekerjaan
nama_ppk pilih dari ta_personel
nama_pptk pilih dari ta_personel