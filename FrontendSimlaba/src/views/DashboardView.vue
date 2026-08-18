<template>
  <div class="space-y-6 pb-12">
    
    <!-- Executive Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] dark:from-[#0f1729] dark:via-[#162032] dark:to-[#1a2940] p-7 sm:p-8 transition-colors duration-300">
      <div class="absolute inset-0 opacity-[0.05]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;40&quot; height=&quot;40&quot; viewBox=&quot;0 0 40 40&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot; fill-rule=&quot;evenodd&quot;%3E%3Cpath d=&quot;M0 40L40 0H20L0 20M40 40V20L20 40&quot;/%3E%3C/g%3E%3C/svg%3E')"></div>
      <div class="absolute -top-16 -right-16 w-56 h-56 bg-[#3aada4]/20 rounded-full blur-[80px]"></div>
      <div class="absolute -bottom-12 -left-12 w-44 h-44 bg-[#f39159]/15 rounded-full blur-[70px]"></div>

      <div class="relative z-10 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          
          <h1 class="text-2xl sm:text-3xl font-black tracking-tight text-white leading-tight">
            Simlaba Kota Tegal
          </h1>
          <p class="text-xs text-[#3aada4] mt-1.5 font-semibold">Sistem Informasi Laporan Perkembangan Pembangunan - Bagian Pengadaan Barang dan Jasa, dan Administrasi Pembangunan Setda Kota Tegal

</p>
        </div>

        <div class="flex items-center space-x-2">
          <div class="bg-emerald-500/20 backdrop-blur border border-emerald-400/30 px-3.5 py-2 rounded-xl flex items-center space-x-2">
            <span class="relative flex h-2.5 w-2.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400"></span>
            </span>
            
          </div>
        </div>
      </div>
    </div>

    <!-- 4 Metric Cards with full color -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      
      <!-- Total Anggaran -->
      <div class="bg-white dark:bg-[#141d30] p-5 rounded-2xl border-2 border-blue-100 dark:border-blue-900/30 shadow-sm shadow-blue-100/50 dark:shadow-blue-900/10 hover:shadow-lg hover:shadow-blue-200/50 dark:hover:shadow-blue-900/20 transition-all duration-300 group">
        <div class="flex items-center justify-between">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center shadow-md shadow-blue-500/25">
            <Wallet class="w-5 h-5" />
          </div>
          <span class="text-[10px] font-black text-blue-500 dark:text-blue-400 uppercase tracking-wider">Total Anggaran</span>
        </div>
        <h3 class="text-lg font-black text-slate-900 dark:text-white tracking-tight mt-3 leading-tight">
          {{ formatRupiah(summary.total_anggaran) }}
        </h3>
        <p class="text-xs text-blue-500/70 dark:text-blue-400/60 mt-1 font-semibold"></p>
      </div>

      <!-- Serapan -->
      <div class="bg-white dark:bg-[#141d30] p-5 rounded-2xl border-2 border-[#308e87]/20 dark:border-[#308e87]/15 shadow-sm shadow-[#308e87]/10 dark:shadow-[#308e87]/5 hover:shadow-lg hover:shadow-[#308e87]/20 dark:hover:shadow-[#308e87]/10 transition-all duration-300 group">
        <div class="flex items-center justify-between">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#308e87] to-[#3aada4] text-white flex items-center justify-center shadow-md shadow-[#308e87]/25">
            <Coins class="w-5 h-5" />
          </div>
          <span class="text-[10px] font-black text-[#308e87] dark:text-[#3aada4] uppercase tracking-wider">Serapan Anggaran</span>
        </div>
        <h3 class="text-lg font-black text-[#308e87] dark:text-[#3aada4] tracking-tight mt-3 leading-tight">
          {{ formatRupiah(summary.serapan_anggaran) }}
        </h3>
        <div class="flex items-center space-x-2 mt-1">
          <span class="text-xs font-black text-white bg-[#308e87] px-2 py-0.5 rounded-md shadow-sm shadow-[#308e87]/20">{{ summary.serapan_persen }}%</span>
          <span class="text-xs text-[#308e87]/70 dark:text-[#3aada4]/60 font-semibold"></span>
        </div>
      </div>

      <!-- Realisasi Fisik -->
      <div class="bg-white dark:bg-[#141d30] p-5 rounded-2xl border-2 border-[#f39159]/20 dark:border-[#f39159]/15 shadow-sm shadow-[#f39159]/10 dark:shadow-[#f39159]/5 hover:shadow-lg hover:shadow-[#f39159]/20 dark:hover:shadow-[#f39159]/10 transition-all duration-300 group">
        <div class="flex items-center justify-between">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#f39159] to-[#e07a3e] text-white flex items-center justify-center shadow-md shadow-[#f39159]/25">
            <Activity class="w-5 h-5" />
          </div>
          <span class="text-[10px] font-black text-[#f39159] dark:text-[#f8b088] uppercase tracking-wider">Realisasi Fisik</span>
        </div>
        <h3 class="text-lg font-black text-[#f39159] dark:text-[#f8b088] tracking-tight mt-3 leading-tight">
          {{ summary.realisasi_fisik }}%
        </h3>
        <p class="text-xs text-[#f39159]/70 dark:text-[#f8b088]/60 mt-1 font-semibold">Bulan ke-{{ summary.bulan_terakhir || 8 }} </p>
      </div>

      <!-- Deviasi -->
      <div class="bg-white dark:bg-[#141d30] p-5 rounded-2xl border-2 transition-all duration-300 group"
           :class="summary.deviasi >= 0 
             ? 'border-emerald-200 dark:border-emerald-900/30 shadow-sm shadow-emerald-100/50 hover:shadow-lg hover:shadow-emerald-200/50' 
             : 'border-rose-200 dark:border-rose-900/30 shadow-sm shadow-rose-100/50 hover:shadow-lg hover:shadow-rose-200/50'"
      >
        <div class="flex items-center justify-between">
          <div class="w-10 h-10 rounded-xl text-white flex items-center justify-center shadow-md"
               :class="summary.deviasi >= 0 ? 'bg-gradient-to-br from-emerald-500 to-green-600 shadow-emerald-500/25' : 'bg-gradient-to-br from-rose-500 to-red-600 shadow-rose-500/25'">
            <TrendingUp class="w-5 h-5" />
          </div>
          <span class="text-[10px] font-black uppercase tracking-wider"
                :class="summary.deviasi >= 0 ? 'text-emerald-500 dark:text-emerald-400' : 'text-rose-500 dark:text-rose-400'">Deviasi</span>
        </div>
        <h3 class="text-lg font-black tracking-tight mt-3 leading-tight" 
            :class="summary.deviasi >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'">
          {{ summary.deviasi >= 0 ? '+' : '' }}{{ summary.deviasi }}%
        </h3>
        <p class="text-xs mt-1 font-semibold"
           :class="summary.deviasi >= 0 ? 'text-emerald-500/70 dark:text-emerald-400/60' : 'text-rose-500/70 dark:text-rose-400/60'">Realisasi ({{ summary.realisasi_fisik }}%) - Target ({{ summary.target_fisik }}%)</p>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
      
      <!-- Area Chart RFK -->
      <div class="lg:col-span-2 bg-white dark:bg-[#141d30] p-6 rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm">
        <div class="flex items-center justify-between mb-5">
          <div>
            <h2 class="text-base font-black text-slate-900 dark:text-white">Grafik RFK Per Bulan</h2>
            <p class="text-xs text-slate-400 dark:text-slate-500 mt-0.5 font-medium">Realisasi Fisik & Keuangan Bulanan (%)</p>
          </div>
          <div class="flex items-center space-x-3 text-xs font-bold">
            <span class="flex items-center space-x-1.5">
              <span class="w-3 h-3 rounded-full bg-gradient-to-r from-[#308e87] to-[#3aada4] shadow-sm shadow-[#308e87]/30"></span>
              <span class="text-[#308e87] dark:text-[#3aada4]">Fisik</span>
            </span>
            <span class="flex items-center space-x-1.5">
              <span class="w-3 h-3 rounded-full bg-gradient-to-r from-[#f39159] to-[#f8b088] shadow-sm shadow-[#f39159]/30"></span>
              <span class="text-[#f39159] dark:text-[#f8b088]">Keuangan</span>
            </span>
          </div>
        </div>
        <apexchart type="area" height="320" :options="lineChartOptions" :series="lineChartSeries" />
      </div>

      <!-- Donut -->
      <div class="bg-white dark:bg-[#141d30] p-6 rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm flex flex-col">
        <div class="mb-4">
          <h2 class="text-base font-black text-slate-900 dark:text-white">Serapan Anggaran</h2>
          <p class="text-xs text-slate-400 dark:text-slate-500 mt-0.5 font-medium">Proporsi Metode Pengadaan</p>
        </div>
        <div class="flex-1 flex items-center">
          <apexchart type="donut" height="280" :options="pieChartOptions" :series="pieChartSeries" class="w-full" />
        </div>
        <div class="mt-3 pt-3 border-t-2 border-slate-50 dark:border-slate-800/50 text-center">
          <p class="text-[10px] text-slate-400 dark:text-slate-500 font-medium">Distribusi metode pengadaan barang & jasa</p>
        </div>
      </div>
    </div>

    <!-- Bar & Ranking -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
      
      <!-- Bar -->
      <div class="bg-white dark:bg-[#141d30] p-6 rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm">
        <div class="mb-4">
          <h2 class="text-base font-black text-slate-900 dark:text-white">Target vs Realisasi</h2>
          <p class="text-xs text-slate-400 dark:text-slate-500 mt-0.5 font-medium">Capaian Progres Triwulan</p>
        </div>
        <apexchart type="bar" height="320" :options="barChartOptions" :series="barChartSeries" />
      </div>

      <!-- OPD Ranking -->
      <div class="lg:col-span-2 bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="flex items-center justify-between p-6 pb-4">
          <div>
            <h2 class="text-base font-black text-slate-900 dark:text-white">Ranking OPD</h2>
            <p class="text-xs text-slate-400 dark:text-slate-500 mt-0.5 font-medium">Kinerja Realisasi Per Perangkat Daerah</p>
          </div>
          <span class="text-[10px] text-white font-black bg-gradient-to-r from-[#308e87] to-[#3aada4] px-3 py-1 rounded-lg shadow-sm shadow-[#308e87]/20 uppercase tracking-wider">Top OPD</span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] uppercase tracking-wider font-black border-y-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-5 w-16">Rank</th>
                <th class="py-3.5 px-5">Perangkat Daerah</th>
                <th class="py-3.5 px-5 text-right">Fisik</th>
                <th class="py-3.5 px-5 text-right">Keuangan</th>
                <th class="py-3.5 px-5 text-center">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50">
              <tr 
                v-for="opd in opdRankings" 
                :key="opd.rank" 
                class="even:bg-slate-50/50 dark:even:bg-slate-800/15 hover:bg-[#308e87]/5 dark:hover:bg-[#308e87]/10 transition-colors"
              >
                <td class="py-3.5 px-5">
                  <span class="w-7 h-7 rounded-lg inline-flex items-center justify-center font-black text-xs"
                        :class="opd.rank <= 3 ? 'bg-gradient-to-br from-[#308e87] to-[#3aada4] text-white shadow-sm shadow-[#308e87]/20' : 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400'">
                    {{ opd.rank }}
                  </span>
                </td>
                <td class="py-3.5 px-5 text-slate-800 dark:text-slate-200 font-bold">{{ opd.nama_opd }}</td>
                <td class="py-3.5 px-5 text-right font-black text-[#308e87] dark:text-[#3aada4]">{{ opd.realisasi_fisik }}%</td>
                <td class="py-3.5 px-5 text-right font-black text-[#f39159] dark:text-[#f8b088]">{{ opd.realisasi_keuangan }}%</td>
                <td class="py-3.5 px-5 text-center">
                  <span class="px-2.5 py-1 rounded-lg text-[10px] font-black"
                        :class="opd.status === 'Sesuai Target' 
                          ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20' 
                          : 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20'">
                    {{ opd.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useTheme } from '@/composables/useTheme'
import { Wallet, Coins, Activity, TrendingUp } from 'lucide-vue-next'

const { isDark } = useTheme()

const summary = ref({
  total_anggaran: 125450000000,
  serapan_anggaran: 87815000000,
  serapan_persen: 70.0,
  realisasi_fisik: 75.4,
  deviasi: 5.4
})

const opdRankings = ref([])

const lineChartOptions = computed(() => ({
  chart: { toolbar: { show: false }, zoom: { enabled: false }, fontFamily: 'Plus Jakarta Sans, sans-serif', background: 'transparent' },
  theme: { mode: isDark.value ? 'dark' : 'light' },
  stroke: { curve: 'smooth', width: 3 },
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.4, opacityTo: 0.05, stops: [0, 90, 100] } },
  colors: ['#308e87', '#f39159'],
  xaxis: { 
    categories: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
    labels: { style: { colors: isDark.value ? '#475569' : '#94a3b8', fontSize: '11px', fontWeight: 600 } },
    axisBorder: { show: false }, axisTicks: { show: false }
  },
  yaxis: { max: 100, labels: { style: { colors: isDark.value ? '#475569' : '#94a3b8', fontSize: '11px', fontWeight: 600 } } },
  grid: { borderColor: isDark.value ? '#1e293b' : '#f1f5f9', strokeDashArray: 4 },
  legend: { show: false }, dataLabels: { enabled: false },
  tooltip: { theme: isDark.value ? 'dark' : 'light' }
}))

