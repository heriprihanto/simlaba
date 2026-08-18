<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    <div class="bg-white dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-5 py-3.5 flex items-center justify-between shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-700 text-white flex items-center justify-center shadow-md">
          <FileText class="w-5 h-5" />
        </div>
        <div>
          <h2 class="text-sm font-black text-slate-900 dark:text-white">Laporan Perkembangan Pembangunan</h2>
          <p class="text-[11px] text-slate-500">Cetak &amp; Ekspor Laporan Triwulanan, Tahunan, dan Realisasi Fisik Keuangan</p>
        </div>
      </div>

      <button 
        @click="showSwal('Cetak Laporan', 'Formulir pencetakan laporan siap.')"
        class="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-[#308e87] text-white flex items-center space-x-1.5 shadow-sm"
      >
        <Printer class="w-3.5 h-3.5" />
        <span>Cetak Laporan</span>
      </button>
    </div>

    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="rep in laporanList" :key="rep.judul" class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm space-y-3 hover:border-blue-400 transition-colors">
          <div class="flex items-center justify-between">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400">{{ rep.tipe }}</span>
            <span class="text-[10px] text-slate-400">{{ rep.tgl }}</span>
          </div>
          <h4 class="text-xs font-black text-slate-900 dark:text-white leading-snug">{{ rep.judul }}</h4>
          <p class="text-[11px] text-slate-500">{{ rep.desc }}</p>
          <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center">
            <span class="text-[10px] font-bold text-slate-400">{{ rep.size }}</span>
            <button @click="showSwal('Mengunduh', 'Berkas laporan sedang diunduh.')" class="text-xs font-bold text-blue-600 hover:underline flex items-center space-x-1">
              <Download class="w-3 h-3" />
              <span>Unduh</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Swal from 'sweetalert2'
import { FileText, Printer, Download } from 'lucide-vue-next'

const laporanList = [
  { tipe: 'Laporan Triwulan', judul: 'Laporan Perkembangan Pembangunan Triwulan II 2026', desc: 'Rekapitulasi RFK 34 OPD Kota Tegal', tgl: '15 Juli 2026', size: '4.2 MB PDF' },
  { tipe: 'Laporan Tahunan', judul: 'Laporan Evaluasi Pelaksanaan RPJMD Tahun 2025', desc: 'Capaian 5 Sasaran Strategis Daerah', tgl: '10 Feb 2026', size: '8.7 MB PDF' },
  { tipe: 'Rekapitulasi DAK', judul: 'Laporan Realisasi Penyerapan DAK Fisik 2026', desc: 'Pemantauan Dana Alokasi Khusus Pesisir', tgl: '01 Agustus 2026', size: '2.9 MB PDF' }
]

const showSwal = (title, text) => {
  Swal.fire({ title, text, icon: 'info', confirmButtonColor: '#2563eb', timer: 2000 })
}
</script>
