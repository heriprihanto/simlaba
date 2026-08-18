<template>
  <header class="sticky top-0 z-50 bg-white/95 dark:bg-[#0f1729]/95 backdrop-blur-md border-b-2 border-[#308e87]/20 dark:border-[#308e87]/30 shadow-sm shadow-[#308e87]/5 dark:shadow-black/20 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Brand -->
        <div class="flex items-center space-x-3 cursor-pointer group select-none shrink-0" @click="$router.push('/')">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#308e87] via-[#3aada4] to-[#245f5a] flex items-center justify-center text-white font-black text-lg shadow-lg shadow-[#308e87]/30 group-hover:shadow-[#308e87]/40 group-hover:scale-105 transition-all">
            E
          </div>
          <div class="hidden sm:block">
            <div class="flex items-center space-x-1.5">
              <span class="font-black text-base text-slate-900 dark:text-white tracking-tight">EMONEV</span>
              <span class="bg-gradient-to-r from-[#308e87] to-[#3aada4] text-white text-[9px] font-black px-2 py-0.5 rounded-md shadow-sm">2027</span>
            </div>
            <p class="text-[10px] text-[#308e87] dark:text-[#3aada4] font-bold leading-none mt-0.5 uppercase tracking-wider">Kota Tegal</p>
          </div>
        </div>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center bg-slate-100/80 dark:bg-slate-800/60 rounded-2xl p-1.5 space-x-1 border border-slate-200/80 dark:border-slate-700/50 relative">
          
          <!-- 1. Beranda -->
          <router-link 
            to="/" 
            class="px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 flex items-center space-x-1.5"
            :class="[
              $route.path === '/' 
                ? 'bg-[#308e87] text-white shadow-md shadow-[#308e87]/30' 
                : 'text-slate-600 dark:text-slate-400 hover:text-[#308e87] dark:hover:text-[#3aada4] hover:bg-white dark:hover:bg-slate-700/60'
            ]"
            @click="closeAllDropdowns"
          >
            <LayoutDashboard class="w-4 h-4" />
            <span>Beranda</span>
          </router-link>

          <!-- 2. Perencanaan (Dropdown) -->
          <div class="relative" ref="perencanaanDropdownRef">
            <button 
              type="button"
              @click="toggleDropdown('perencanaan')"
              class="px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 flex items-center space-x-1.5"
              :class="[
                isPerencanaanActive 
                  ? 'bg-[#308e87] text-white shadow-md shadow-[#308e87]/30' 
                  : openDropdown === 'perencanaan'
                    ? 'bg-white dark:bg-slate-700 text-[#308e87] dark:text-[#3aada4] shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-[#308e87] dark:hover:text-[#3aada4] hover:bg-white dark:hover:bg-slate-700/60'
              ]"
            >
              <CalendarDays class="w-4 h-4" />
              <span>Perencanaan</span>
              <ChevronDown class="w-3.5 h-3.5 transition-transform duration-200" :class="{ 'rotate-180': openDropdown === 'perencanaan' }" />
            </button>

            <!-- Dropdown Menu -->
            <transition name="dropdown-fade">
              <div 
                v-if="openDropdown === 'perencanaan'"
                class="absolute left-0 mt-2 w-56 bg-white dark:bg-[#141d30] border border-slate-200/90 dark:border-slate-700/80 rounded-2xl p-1.5 shadow-2xl shadow-slate-300/50 dark:shadow-black/60 z-50 overflow-hidden"
              >
                <div class="px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-wider text-[#308e87] dark:text-[#3aada4] border-b border-slate-100 dark:border-slate-800 mb-1">
                  Menu Perencanaan
                </div>
                <router-link 
                  v-for="item in perencanaanItems" 
                  :key="item.path" 
                  :to="item.path"
                  class="flex items-center px-3 py-2 rounded-xl text-xs font-bold transition-colors"
                  :class="[
                    $route.path === item.path
                      ? 'bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-[#308e87] dark:hover:text-[#3aada4]'
                  ]"
                  @click="closeAllDropdowns"
                >
                  <span class="w-1.5 h-1.5 rounded-full mr-2" :class="$route.path === item.path ? 'bg-[#308e87]' : 'bg-slate-300 dark:bg-slate-600'"></span>
                  <span>{{ item.label }}</span>
                </router-link>
              </div>
            </transition>
          </div>

          <!-- 3. Pelaksanaan (Dropdown) -->
          <div class="relative" ref="pelaksanaanDropdownRef">
            <button 
              type="button"
              @click="toggleDropdown('pelaksanaan')"
              class="px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 flex items-center space-x-1.5"
              :class="[
                isPelaksanaanActive 
                  ? 'bg-[#308e87] text-white shadow-md shadow-[#308e87]/30' 
                  : openDropdown === 'pelaksanaan'
                    ? 'bg-white dark:bg-slate-700 text-[#308e87] dark:text-[#3aada4] shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-[#308e87] dark:hover:text-[#3aada4] hover:bg-white dark:hover:bg-slate-700/60'
              ]"
            >
              <Activity class="w-4 h-4" />
              <span>Pelaksanaan</span>
              <ChevronDown class="w-3.5 h-3.5 transition-transform duration-200" :class="{ 'rotate-180': openDropdown === 'pelaksanaan' }" />
            </button>

            <!-- Dropdown Menu -->
            <transition name="dropdown-fade">
              <div 
                v-if="openDropdown === 'pelaksanaan'"
                class="absolute left-0 mt-2 w-64 bg-white dark:bg-[#141d30] border border-slate-200/90 dark:border-slate-700/80 rounded-2xl p-1.5 shadow-2xl shadow-slate-300/50 dark:shadow-black/60 z-50 overflow-hidden"
              >
                <div class="px-3 py-1.5 text-[10px] font-extrabold uppercase tracking-wider text-[#308e87] dark:text-[#3aada4] border-b border-slate-100 dark:border-slate-800 mb-1">
                  Menu Pelaksanaan
                </div>
                <router-link 
                  v-for="item in pelaksanaanItems" 
                  :key="item.path" 
                  :to="item.path"
                  class="flex items-center px-3 py-2 rounded-xl text-xs font-bold transition-colors"
                  :class="[
                    $route.path === item.path
                      ? 'bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-[#308e87] dark:hover:text-[#3aada4]'
                  ]"
                  @click="closeAllDropdowns"
                >
                  <span class="w-1.5 h-1.5 rounded-full mr-2" :class="$route.path === item.path ? 'bg-[#308e87]' : 'bg-slate-300 dark:bg-slate-600'"></span>
                  <span class="truncate">{{ item.label }}</span>
                </router-link>
              </div>
            </transition>
          </div>

          <!-- 4. Laporan (Tampilan Tetap) -->
          <router-link 
            to="/laporan" 
            class="px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 flex items-center space-x-1.5"
            :class="[
              $route.path.startsWith('/laporan') || $route.path.startsWith('/report')
                ? 'bg-[#308e87] text-white shadow-md shadow-[#308e87]/30' 
                : 'text-slate-600 dark:text-slate-400 hover:text-[#308e87] dark:hover:text-[#3aada4] hover:bg-white dark:hover:bg-slate-700/60'
            ]"
            @click="closeAllDropdowns"
          >
            <FileText class="w-4 h-4" />
            <span>Laporan</span>
          </router-link>

        </nav>

        <!-- Right Controls -->
        <div class="flex items-center space-x-2 shrink-0">
          <!-- Theme Toggle -->
          <button 
            type="button"
            @click="toggleTheme"
            class="w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 active:scale-90 border"
            :class="isDark 
              ? 'bg-amber-500/10 border-amber-500/30 text-amber-400 hover:bg-amber-500/20' 
              : 'bg-indigo-500/10 border-indigo-500/20 text-indigo-600 hover:bg-indigo-500/20'"
            :title="isDark ? 'Mode Terang' : 'Mode Gelap'"
          >
            <Sun v-if="isDark" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>

          <!-- User -->
          <div class="hidden sm:flex items-center space-x-2 bg-gradient-to-r from-[#f39159]/10 to-[#f39159]/5 dark:from-[#f39159]/15 dark:to-[#f39159]/5 border border-[#f39159]/20 dark:border-[#f39159]/25 px-3 py-1.5 rounded-xl">
            <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#f39159] to-[#e07a3e] text-white font-bold text-xs flex items-center justify-center shadow-sm shadow-[#f39159]/20">
              {{ userInitial }}
            </div>
            <span class="text-xs font-bold text-[#e07a3e] dark:text-[#f8b088] max-w-[100px] truncate">{{ userName }}</span>
          </div>

          <!-- Logout -->
          <button 
            type="button"
            @click="handleLogout"
            class="w-9 h-9 rounded-xl flex items-center justify-center text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 transition-all active:scale-90 border border-transparent hover:border-red-200 dark:hover:border-red-800/50"
            title="Logout"
          >
            <LogOut class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Mobile Nav Horizontal Scrollable -->
      <div class="flex md:hidden overflow-x-auto py-2 space-x-1.5 border-t border-[#308e87]/10 dark:border-[#308e87]/20 no-scrollbar">
        <!-- Beranda -->
        <router-link 
          to="/"
          class="px-3 py-1.5 rounded-lg text-[11px] font-bold whitespace-nowrap flex items-center space-x-1 shrink-0 transition-colors"
          :class="[
            $route.path === '/' 
              ? 'bg-[#308e87] text-white shadow-sm shadow-[#308e87]/25' 
              : 'bg-[#308e87]/8 dark:bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
          ]"
        >
          <LayoutDashboard class="w-3.5 h-3.5" />
          <span>Beranda</span>
        </router-link>

        <!-- Perencanaan Links -->
        <router-link 
          v-for="item in perencanaanItems"
          :key="item.path"
          :to="item.path"
          class="px-3 py-1.5 rounded-lg text-[11px] font-bold whitespace-nowrap flex items-center space-x-1 shrink-0 transition-colors"
          :class="[
            $route.path === item.path 
              ? 'bg-[#308e87] text-white shadow-sm shadow-[#308e87]/25' 
              : 'bg-[#308e87]/8 dark:bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
          ]"
        >
          <span>{{ item.label }}</span>
        </router-link>

        <!-- Pelaksanaan Links -->
        <router-link 
          v-for="item in pelaksanaanItems"
          :key="item.path"
          :to="item.path"
          class="px-3 py-1.5 rounded-lg text-[11px] font-bold whitespace-nowrap flex items-center space-x-1 shrink-0 transition-colors"
          :class="[
            $route.path === item.path 
              ? 'bg-[#308e87] text-white shadow-sm shadow-[#308e87]/25' 
              : 'bg-[#308e87]/8 dark:bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
          ]"
        >
          <span>{{ item.label }}</span>
        </router-link>

        <!-- Laporan -->
        <router-link 
          to="/laporan"
          class="px-3 py-1.5 rounded-lg text-[11px] font-bold whitespace-nowrap flex items-center space-x-1 shrink-0 transition-colors"
          :class="[
            $route.path.startsWith('/laporan') || $route.path.startsWith('/report')
              ? 'bg-[#308e87] text-white shadow-sm shadow-[#308e87]/25' 
              : 'bg-[#308e87]/8 dark:bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
          ]"
        >
          <FileText class="w-3.5 h-3.5" />
          <span>Laporan</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import { 
  LayoutDashboard, CalendarDays, Activity, FileText, 
  ChevronDown, LogOut, Sun, Moon 
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()

const openDropdown = ref(null)
const perencanaanDropdownRef = ref(null)
const pelaksanaanDropdownRef = ref(null)

// 1. Perencanaan Submenu
const perencanaanItems = [
  { label: 'RPJPD', path: '/perencanaan/rpjpd' },
  { label: 'RPJMD', path: '/perencanaan/rpjmd' },
  { label: 'Renstra', path: '/perencanaan/renstra' },
  { label: 'Renja', path: '/perencanaan/renja' },
  { label: 'Perjanjian Kinerja', path: '/perencanaan/perjanjian-kinerja' }
]

// 2. Pelaksanaan Submenu
const pelaksanaanItems = [
  { label: 'Capaian Kinerja Triwulanan', path: '/pelaksanaan/capaian-kinerja-triwulanan' },
  { label: "SDG's", path: '/pelaksanaan/sdgs' },
  { label: 'Dana Alokasi Khusus', path: '/pelaksanaan/dana-alokasi-khusus' },
  { label: 'Sinkronisasi Serapan Anggaran', path: '/pelaksanaan/sinkronisasi-serapan-anggaran' },
  { label: 'Pelaporan Kinerja', path: '/pelaksanaan/pelaporan-kinerja' },
  { label: 'Evaluasi Kinerja', path: '/pelaksanaan/evaluasi-kinerja' }
]

const isPerencanaanActive = computed(() => route.path.startsWith('/perencanaan'))
const isPelaksanaanActive = computed(() => route.path.startsWith('/pelaksanaan'))

const toggleDropdown = (name) => {
  if (openDropdown.value === name) {
    openDropdown.value = null
  } else {
    openDropdown.value = name
  }
}

const closeAllDropdowns = () => {
  openDropdown.value = null
}

const handleClickOutside = (event) => {
  if (
    perencanaanDropdownRef.value && !perencanaanDropdownRef.value.contains(event.target) &&
    pelaksanaanDropdownRef.value && !pelaksanaanDropdownRef.value.contains(event.target)
  ) {
    closeAllDropdowns()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const userName = computed(() => authStore.userFullName)
const userInitial = computed(() => (userName.value.charAt(0) || 'A').toUpperCase())

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
