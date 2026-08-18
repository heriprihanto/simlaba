<template>
  <div class="h-full flex flex-col bg-white dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    <div class="flex-1 flex flex-col items-center justify-center p-6 text-center">
      <div class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-400 flex items-center justify-center mb-3">
        <Trash2 class="w-8 h-8" />
      </div>
      <h3 class="text-sm font-black text-slate-700 dark:text-slate-300">Tempat Sampah Kosong</h3>
      <p class="text-xs text-slate-400 mt-1 max-w-xs">Tidak ada berkas atau data perencanaan yang terhapus.</p>
    </div>
  </div>
</template>

<script setup>
import { Trash2 } from 'lucide-vue-next'
</script>
