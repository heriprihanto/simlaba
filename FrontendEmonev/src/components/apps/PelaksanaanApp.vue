<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    <div class="bg-white dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-5 py-3.5 flex items-center justify-between shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 text-white flex items-center justify-center shadow-md">
          <Activity class="w-5 h-5" />
        </div>
        <div>
          <h2 class="text-sm font-black text-slate-900 dark:text-white">Pelaksanaan &amp; Capaian Kinerja</h2>
          <p class="text-[11px] text-slate-500">Monitoring Capaian Triwulanan, SDGs, DAK, dan Evaluasi</p>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="bg-slate-100 dark:bg-[#111c2e] border-b border-slate-200 dark:border-slate-800 px-4 py-2 flex items-center space-x-1 overflow-x-auto no-scrollbar shrink-0">
      <button 
        v-for="t in tabs" 
        :key="t" 
        @click="activeTab = t" 
        class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all shrink-0"
        :class="activeTab === t ? 'bg-white dark:bg-[#1e293b] text-amber-600 font-black shadow-sm' : 'text-slate-600 hover:text-slate-900'"
      >
        {{ t }}
      </button>
    </div>

    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-sm font-black">{{ activeTab }} — Kota Tegal</h3>
          <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/10 text-amber-600">Tahun Anggaran 2026</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed">
          Modul monitoring terpadu untuk pencatatan progres fisik, pelaporan evaluasi program, sinkronisasi serapan keuangan, dan capaian target indikator sasaran pembangunan.
        </p>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50 dark:bg-slate-800/60 font-bold text-slate-500 border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th class="py-2.5 px-4">Program / Subkegiatan</th>
              <th class="py-2.5 px-4 w-40">Perangkat Daerah</th>
              <th class="py-2.5 px-4 text-center w-24">Target Fisik</th>
              <th class="py-2.5 px-4 text-center w-24">Realisasi</th>
              <th class="py-2.5 px-4 text-center w-24">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
            <tr v-for="item in mockData" :key="item.nama" class="hover:bg-slate-50/70">
              <td class="py-2.5 px-4 font-bold">{{ item.nama }}</td>
              <td class="py-2.5 px-4 text-slate-600">{{ item.opd }}</td>
              <td class="py-2.5 px-4 text-center">{{ item.target }}%</td>
              <td class="py-2.5 px-4 text-center font-bold text-emerald-600">{{ item.realisasi }}%</td>
              <td class="py-2.5 px-4 text-center">
                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-600 border border-emerald-200">On Track</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Activity } from 'lucide-vue-next'

const tabs = ['Capaian Kinerja Triwulanan', "SDG's", 'Dana Alokasi Khusus (DAK)', 'Sinkronisasi Serapan', 'Pelaporan Kinerja', 'Evaluasi Kinerja']
const activeTab = ref('Capaian Kinerja Triwulanan')

const mockData = [
  { nama: 'Pembangunan Sabuk Pantai & Polder Muarareja', opd: 'DPUPR', target: 80, realisasi: 84 },
  { nama: 'Peningkatan Kualitas Sarana Puskesmas', opd: 'Dinas Kesehatan', target: 90, realisasi: 92 },
  { nama: 'Bantuan Beasiswa Pendidikan Siswa Miskin', opd: 'Dinas Pendidikan', target: 100, realisasi: 100 },
  { nama: 'Pengembangan Sentra Kuliner Pesisir Tegalsari', opd: 'DKPPP', target: 75, realisasi: 78 }
]
</script>
