<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    
    <!-- Top Action & Info Bar -->
    <div class="bg-white dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-5 py-3.5 flex flex-wrap items-center justify-between gap-3 shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br flex items-center justify-center text-white shadow-md" :class="currentApp.iconColor">
          <component :is="iconComponent" class="w-5 h-5" />
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h2 class="text-sm font-black text-slate-900 dark:text-white">{{ currentApp.title }}</h2>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]">{{ currentApp.category }}</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ currentApp.desc }}</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center space-x-2">
        <button 
          @click="showSwal('Ekspor Data', `Data ${currentApp.title} berhasil diunduh.`)"
          class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 flex items-center space-x-1.5 transition-colors"
        >
          <Download class="w-3.5 h-3.5" />
          <span>Ekspor</span>
        </button>
        <button 
          @click="showSwal('Tambah Data', `Formulir penambahan data ${currentApp.title} dibuka.`)"
          class="px-3 py-1.5 rounded-lg text-xs font-bold bg-[#308e87] hover:bg-[#27756f] text-white flex items-center space-x-1.5 shadow-sm"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Data</span>
        </button>
      </div>
    </div>

    <!-- Search & Filter Bar -->
    <div class="bg-slate-100 dark:bg-[#111c2e] border-b border-slate-200 dark:border-slate-800 px-5 py-2.5 flex flex-col sm:flex-row items-center justify-between gap-3 shrink-0">
      <div class="relative w-full sm:w-72">
        <Search class="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Cari data..."
          class="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-[#308e87]"
        />
      </div>
      <div class="text-[11px] text-slate-500 font-medium">
        Kota Tegal • Tahun Anggaran 2026/2027
      </div>
    </div>

    <!-- Content Area (Scrollable) -->
    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      
      <!-- Summary Banner Card -->
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center space-x-2">
            <span class="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-wider bg-[#308e87]/10 text-[#308e87]">
              {{ currentApp.badge }}
            </span>
            <span class="text-xs font-bold text-slate-700 dark:text-slate-300">Modul Perencanaan &amp; Evaluasi</span>
          </div>
          <span class="text-xs text-emerald-600 font-bold">Terhubung ke Database</span>
        </div>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
          {{ currentApp.desc }}. Modul ini memfasilitasi integrasi cascading program, pemantauan target kinerja, alokasi anggaran, serta pelaporan berkala secara akuntabel.
        </p>
      </div>

      <!-- Data Table -->
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
        <table class="w-full text-left text-xs border-collapse">
          <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-bold border-b border-slate-200 dark:border-slate-800 text-[11px]">
            <tr>
              <th class="py-2.5 px-4 w-20 text-center">Kode</th>
              <th class="py-2.5 px-4">Uraian / Indikator Kinerja</th>
              <th class="py-2.5 px-4 w-44">Perangkat Daerah (OPD)</th>
              <th class="py-2.5 px-4 text-center w-24">Target</th>
              <th class="py-2.5 px-4 text-center w-24">Realisasi</th>
              <th class="py-2.5 px-4 text-center w-24">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
            <tr v-for="item in filteredRows" :key="item.kode" class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
              <td class="py-2.5 px-4 text-center font-bold text-[#308e87]">{{ item.kode }}</td>
              <td class="py-2.5 px-4 font-bold text-slate-900 dark:text-white leading-relaxed">{{ item.uraian }}</td>
              <td class="py-2.5 px-4 text-slate-600 dark:text-slate-300 font-medium">{{ item.opd }}</td>
              <td class="py-2.5 px-4 text-center font-bold text-slate-700 dark:text-slate-300">{{ item.target }}</td>
              <td class="py-2.5 px-4 text-center font-black text-emerald-600">{{ item.realisasi }}</td>
              <td class="py-2.5 px-4 text-center">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-600 border border-emerald-200">
                  {{ item.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Swal from 'sweetalert2'
import { useWindowStore } from '@/stores/windowStore'
import { 
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, Download, Plus, Search 
} from 'lucide-vue-next'

const props = defineProps({
  appId: { type: String, required: true }
})

const windowStore = useWindowStore()
const searchQuery = ref('')

const iconMap = {
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText 
}

const currentApp = computed(() => {
  return windowStore.appDefinitions.find(a => a.id === props.appId) || {
    id: props.appId,
    title: 'Modul EMONEV',
    category: 'Perencanaan',
    desc: 'Modul sistem perencanaan dan evaluasi pembangunan daerah.',
    icon: 'Layers',
    iconColor: 'from-blue-600 to-blue-800',
    badge: 'EMONEV'
  }
})

const iconComponent = computed(() => iconMap[currentApp.value.icon] || Layers)

const sampleDataMap = {
  renstra: [
    { kode: 'RS.01', uraian: 'Pengembangan Akses dan Kualitas Layanan Pendidikan Dasar', opd: 'Dinas Pendidikan & Kebudayaan', target: '100%', realisasi: '96.5%', status: 'Sesuai Target' },
    { kode: 'RS.02', uraian: 'Peningkatan Derajat Kesehatan Masyarakat dan Penurunan Stunting', opd: 'Dinas Kesehatan Kota Tegal', target: '92%', realisasi: '94.2%', status: 'Melampaui' },
    { kode: 'RS.03', uraian: 'Peningkatan Infrastruktur Drainase & Tanggul Rob Pesisir', opd: 'DPUPR Kota Tegal', target: '85%', realisasi: '87.4%', status: 'Melampaui' },
    { kode: 'RS.04', uraian: 'Daya Saing Sektor Perikanan Tangkap & Kelautan', opd: 'DKPPP Kota Tegal', target: '90%', realisasi: '89.5%', status: 'Sesuai Target' }
  ],
  renja: [
    { kode: 'RJ.01', uraian: 'Pelaksanaan Program Bantuan Siswa Miskin Berprestasi', opd: 'Dinas Pendidikan', target: '1.200 Siswa', realisasi: '1.200 Siswa', status: 'Selesai 100%' },
    { kode: 'RJ.02', uraian: 'Operasionalisasi Pompa Polder Kawasan Muarareja & Tegalsari', opd: 'DPUPR', target: '12 Pompa', realisasi: '12 Pompa', status: 'Optimal' },
    { kode: 'RJ.03', uraian: 'Pengadaan Sarana Cold Storage Perikanan Rakyat', opd: 'DKPPP', target: '2 Unit', realisasi: '2 Unit', status: 'Selesai' }
  ],
  perjanjian_kinerja: [
    { kode: 'PK.01', uraian: 'Pencapaian Nilai Indeks Kepuasan Masyarakat (IKM) Minimal 88.0', opd: 'Bagian Organisasi Setda', target: '88.0 Poin', realisasi: '91.2 Poin', status: 'Tercapai' },
    { kode: 'PK.02', uraian: 'Tingkat Kematangan Penyelenggaraan SPBE Terpadu', opd: 'Diskominfo Kota Tegal', target: '3.80 (Baik)', realisasi: '3.92 (Sangat Baik)', status: 'Melampaui' },
    { kode: 'PK.03', uraian: 'Opini Laporan Keuangan Pemerintah Daerah Wajar Tanpa Pengecualian', opd: 'BKD & Inspektorat', target: 'WTP', realisasi: 'WTP (BPK RI)', status: 'Tercapai' }
  ],
  capaian_kinerja: [
    { kode: 'CK.01', uraian: 'Capaian Kinerja Triwulan I TA 2026 (Fisik & Keuangan)', opd: 'Seluruh OPD Kota Tegal', target: '25%', realisasi: '28.4%', status: 'On Track' },
    { kode: 'CK.02', uraian: 'Capaian Kinerja Triwulan II TA 2026 (Fisik & Keuangan)', opd: 'Seluruh OPD Kota Tegal', target: '50%', realisasi: '54.8%', status: 'On Track' },
    { kode: 'CK.03', uraian: 'Capaian Kinerja Triwulan III TA 2026 (Bulan Berjalan)', opd: 'Seluruh OPD Kota Tegal', target: '75%', realisasi: '82.3%', status: 'Melampaui' }
  ],
  sdgs: [
    { kode: 'SDG.01', uraian: 'Tujuan 1: Tanpa Kemiskinan (Pengentasan Kemiskinan Ekstrem)', opd: 'Dinas Sosial & Bapperida', target: '0.00%', realisasi: '0.45%', status: 'Progres Positif' },
    { kode: 'SDG.03', uraian: 'Tujuan 3: Kehidupan Sehat dan Sejahtera (Universal Health Coverage)', opd: 'Dinas Kesehatan', target: '98.0%', realisasi: '99.2%', status: 'Tercapai' },
    { kode: 'SDG.06', uraian: 'Tujuan 6: Air Bersih dan Sanitasi Layak bagi Seluruh Warga', opd: 'DPUPR & Perumda Tirta', target: '90.0%', realisasi: '92.5%', status: 'Tercapai' },
    { kode: 'SDG.14', uraian: 'Tujuan 14: Ekosistem Lautan dan Konservasi Pesisir Berkelanjutan', opd: 'DKPPP & DLH', target: '100%', realisasi: '100%', status: 'Tercapai' }
  ],
  dak: [
    { kode: 'DAK.01', uraian: 'DAK Fisik Bidang Kesehatan (Penguatan Sarana Puskesmas)', opd: 'Dinas Kesehatan', target: 'Rp 18,5 M', realisasi: 'Rp 17,9 M', status: 'Serapan 96.8%' },
    { kode: 'DAK.02', uraian: 'DAK Fisik Bidang Kelautan dan Perikanan (TPI Tegalsari)', opd: 'DKPPP Kota Tegal', target: 'Rp 12,2 M', realisasi: 'Rp 11,8 M', status: 'Serapan 97.2%' },
    { kode: 'DAK.03', uraian: 'DAK Fisik Bidang Jalan dan Jembatan Perkotaan', opd: 'DPUPR Kota Tegal', target: 'Rp 24,0 M', realisasi: 'Rp 23,4 M', status: 'Serapan 97.5%' }
  ],
  sinkronisasi_serapan: [
    { kode: 'SINK.01', uraian: 'Rekonsiliasi Realisasi Belanja Barang/Jasa vs SP2D Kasda', opd: 'BKD & Seluruh OPD', target: '100%', realisasi: '100%', status: 'Sinkron' },
    { kode: 'SINK.02', uraian: 'Sinkronisasi Data Realisasi Fisik SIMLABA dengan BPKAD', opd: 'Bapperida & BKD', target: '100%', realisasi: '100%', status: 'Sinkron' }
  ],
  pelaporan_kinerja: [
    { kode: 'LAP.01', uraian: 'Pelaporan Kinerja Triwulan III Subkegiatan Perangkat Daerah', opd: '34 OPD Kota Tegal', target: '34 OPD', realisasi: '34 OPD (Lengkap)', status: 'Terverifikasi' },
    { kode: 'LAP.02', uraian: 'Pelaporan Fisik Pekerjaan Konstruksi dan Pengadaan Terbuka', opd: 'Bagian PBJ Setda', target: '418 Paket', realisasi: '418 Paket', status: 'Terverifikasi' }
  ],
  evaluasi_kinerja: [
    { kode: 'EV.01', uraian: 'Evaluasi Dampak Program Pengentasan Kemiskinan Terpadu', opd: 'Bapperida & Tim Koordinasi', target: 'Laporan Final', realisasi: 'Terselesaikan', status: 'Efektif' },
    { kode: 'EV.02', uraian: 'Evaluasi Manfaat Sistem Polder dan Tanggul Rob Pantai', opd: 'DPUPR & Bapperida', target: 'Bebas Genangan', realisasi: 'Genangan Turun 95%', status: 'Sangat Efektif' }
  ]
}

const tableData = computed(() => {
  return sampleDataMap[props.appId] || [
    { kode: 'MOD.01', uraian: `Data Perencanaan ${currentApp.value.title}`, opd: 'Perangkat Daerah Pengampu', target: '100%', realisasi: '95%', status: 'Sesuai Target' }
  ]
})

const filteredRows = computed(() => {
  if (!searchQuery.value) return tableData.value
  const q = searchQuery.value.toLowerCase()
  return tableData.value.filter(r => r.uraian.toLowerCase().includes(q) || r.kode.toLowerCase().includes(q) || r.opd.toLowerCase().includes(q))
})

const showSwal = (title, text) => {
  Swal.fire({
    title,
    text,
    icon: 'info',
    confirmButtonColor: '#308e87',
    timer: 2000
  })
}
</script>
