<template>
  <div class="space-y-6 max-w-[1700px] mx-auto pb-16">
    
    <!-- 1. HEADER SECTION & DOKUMEN BADGE -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-[#141d30] p-6 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-sm">
      <div class="space-y-1.5">
        <div class="flex items-center space-x-2">
          <span class="px-3 py-1 rounded-full text-xs font-black bg-[#308e87]/10 text-[#308e87] border border-[#308e87]/20 uppercase tracking-wider flex items-center space-x-1.5">
            <BookOpen class="w-3.5 h-3.5" />
            <span>Dokumen Perencanaan Jangka Panjang Daerah</span>
          </span>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20">
            20 Tahun (2025–2045)
          </span>
        </div>
        <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
          RPJPD Kota Tegal 2025–2045
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Rencana Pembangunan Jangka Panjang Daerah • Visi, Sasaran Visi, Misi, Arah Kebijakan & Sasaran Pokok
        </p>
      </div>

      <!-- Actions -->
      <div class="flex items-center space-x-2.5">
        <button 
          @click="refreshCurrentTab"
          class="px-3.5 py-2 rounded-2xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all flex items-center space-x-2 cursor-pointer"
          title="Segarkan Data Tab Aktif"
        >
          <RotateCw class="w-4 h-4" />
          <span>Segarkan</span>
        </button>

        <button 
          @click="exportData"
          class="px-4 py-2 rounded-2xl text-xs font-black bg-gradient-to-r from-[#308e87] to-[#236b65] hover:from-[#27756f] hover:to-[#1a524e] text-white shadow-md shadow-[#308e87]/20 transition-all flex items-center space-x-2 cursor-pointer"
        >
          <Download class="w-4 h-4" />
          <span>Export Dokumen</span>
        </button>
      </div>
    </div>

    <!-- 2. TAB NAVIGATION BAR -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        class="flex flex-col p-4 rounded-2xl border text-left transition-all relative overflow-hidden group cursor-pointer"
        :class="activeTab === tab.id 
          ? 'bg-white dark:bg-[#141d30] border-[#308e87] dark:border-[#308e87] shadow-lg shadow-[#308e87]/10 ring-2 ring-[#308e87]/20' 
          : 'bg-white/60 dark:bg-[#141d30]/60 border-slate-200/80 dark:border-slate-800/80 hover:bg-white dark:hover:bg-[#141d30] hover:border-slate-300 dark:hover:border-slate-700'"
      >
        <div class="flex items-center justify-between mb-2">
          <div 
            class="w-8 h-8 rounded-xl flex items-center justify-center transition-colors"
            :class="activeTab === tab.id ? tab.activeIconClass : 'bg-slate-100 dark:bg-slate-800 text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-200'"
          >
            <component :is="tab.icon" class="w-4 h-4" />
          </div>
          <span 
            v-if="tab.badge"
            class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full"
            :class="activeTab === tab.id ? 'bg-[#308e87]/10 text-[#308e87]' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'"
          >
            {{ tab.badge }}
          </span>
        </div>

        <span class="text-xs font-black tracking-tight" :class="activeTab === tab.id ? 'text-slate-900 dark:text-white' : 'text-slate-600 dark:text-slate-400'">
          {{ tab.name }}
        </span>
        <span class="text-[10px] text-slate-400 dark:text-slate-500 mt-0.5 truncate">
          {{ tab.subtitle }}
        </span>

        <!-- Active bottom indicator bar -->
        <div 
          v-if="activeTab === tab.id" 
          class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-[#308e87] to-[#f39159]"
        ></div>
      </button>
    </div>

    <!-- 3. MODULAR TAB CONTENTS -->
    <div class="transition-all duration-200">
      
      <!-- TAB 1: VISI & PENJELASAN VISI -->
      <RpjpdVisiTab 
        v-if="activeTab === 'visi'" 
        ref="visiTabRef"
      />

      <!-- TAB 2: SASARAN VISI & INDIKATOR (TREE TABLE) -->
      <RpjpdSasaranVisiTab 
        v-else-if="activeTab === 'sasaran_visi'" 
        ref="sasaranVisiTabRef"
      />

      <!-- TAB 3: MISI DAERAH -->
      <RpjpdMisiTab 
        v-else-if="activeTab === 'misi'" 
        ref="misiTabRef"
        @selectMisiArah="handleSelectMisiArah"
      />

      <!-- TAB 4: ARAH KEBIJAKAN (4 PERIODE RPJMD) -->
      <RpjpdArahKebijakanTab 
        v-else-if="activeTab === 'arah_kebijakan'" 
        ref="arahTabRef"
        :initialMisi="selectedMisiForArah"
      />

      <!-- TAB 5: SASARAN POKOK & INDIKATOR (TREE TABLE) -->
      <RpjpdSasaranPokokTab 
        v-else-if="activeTab === 'sasaran_pokok'" 
        ref="sasaranPokokTabRef"
      />

    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Swal from 'sweetalert2'
import { 
  BookOpen, Compass, Target, Flag, Milestone, CheckCircle2, 
  RotateCw, Download 
} from 'lucide-vue-next'

// Modular Components per Menu Tab
import RpjpdVisiTab from '@/components/rpjpd/RpjpdVisiTab.vue'
import RpjpdSasaranVisiTab from '@/components/rpjpd/RpjpdSasaranVisiTab.vue'
import RpjpdMisiTab from '@/components/rpjpd/RpjpdMisiTab.vue'
import RpjpdArahKebijakanTab from '@/components/rpjpd/RpjpdArahKebijakanTab.vue'
import RpjpdSasaranPokokTab from '@/components/rpjpd/RpjpdSasaranPokokTab.vue'

const activeTab = ref('visi')
const selectedMisiForArah = ref('')

const visiTabRef = ref(null)
const sasaranVisiTabRef = ref(null)
const misiTabRef = ref(null)
const arahTabRef = ref(null)
const sasaranPokokTabRef = ref(null)

const tabs = computed(() => [
  {
    id: 'visi',
    name: '1. Visi Daerah',
    subtitle: 'Visi & Pokok Penjelasan',
    icon: Compass,
    badge: '4 Pokok',
    activeIconClass: 'bg-[#308e87]/15 text-[#308e87]'
  },
  {
    id: 'sasaran_visi',
    name: '2. Sasaran Visi',
    subtitle: 'Tree: 5 Sasaran & 8 Indikator',
    icon: Target,
    badge: 'Tree Table',
    activeIconClass: 'bg-[#308e87]/15 text-[#308e87]'
  },
  {
    id: 'misi',
    name: '3. Misi Daerah',
    subtitle: '5 Misi Pembangunan',
    icon: Flag,
    badge: '5 Misi',
    activeIconClass: 'bg-[#f39159]/15 text-[#f39159]'
  },
  {
    id: 'arah_kebijakan',
    name: '4. Arah Kebijakan',
    subtitle: 'Periode RPJMD 1 | 2 | 3 | 4',
    icon: Milestone,
    badge: '4 Periode',
    activeIconClass: 'bg-amber-500/15 text-amber-600'
  },
  {
    id: 'sasaran_pokok',
    name: '5. Sasaran Pokok',
    subtitle: 'Tree: 6 Pokok & 57 Indikator',
    icon: CheckCircle2,
    badge: 'Tree Table',
    activeIconClass: 'bg-[#f39159]/15 text-[#f39159]'
  }
])

function refreshCurrentTab() {
  if (activeTab.value === 'visi' && visiTabRef.value) {
    visiTabRef.value.fetchRpjpdVisiData()
  } else if (activeTab.value === 'sasaran_visi' && sasaranVisiTabRef.value) {
    sasaranVisiTabRef.value.fetchSasaranVisiData()
  } else if (activeTab.value === 'misi' && misiTabRef.value) {
    misiTabRef.value.fetchMisiData()
  } else if (activeTab.value === 'arah_kebijakan' && arahTabRef.value) {
    arahTabRef.value.fetchArahKebijakanData()
  } else if (activeTab.value === 'sasaran_pokok' && sasaranPokokTabRef.value) {
    sasaranPokokTabRef.value.fetchSasaranPokokData()
  }
  
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'info',
    title: 'Data sedang disegarkan...',
    showConfirmButton: false,
    timer: 1500
  })
}

function handleSelectMisiArah(idmisi) {
  selectedMisiForArah.value = idmisi
  activeTab.value = 'arah_kebijakan'
  if (arahTabRef.value) {
    arahTabRef.value.setMisiFilter(idmisi)
  }
}

function exportData() {
  Swal.fire({
    title: 'Export Dokumen RPJPD',
    text: 'Pilih format ekspor data perencanaan jangka panjang daerah Kota Tegal:',
    icon: 'question',
    showDenyButton: true,
    showCancelButton: true,
    confirmButtonText: 'Export Excel (.xlsx)',
    denyButtonText: 'Export PDF (.pdf)',
    cancelButtonText: 'Batal',
    confirmButtonColor: '#308e87',
    denyButtonColor: '#f39159'
  }).then((res) => {
    if (res.isConfirmed || res.isDenied) {
      const format = res.isConfirmed ? 'Excel' : 'PDF'
      Swal.fire('Berhasil', `Dokumen RPJPD (${format}) sedang dipersiapkan untuk diunduh.`, 'success')
    }
  })
}
</script>
