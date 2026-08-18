<template>
  <div class="min-h-[75vh] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-lg bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-black/30 text-center relative overflow-hidden">
      
      <!-- Ambient Glow -->
      <div class="absolute -top-12 -right-12 w-32 h-32 bg-[#308e87]/10 dark:bg-[#308e87]/20 rounded-full blur-2xl"></div>
      <div class="absolute -bottom-12 -left-12 w-32 h-32 bg-[#f39159]/10 dark:bg-[#f39159]/20 rounded-full blur-2xl"></div>

      <!-- Icon -->
      <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-[#308e87] via-[#3aada4] to-[#245f5a] text-white inline-flex items-center justify-center mb-6 shadow-xl shadow-[#308e87]/25 relative z-10">
        <FolderGit2 class="w-10 h-10" />
      </div>

      <!-- Category Tag -->
      <div v-if="pageCategory" class="mb-3">
        <span class="inline-flex items-center px-3 py-1 rounded-lg text-[11px] font-extrabold uppercase tracking-wider bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20">
          {{ pageCategory }}
        </span>
      </div>

      <!-- Title & Description -->
      <h2 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight relative z-10">{{ pageTitle }}</h2>
      <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-2 leading-relaxed font-medium max-w-md mx-auto relative z-10">
        {{ pageDescription }}
      </p>

      <!-- Status Badge -->
      <div class="mt-8 pt-6 border-t border-slate-100 dark:border-slate-800/80 flex flex-wrap items-center justify-center gap-3 relative z-10">
        <span class="inline-flex items-center px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 shadow-sm">
          <Clock class="w-4 h-4 mr-1.5" />
          Modul Dalam Tahap Integrasi Data
        </span>
        <button 
          @click="$router.push('/')"
          class="inline-flex items-center px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
        >
          <ArrowLeft class="w-3.5 h-3.5 mr-1" />
          Kembali ke Beranda
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { FolderGit2, Clock, ArrowLeft } from 'lucide-vue-next'

const props = defineProps({
  title: { type: String, default: '' },
  category: { type: String, default: '' },
  description: { type: String, default: '' }
})

const route = useRoute()

const pageTitle = computed(() => props.title || route.meta?.title || 'Halaman Modul')
const pageCategory = computed(() => props.category || route.meta?.category || '')
const pageDescription = computed(() => props.description || route.meta?.description || 'Halaman modul ini sedang disiapkan untuk integrasi data fitur evaluasi dan monitoring.')
</script>
