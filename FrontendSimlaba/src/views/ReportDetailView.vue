<template>
  <div class="min-h-screen bg-slate-100 dark:bg-[#0b132b] text-slate-800 dark:text-slate-100 p-4 sm:p-8 print:p-0 print:bg-white print:text-black">
    
    <!-- Top Action Bar (Hidden when printing) -->
    <div class="max-w-6xl mx-auto mb-6 flex flex-col sm:flex-row items-center justify-between gap-4 print:hidden">
      <div class="flex items-center space-x-3">
        <button 
          @click="closeWindow" 
          class="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold hover:bg-slate-50 transition-colors inline-flex items-center space-x-1.5 cursor-pointer"
        >
          <ArrowLeft class="w-4 h-4" />
          <span>Tutup Jendela</span>
        </button>
        <span class="text-xs font-bold text-slate-400">
          Pratinjau Dokumen Laporan SIMLABA
        </span>
      </div>

      <div class="flex items-center space-x-2">
        <button 
          @click="printReport" 
          class="px-5 py-2.5 rounded-xl bg-[#308e87] hover:bg-[#25736d] text-white font-black text-xs transition-all shadow-md inline-flex items-center space-x-2 cursor-pointer active:scale-95"
        >
          <Printer class="w-4 h-4" />
          <span>Cetak / Cetak PDF</span>
        </button>
      </div>
    </div>

    <!-- Report Paper Container -->
    <div class="max-w-6xl mx-auto bg-white dark:bg-[#141d30] print:bg-white print:text-black rounded-3xl print:rounded-none border border-slate-200 dark:border-slate-800 print:border-none shadow-2xl print:shadow-none p-6 sm:p-10 space-y-6">
      
      <!-- Kop Header -->
      <div class="border-b-2 border-slate-900 dark:border-slate-100 print:border-black pb-4 text-center space-y-1">
        <h2 class="text-lg sm:text-xl font-black uppercase tracking-wider text-slate-900 dark:text-white print:text-black">
          PEMERINTAH KOTA TEGAL
        </h2>
        <h3 class="text-sm sm:text-base font-extrabold uppercase text-slate-800 dark:text-slate-200 print:text-black">
          SISTEM INFORMASI LAPORAN PERKEMBANGAN PEMBANGUNAN (SIMLABA)
        </h3>
        <p class="text-xs font-bold text-slate-500 dark:text-slate-400 print:text-slate-600">
          {{ reportTitle }}
        </p>
      </div>

      <!-- Parameter Information Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-semibold bg-slate-50 dark:bg-slate-800/40 print:bg-slate-50 p-4 rounded-2xl border border-slate-200 dark:border-slate-700/60 print:border-slate-200">
        <div>
          <span class="text-slate-400 block text-[10px] font-bold uppercase">Perangkat Daerah (OPD):</span>
          <span class="font-extrabold text-slate-900 dark:text-white print:text-black">{{ opdName }}</span>
        </div>
        <div>
          <span class="text-slate-400 block text-[10px] font-bold uppercase">Tahun Anggaran:</span>
          <span class="font-extrabold text-slate-900 dark:text-white print:text-black">T.A. {{ tahun }}</span>
        </div>
        <div>
          <span class="text-slate-400 block text-[10px] font-bold uppercase">Periode Laporan:</span>
          <span class="font-extrabold text-slate-900 dark:text-white print:text-black">{{ bulanLabel }}</span>
        </div>
        <div>
          <span class="text-slate-400 block text-[10px] font-bold uppercase">Format Output:</span>
          <span class="font-extrabold uppercase text-[#308e87] dark:text-[#3aada4] print:text-black">{{ formatOutput }}</span>
        </div>
      </div>

      <!-- Report Body / Data Loading -->
      <div v-if="loading" class="py-16 text-center">
        <Loader2 class="w-8 h-8 animate-spin mx-auto mb-2 text-[#308e87]" />
        <span class="font-bold text-xs text-slate-400">Memuat data laporan...</span>
      </div>

      <div v-else class="space-y-6">
        <!-- Sample/Generated Report Table -->
        <div class="overflow-x-auto rounded-2xl border border-slate-200 dark:border-slate-800 print:border-slate-300">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-100 dark:bg-slate-800 print:bg-slate-100 text-slate-800 dark:text-slate-200 print:text-black font-black uppercase text-[10px] border-b border-slate-200 dark:border-slate-700">
                <th class="py-3 px-4 w-12 text-center">No</th>
                <th class="py-3 px-4">Program / Kegiatan / Pekerjaan</th>
                <th class="py-3 px-4 text-right">Pagu Anggaran</th>
                <th class="py-3 px-4 text-center">Realisasi Fisik</th>
                <th class="py-3 px-4 text-right">Realisasi Keuangan</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800 print:divide-slate-200 font-semibold">
              <tr v-for="(item, idx) in reportRows" :key="idx" class="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                <td class="py-2.5 px-4 text-center font-mono text-slate-400">{{ idx + 1 }}</td>
                <td class="py-2.5 px-4 font-bold text-slate-900 dark:text-white print:text-black">{{ item.nama }}</td>
                <td class="py-2.5 px-4 text-right font-mono">{{ formatRupiah(item.anggaran) }}</td>
                <td class="py-2.5 px-4 text-center font-mono text-emerald-600 dark:text-emerald-400 font-bold">{{ item.fisik }}%</td>
                <td class="py-2.5 px-4 text-right font-mono text-blue-600 dark:text-blue-400 font-bold">{{ formatRupiah(item.keuangan) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Footer Sign / Note -->
        <div class="pt-8 flex justify-end text-xs">
          <div class="text-right space-y-1 font-bold">
            <p class="text-slate-800 dark:text-slate-200 print:text-black">{{ footerText }}</p>
            <p class="text-[10px] text-slate-400 font-mono">Dicetak melalui SIMLABA Kota Tegal</p>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ArrowLeft, Printer, Loader2 } from 'lucide-vue-next'

const route = useRoute()
const reportId = computed(() => route.params.id || 'rko_semua')

const idSubPd = computed(() => route.query.id_sub_pd || null)
const tahun = computed(() => route.query.tahun || 2026)
const bulan = computed(() => Number(route.query.bulan || 0))
const footerText = computed(() => route.query.footer_text || 'Tegal')
const formatOutput = computed(() => route.query.format || 'web')

const loading = ref(true)
const opdName = ref('Semua Perangkat Daerah (Kota Tegal)')
const reportTitle = ref('Laporan SIMLABA')
const reportRows = ref([])

const monthNames = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]