const lineChartSeries = ref([
  { name: 'Realisasi Fisik (%)', data: [4.8, 11.5, 18.9, 30.2, 42.1, 56.4, 65.0, 75.2, 82.0, 0, 0, 0] },
  { name: 'Realisasi Keuangan (%)', data: [3.5, 9.2, 16.5, 26.0, 38.2, 50.1, 60.5, 70.0, 78.5, 0, 0, 0] }
])

const pieChartOptions = computed(() => ({
  chart: { background: 'transparent' },
  theme: { mode: isDark.value ? 'dark' : 'light' },
  labels: ["Tender", "Pengadaan Langsung", "Swakelola", "E-Purchasing"],
  colors: ['#308e87', '#f39159', '#3b82f6', '#8b5cf6'],
  stroke: { width: 3, colors: [isDark.value ? '#141d30' : '#ffffff'] },
  legend: { position: 'bottom', fontSize: '11px', labels: { colors: isDark.value ? '#64748b' : '#94a3b8' }, markers: { width: 10, height: 10, radius: 3 } },
  dataLabels: { enabled: true, style: { fontSize: '11px', fontWeight: 700 } },
  plotOptions: { pie: { donut: { size: '62%' } } }
}))

const pieChartSeries = ref([45, 25, 20, 10])

const barChartOptions = computed(() => ({
  chart: { toolbar: { show: false }, fontFamily: 'Plus Jakarta Sans, sans-serif', background: 'transparent' },
  theme: { mode: isDark.value ? 'dark' : 'light' },
  colors: [isDark.value ? '#1e293b' : '#e2e8f0', '#308e87'],
  plotOptions: { bar: { borderRadius: 8, columnWidth: '50%' } },
  dataLabels: { enabled: false },
  xaxis: { 
    categories: ["TW I", "TW II", "TW III", "TW IV"],
    labels: { style: { colors: isDark.value ? '#475569' : '#94a3b8', fontSize: '11px', fontWeight: 600 } },
    axisBorder: { show: false }, axisTicks: { show: false }
  },
  yaxis: { labels: { style: { colors: isDark.value ? '#475569' : '#94a3b8', fontSize: '11px', fontWeight: 600 } } },
  grid: { borderColor: isDark.value ? '#1e293b' : '#f1f5f9', strokeDashArray: 4 },
  tooltip: { theme: isDark.value ? 'dark' : 'light' }
}))

