<template>
  <div class="min-h-[70vh] flex items-center justify-center py-12">
    <div class="text-center max-w-sm">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#308e87] to-[#3aada4] text-white inline-flex items-center justify-center mb-4 shadow-xl shadow-[#308e87]/25">
        <FolderGit2 class="w-8 h-8" />
      </div>

      <h2 class="text-xl font-black text-slate-900 dark:text-white tracking-tight">{{ title }}</h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 leading-relaxed font-medium max-w-xs mx-auto">{{ description }}</p>

      <div class="mt-6 pt-4 border-t-2 border-slate-100 dark:border-slate-800/50 flex items-center justify-center">
        <span class="inline-flex items-center px-3 py-1.5 rounded-xl text-xs font-black bg-[#f39159]/10 text-[#f39159] dark:text-[#f8b088] border border-[#f39159]/20 shadow-sm shadow-[#f39159]/5">
          <Clock class="w-4 h-4 mr-1.5" />
          Tahap Pengembangan
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FolderGit2, Clock } from 'lucide-vue-next'

defineProps({
  title: { type: String, default: 'Halaman Modul' },
  description: { type: String, default: 'Halaman modul ini disiapkan untuk integrasi data fitur berikutnya.' }
})
</script>