const bulanLabel = computed(() => {
  if (bulan.value > 0 && bulan.value <= 12) {
    return `Bulan ${bulan.value} - ${monthNames[bulan.value - 1]}`
  }
  return 'Semua Bulan (Tahunan)'
})

const formatRupiah = (val) => {
  if (val === null || val === undefined) return 'Rp 0'
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(val)
}

const printReport = () => {
  window.print()
}

const closeWindow = () => {
  window.close()
}

const fetchReportData = async () => {
  loading.value = true
  try {
    if (idSubPd.value) {
      const resOpd = await axios.get('/api/v1/personel/opd')
      const found = resOpd.data.find(o => String(o.id_sub_pd) === String(idSubPd.value))
      if (found) {
        opdName.value = `[${found.kode}] ${found.nama_pd}`
      }
    }

    reportTitle.value = `LAPORAN HASIL PELAKSANAAN (${reportId.value.toUpperCase()})`

    reportRows.value = [
      { nama: 'Program Penunjang Urusan Pemerintahan Daerah', anggaran: 1250000000, fisik: 85, keuangan: 1062500000 },
      { nama: 'Kegiatan Perencanaan, Penganggaran, dan Evaluasi Kinerja', anggaran: 450000000, fisik: 90, keuangan: 405000000 },
      { nama: 'Kegiatan Pemeliharaan Sarana dan Prasarana Pendukung', anggaran: 300000000, fisik: 75, keuangan: 225000000 },
      { nama: 'Subkegiatan Pelaksanaan Penyusunan Dokumen Evaluasi', anggaran: 150000000, fisik: 95, keuangan: 142500000 }
    ]
  } catch (err) {
    console.warn('Gagal memuat data detail laporan:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchReportData()
})
</script>
