<template>
  <div class="h-full flex flex-col bg-white dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    <!-- Explorer Ribbon -->
    <div class="bg-slate-100 dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-4 py-2 flex items-center space-x-2 text-xs">
      <button class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500"><ArrowLeft class="w-4 h-4" /></button>
      <button class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500"><ArrowRight class="w-4 h-4" /></button>
      <button class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500"><ArrowUp class="w-4 h-4" /></button>
      
      <!-- Path bar -->
      <div class="flex-1 bg-white dark:bg-[#0f172a] border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1 flex items-center space-x-1 text-slate-600 dark:text-slate-300 font-medium">
        <Folder class="w-3.5 h-3.5 text-amber-500" />
        <span>Dokumen Perencanaan</span>
        <span>&gt;</span>
        <span>Kota Tegal</span>
      </div>
    </div>

    <!-- Explorer Grid -->
    <div class="flex-1 overflow-y-auto p-4 grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-3">
      <div v-for="f in files" :key="f.name" class="flex flex-col items-center p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800/60 cursor-pointer text-center group">
        <component :is="f.icon" class="w-10 h-10 mb-1.5 transition-transform group-hover:scale-105" :class="f.color" />
        <span class="text-xs font-bold text-slate-800 dark:text-slate-200 break-all leading-tight">{{ f.name }}</span>
        <span class="text-[10px] text-slate-400 mt-0.5">{{ f.type }}</span>
      </div>
    </div>

    <!-- Status bar -->
    <div class="bg-slate-100 dark:bg-[#141d30] border-t border-slate-200 dark:border-slate-800 px-3 py-1 text-[11px] text-slate-500 flex justify-between">
      <span>{{ files.length }} item</span>
      <span>Penyimpanan Sistem EMONEV</span>
    </div>
  </div>
</template>

<script setup>
import { ArrowLeft, ArrowRight, ArrowUp, Folder, FileText, FileSpreadsheet, FileArchive } from 'lucide-vue-next'

const files = [
  { name: 'RPJPD_2025_2045.pdf', type: 'PDF Dokumen', icon: FileText, color: 'text-red-500' },
  { name: 'RPJMD_2025_2029.pdf', type: 'PDF Dokumen', icon: FileText, color: 'text-red-500' },
  { name: 'Matriks_IKU_IKD.xlsx', type: 'Excel Spreadsheet', icon: FileSpreadsheet, color: 'text-emerald-500' },
  { name: 'Renstra_34_OPD', type: 'Folder Berkas', icon: Folder, color: 'text-amber-500' },
  { name: 'Lampiran_DPA_2026.zip', type: 'Arsip Berkas', icon: FileArchive, color: 'text-purple-500' },
  { name: 'Peta_Spasial_GIS.geojson', type: 'Data Spasial', icon: FileText, color: 'text-blue-500' }
]
</script>