const barChartSeries = ref([
  { name: 'Target (%)', data: [20.0, 58.0, 85.0, 100.0] },
  { name: 'Realisasi (%)', data: [18.9, 56.4, 82.0, 0.0] }
])

const formatRupiah = (val) => {
  if (!val) return 'Rp 0'
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val)
}

import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const fetchData = async () => {
  try {
    const [sumRes, chartRes, opdRes] = await Promise.all([
      axios.get('/api/v1/dashboard/summary'),
      axios.get('/api/v1/dashboard/charts'),
      axios.get('/api/v1/dashboard/opd-ranking')
    ])
    summary.value = sumRes.data

    let opdData = opdRes.data
    const user = authStore.user
    if (user && user.role_id > 5) {
      const allowedOpdIds = user.id_opds || []
      if (allowedOpdIds.length > 0) {
        opdData = opdData.filter(o => allowedOpdIds.includes(o.id_sub_pd))
      } else {
        opdData = []
      }
    }

    opdRankings.value = opdData
    if (chartRes.data.line_rfk) {
      lineChartSeries.value = [
        { name: 'Realisasi Fisik (%)', data: chartRes.data.line_rfk.realisasi_fisik },
        { name: 'Realisasi Keuangan (%)', data: chartRes.data.line_rfk.realisasi_keuangan }
      ]
    }
  } catch (err) {
    console.warn('Menggunakan data dummy dashboard:', err)
  }
}

onMounted(() => fetchData())
</script>
