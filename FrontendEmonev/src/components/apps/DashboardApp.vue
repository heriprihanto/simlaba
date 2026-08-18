<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-y-auto p-5 space-y-5 select-none">
    
    <!-- Top Metric Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-bold">Total Pagu APBD 2026</span>
          <div class="w-8 h-8 rounded-lg bg-teal-500/10 text-teal-600 flex items-center justify-center">
            <Coins class="w-4 h-4" />
          </div>
        </div>
        <p class="text-xl font-black text-slate-900 dark:text-white">Rp 1,32 Triliun</p>
        <span class="text-[10px] text-teal-600 font-bold mt-1 block">100% Pagu DPA Terdistribusi</span>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-bold">Serapan Keuangan</span>
          <div class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-600 flex items-center justify-center">
            <TrendingUp class="w-4 h-4" />
          </div>
        </div>
        <p class="text-xl font-black text-slate-900 dark:text-white">74.85%</p>
        <span class="text-[10px] text-emerald-600 font-bold mt-1 block">+2.4% di atas target triwulan</span>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-bold">Realisasi Fisik</span>
          <div class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-600 flex items-center justify-center">
            <CheckCircle2 class="w-4 h-4" />
          </div>
        </div>
        <p class="text-xl font-black text-slate-900 dark:text-white">82.30%</p>
        <span class="text-[10px] text-amber-600 font-bold mt-1 block">Deviasi Fisik +1.8%</span>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm">
        <div class="flex items-center justify-between text-slate-500 mb-2">
          <span class="text-xs font-bold">Paket Pekerjaan OPD</span>
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-600 flex items-center justify-center">
            <Briefcase class="w-4 h-4" />
          </div>
        </div>
        <p class="text-xl font-black text-slate-900 dark:text-white">418 Paket</p>
        <span class="text-[10px] text-purple-600 font-bold mt-1 block">34 Perangkat Daerah Aktif</span>
      </div>
    </div>

    <!-- Charts / Progress Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      <!-- Serapan Per Triwulan -->
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-500">Progres Serapan Anggaran Triwulanan</h3>
        <div class="space-y-3 pt-2">
          <div v-for="q in triwulanan" :key="q.name" class="space-y-1">
            <div class="flex justify-between text-xs font-bold">
              <span>{{ q.name }}</span>
              <span>{{ q.serapan }}%</span>
            </div>
            <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2 overflow-hidden">
              <div class="bg-gradient-to-r from-teal-500 to-emerald-500 h-2 rounded-full" :style="{ width: q.serapan + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Top 5 OPD Kinerja Tertinggi -->
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
        <h3 class="text-xs font-black uppercase tracking-wider text-slate-500">Top 5 Kinerja Perangkat Daerah</h3>
        <div class="divide-y divide-slate-100 dark:divide-slate-800 text-xs">
          <div v-for="(opd, idx) in topOpd" :key="opd.nama" class="py-2 flex items-center justify-between">
            <div class="flex items-center space-x-2.5">
              <span class="w-5 h-5 rounded-full bg-slate-100 dark:bg-slate-800 text-center font-bold text-[10px] flex items-center justify-center">{{ idx + 1 }}</span>
              <span class="font-bold text-slate-900 dark:text-white">{{ opd.nama }}</span>
            </div>
            <span class="font-black text-emerald-600 dark:text-emerald-400">{{ opd.nilai }}%</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { Coins, TrendingUp, CheckCircle2, Briefcase } from 'lucide-vue-next'

const triwulanan = [
  { name: 'Triwulan I (Jan – Mar)', serapan: 92 },
  { name: 'Triwulan II (Apr – Jun)', serapan: 88 },
  { name: 'Triwulan III (Jul – Sep)', serapan: 75 },
  { name: 'Triwulan IV (Okt – Des)', serapan: 44 }
]

const topOpd = [
  { nama: 'Dinas Kesehatan Kota Tegal', nilai: '94.2' },
  { nama: 'Dinas Pendidikan dan Kebudayaan', nilai: '91.8' },
  { nama: 'DKPPP Kota Tegal', nilai: '89.5' },
  { nama: 'DPUPR Kota Tegal', nilai: '87.4' },
  { nama: 'Diskominfo Kota Tegal', nilai: '86.1' }
]
</script>
