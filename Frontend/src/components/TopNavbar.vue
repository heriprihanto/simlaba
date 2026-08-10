<template>
  <header class="sticky top-0 z-50 bg-white dark:bg-[#0f1729] border-b-2 border-[#308e87]/20 dark:border-[#308e87]/30 shadow-sm shadow-[#308e87]/5 dark:shadow-black/20 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Brand -->
        <div class="flex items-center space-x-3 cursor-pointer group select-none" @click="$router.push('/')">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#308e87] via-[#3aada4] to-[#245f5a] flex items-center justify-center text-white font-black text-lg shadow-lg shadow-[#308e87]/30 group-hover:shadow-[#308e87]/40 group-hover:scale-105 transition-all">
            S
          </div>
          <div class="hidden sm:block">
            <div class="flex items-center space-x-1.5">
              <span class="font-black text-base text-slate-900 dark:text-white tracking-tight">SIMLABA</span>
              <span class="bg-gradient-to-r from-[#308e87] to-[#3aada4] text-white text-[9px] font-black px-2 py-0.5 rounded-md shadow-sm">2026</span>
            </div>
            <p class="text-[10px] text-[#308e87] dark:text-[#3aada4] font-bold leading-none mt-0.5 uppercase tracking-wider">Kota Tegal</p>
          </div>
        </div>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center bg-nav-slate-50 dark:bg-slate-800/50 rounded-xl p-1 space-x-0.5 border border-slate-200/80 dark:border-slate-700/50">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="px-3.5 py-2 rounded-lg text-xs font-bold transition-all duration-200 flex items-center space-x-1.5"
            :class="[
              $route.path === item.path 
                ? 'bg-[#308e87] text-white shadow-md shadow-[#308e87]/30' 
                : 'text-slate-600 dark:text-slate-400 hover:text-[#308e87] dark:hover:text-[#3aada4] hover:bg-white dark:hover:bg-slate-700/50'
            ]"
          >
            <component :is="item.icon" class="w-4 h-4" />
            <span>{{ item.label }}</span>
          </router-link>
        </nav>

        <!-- Right Controls -->
        <div class="flex items-center space-x-2">
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

      <!-- Mobile Nav -->
      <div class="flex md:hidden overflow-x-auto py-2 space-x-1.5 border-t border-[#308e87]/10 dark:border-[#308e87]/20 no-scrollbar">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="px-3 py-1.5 rounded-lg text-[11px] font-bold whitespace-nowrap flex items-center space-x-1.5 shrink-0 transition-colors"
          :class="[
            $route.path === item.path 
              ? 'bg-[#308e87] text-white shadow-sm shadow-[#308e87]/25' 
              : 'bg-[#308e87]/8 dark:bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]'
          ]"
        >
          <component :is="item.icon" class="w-3.5 h-3.5" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import { 
  LayoutDashboard, Users, ClipboardList, TrendingUp, 
  FileText, Settings, Map, LogOut, Sun, Moon
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()

const navItems = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Personel', path: '/personel', icon: Users },
  { label: 'RKO', path: '/rko', icon: ClipboardList },
  { label: 'RFK', path: '/rfk', icon: TrendingUp },
  { label: 'Laporan', path: '/laporan', icon: FileText },
  { label: 'Pengaturan', path: '/pengaturan', icon: Settings },
  { label: 'Peta', path: '/peta', icon: Map }
]

const userName = computed(() => authStore.userFullName)
const userInitial = computed(() => (userName.value.charAt(0) || 'A').toUpperCase())

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
