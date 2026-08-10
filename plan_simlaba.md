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

Submit RKO Error AttributeError: 'CurrentUser' object has no attribute 'name'


Notifikasi jangan pakai javascript alert, pakai notifikasi yang modern 


## RKO
Form Pekerjaan 
ubah Pelaksanaan Pekerjaan menjadi satu combobox bulan Januari - Desember, bisa dipilih lebih dari 1 (multiselect)



## RKO
Form Pekerjaan 
Tambah field Sumber dana, combobox dari tabel ref_sumberdana


## Pengaturan
Pengaturan User, Peragnkat Daerah dan Tagging, kolom aksi icon edit dapus pakai menu saja 


## RKO
Saat expand semua item treeview, lebar kolom Program > Kegiatan > Subkegiatan > Pekerjaan maksimal 50%


## Dashboard
Perbaiki Data pada dashboard, 
Total angggaran field anggaran pada tabel renja_subkegiatan
Serapan Anggaran field realisasi pada tabel renja_subkegiatan_realisasi
Capaian Realisasi Fisik field fisik tabel ta_pekerjaan_realisasi pada bulan terahir
Deviasi (realisasi fisik - target fisik) 

## RKO 
Form Pekerjaan bisa maximize 

## RKO
Tambah kolom nama_ppk dan nama_pptk

## RKO
Tooltip text pada item di kolom Program > Kegiatan > Subkegiatan > Pekerjaan

## RKO 
Form Pekerjaan
Jika pilih tagging Usulan Pokir DPRD, munculkan combobox searcable Usulan Pokir DPRD (tabel ta_pokir), tampilkan field nama_kamus, usulan, nama_pengusul
bisa dipilih lebih dari satu


## RKO
Form Pekerjaan
Jika pilih tagging Usulan Musrenbang, munculkan combobox searcable Usulan Musrenbang (tabel ta_musrenbang), tampilkan field nama_kamus, usulan, nama_pengusul
bisa dipilih lebih dari satu

## RKO
Form Pekerjaan
Jika pilih sumber dana dengan kode diawali 2.2.01.09 (Dana Alokasi Khusus DAK), munculkan combobox searcable data dari tabel dak_detail_rincian
hanya bisa dipilih satu



## RFK
- Tampilan Awal OPD List
- Kolom  Kode OPD | Nama OPD | Laporan Bulanan |
                              | Jan | Feb | Mar | Apr | Mei | Jun | Jul | Agu | Sep | Okt | Nov | Des |
  tgl_kirim format Tanggal Bulan
tabel terkait  ta_opd, ta_laporan_rfk

## RFK
Klik nama OPD, tampilkan tabel :
No | Bulan | Tanggal Buat | Tanggal Kirim | Tanggal Verifikasi

dari tabel ta_laporan_rfk

## RFK
Tampilkan hanya sampai bulan yang ada di tabel  ta_laporan_rfk
tambah button Buat Laporan RFK
Proses Buat Laporan RFK : 
- Jika RKO sudah diapprove admin
- Jika bulan sebelumnya sudah dikirim


## RFK
Klik Item Bulan, tampilkan data RFK bulan tersebut
| Program > Kegiatan > Sub kegiatan > Pekerjaan   | Anggaran | Realisasi Fisik | Realisasi Keuangan                                   | Realisai Keuangan Per Bulan                                           |
|                                                 |          |                 | Bulan Ini  | Total Sampai Bulan Ini  | Total (SIPD)  | Jan | Feb | Mar | Apr | Mei | Jun | Jul | Agu | Sep | Okt | Nov | Des |
| -------- | ------- |        |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 

 | Anggaran |  | 

 ## RFK
 Revisi flow RFK
 Klik Nama OPD tampilkan tabel bulan
 klik item bulan pada tabel bulan  tampilkan data RFK (jangan bentuk modal)

## RFK
 khusus admin
 pada tabel bulan tambah tombol Aksi Hapus 

- Proses hapus harus urut dari bulan terbaru dulu, tidak bisa lompat
 

## RFK
Klik Item Pekerjaan, tampilkan form entri realisasi 
tabel ta_pekerjaan_realisasi

## RFK
saat buat laporan RFK, copy ta_pekerjaan_realisasi bulan lalu. realisasi fisik dan fisik bulan lalu
Form Entri Realisasi Pekerjaan tampilkan realisasi fisik bulan lalu, target fisik bulan ini, tagging

## RFK
Form Entri Realisasi Pekerjaan
Buat tab Upload data dukunng (Foto, dokumen) untuk pekerjaan tersebut


## RFK
Form Entri Realisasi Pekerjaan
tambah navigasi previous next untuk load data sebelum / berikutnya

## RFK
Form Entri Realisasi Pekerjaan
simpan data jangan tutup window


## Laporan 
set nama variabel form yang akan di post 
Perangkat daerah : pid_sub_pd
Tahun : ptahun
Bulan : pbulan
Footer : pfooter
Format : format


## RFK
Form Entri Realisasi Pekerjaan
Buat tab Lokasi Pekerjaan, beserta map

## RFK
Form Entri Realisasi Pekerjaan
Buat tab Kontrak / SPK
Field :
- Nama PPK
- Nama PPTK
- Nama Ketua Pokja / Pejabat Pengadaan
- Nama Ketua PPHP
- Nilai HPS
- Nilai Kontrak
- Sisa Anggaran
- Nama Penyedia
- Alamat Penyedia
- Nama Pimpinan Penyedia
- NPWP Penyedia
- Nomor Pengadaan / Kontrak / SPK
- Tanggal Kontrak (dari - sampai dengan)
- Nomor SPMK
- Tanggal SPMK (dari - sampai dengan)
- Tanggal Adendum Kontrak (dari - sampai dengan)
- Status (Selesai, Dalam Proses, Dibatalkan)
-