<template>
  <div 
    @mousedown.stop
    class="fixed bottom-0 left-0 right-0 h-12 bg-[#0c192c]/90 dark:bg-[#09111e]/95 backdrop-blur-xl border-t border-slate-700/50 flex items-center justify-between px-1 select-none z-[999] text-white"
  >
    
    <!-- LEFT SIDE: Start Button, Search, Running Windows Only -->
    <div class="flex items-center space-x-1 h-full">
      
      <!-- Windows Start Button -->
      <button
        @click.stop="toggleStartMenu"
        class="w-12 h-full flex items-center justify-center hover:bg-white/10 active:bg-white/15 transition-all relative group cursor-pointer"
        :class="{ 'bg-white/15 text-[#38bdf8]': windowStore.isStartMenuOpen }"
        title="Start (Windows 10)"
      >
        <div class="grid grid-cols-2 gap-0.5 w-4 h-4">
          <div class="bg-current rounded-[1px]"></div>
          <div class="bg-current rounded-[1px]"></div>
          <div class="bg-current rounded-[1px]"></div>
          <div class="bg-current rounded-[1px]"></div>
        </div>
      </button>

      <!-- Windows Search Box -->
      <div 
        @click.stop="toggleSearch"
        class="hidden sm:flex items-center space-x-2 px-3 h-9 bg-white/10 hover:bg-white/15 rounded-lg text-slate-300 text-xs cursor-pointer border border-white/10 transition-colors w-52 lg:w-60"
      >
        <Search class="w-4 h-4 text-slate-400 shrink-0" />
        <span class="truncate text-xs font-medium text-slate-300">Cari modul EMONEV...</span>
      </div>

      <!-- Taskbar App Icons: ONLY OPEN/RUNNING WINDOWS -->
      <div class="flex items-center space-x-1 h-full pl-1 overflow-x-auto no-scrollbar">
        <button
          v-for="win in windowStore.openWindows"
          :key="win.id"
          @click.stop="windowStore.toggleTaskbarItem(win.id)"
          class="h-full px-3.5 flex items-center space-x-2 relative hover:bg-white/10 active:bg-white/15 transition-all group max-w-[180px] rounded-t-sm cursor-pointer"
          :class="[
            !win.isMinimized && windowStore.activeWindowId === win.id 
              ? 'bg-white/15 text-white' 
              : 'bg-white/5 text-slate-300 hover:text-white'
          ]"
          :title="win.title"
        >
          <component :is="getIcon(win.icon)" class="w-4 h-4 shrink-0 transition-transform group-hover:scale-110" />
          <span class="text-xs font-bold truncate">{{ win.title }}</span>
          
          <!-- Running indicator line -->
          <div 
            class="absolute bottom-0 left-1 right-1 h-0.5 rounded-full transition-all"
            :class="!win.isMinimized && windowStore.activeWindowId === win.id 
              ? 'bg-[#38bdf8] h-1 shadow-sm shadow-[#38bdf8]' 
              : 'bg-slate-400'"
          ></div>
        </button>
      </div>

    </div>

    <!-- RIGHT SIDE: System Tray (Theme Switch, Clock, Notifications, Show Desktop) -->
    <div class="flex items-center h-full text-xs font-medium shrink-0 space-x-0.5">
      
      <!-- Theme Switch (Dark / Light Mode) Button -->
      <button 
        @click.stop="handleThemeToggle"
        class="h-full px-2.5 flex items-center justify-center hover:bg-white/10 transition-colors relative cursor-pointer group"
        :title="isDark ? 'Beralih ke Mode Terang (Light Mode)' : 'Beralih ke Mode Gelap (Dark Mode)'"
      >
        <Sun v-if="isDark" class="w-4 h-4 text-amber-300 group-hover:scale-110 transition-transform" />
        <Moon v-else class="w-4 h-4 text-indigo-400 group-hover:scale-110 transition-transform" />
      </button>

      <!-- Clock & Date (Realtime) -->
      <button 
        @click.stop="toggleCalendar"
        class="h-full px-3 flex flex-col items-end justify-center hover:bg-white/10 transition-colors leading-tight text-right text-[11px] cursor-pointer"
        :class="{ 'bg-white/15 text-[#38bdf8]': windowStore.isCalendarOpen }"
        title="Kalender & Waktu Sistem"
      >
        <span class="font-bold tracking-tight text-white">{{ currentTime }}</span>
        <span class="text-[10px] text-slate-300 font-medium">{{ currentDate }}</span>
      </button>

      <!-- Action Center / Notifications -->
      <button 
        @click.stop="toggleActionCenter"
        class="h-full px-2.5 flex items-center justify-center hover:bg-white/10 transition-colors relative cursor-pointer"
        :class="{ 'bg-white/15 text-[#38bdf8]': windowStore.isActionCenterOpen }"
        title="Pusat Tindakan & Notifikasi"
      >
        <MessageSquare class="w-4 h-4 text-slate-200" />
        <span class="absolute top-2 right-1.5 w-2 h-2 rounded-full bg-[#38bdf8]"></span>
      </button>

      <!-- Show Desktop Peek Bar (Far Right Corner) -->
      <button 
        @click.stop="windowStore.minimizeAll"
        class="w-1.5 h-full border-l border-slate-600/70 hover:bg-white/30 transition-colors cursor-pointer"
        title="Tampilkan Desktop"
      ></button>

    </div>

    <!-- ==================== POPUPS / FLYOUTS ==================== -->

    <!-- 1. START MENU WINDOWS 10 -->
    <div 
      v-if="windowStore.isStartMenuOpen"
      @mousedown.stop
      @click.stop
      class="fixed bottom-12 left-0 w-full sm:w-[620px] h-[540px] bg-[#0c192c]/95 dark:bg-[#09111e]/98 backdrop-blur-2xl border border-slate-700/80 rounded-tr-2xl shadow-2xl shadow-black/80 flex overflow-hidden z-[1000] animate-in fade-in slide-in-from-bottom-5 duration-150"
    >
      <!-- Left sidebar buttons (Profile, Theme Toggle, Logout, Power) -->
      <div class="w-12 bg-black/40 border-r border-slate-800 flex flex-col justify-between items-center py-3 shrink-0">
        <div class="flex flex-col items-center space-y-2">
          <button class="p-2 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg cursor-pointer"><Menu class="w-4 h-4" /></button>
          <div 
            class="w-7 h-7 rounded-full bg-gradient-to-br from-[#308e87] to-[#1e5955] text-white flex items-center justify-center font-bold text-xs shadow-md" 
            :title="`Akun: ${authStore.userFullName} (${authStore.userRole})`"
          >
            {{ authStore.userFullName.charAt(0) }}
          </div>
        </div>
        
        <div class="space-y-2 flex flex-col items-center">
          <!-- Theme Switcher button in Start Menu Sidebar -->
          <button 
            @click.stop="handleThemeToggle" 
            class="p-2.5 text-slate-400 hover:text-amber-300 hover:bg-white/10 rounded-lg cursor-pointer transition-colors" 
            :title="isDark ? 'Beralih ke Mode Terang (Light Mode)' : 'Beralih ke Mode Gelap (Dark Mode)'"
          >
            <Sun v-if="isDark" class="w-4 h-4 text-amber-300" />
            <Moon v-else class="w-4 h-4 text-indigo-400" />
          </button>
          
          <button 
            @click.stop="executeLogout" 
            class="p-2.5 text-red-400 hover:text-white hover:bg-red-600 rounded-lg cursor-pointer transition-colors" 
            title="Keluar / Logout"
          >
            <LogOut class="w-4 h-4" />
          </button>
          <button 
            @click.stop="executeLogout" 
            class="p-2.5 text-slate-400 hover:text-red-400 hover:bg-white/10 rounded-lg cursor-pointer transition-colors" 
            title="Daya / Keluar"
          >
            <Power class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Center: 12 Apps List -->
      <div class="w-64 overflow-y-auto p-3 space-y-1 border-r border-slate-800/80">
        <div class="px-2 py-1 text-[10px] font-black uppercase text-slate-400">12 Modul EMONEV Kota Tegal</div>
        <button
          v-for="app in windowStore.appDefinitions"
          :key="app.id"
          @click.stop="launchApp(app.id)"
          class="w-full px-2.5 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-white/10 text-left transition-colors text-xs font-semibold text-slate-200 cursor-pointer"
        >
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br flex items-center justify-center text-white shrink-0" :class="app.iconColor">
            <component :is="getIcon(app.icon)" class="w-3.5 h-3.5" />
          </div>
          <span class="truncate">{{ app.title }}</span>
        </button>
      </div>

      <!-- Right: Live Tiles Windows 10 Grid -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-black/20 flex flex-col justify-between">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-black uppercase text-slate-400">Navigasi Utama</span>
            <div class="flex items-center space-x-2">
              <button 
                @click.stop="handleThemeToggle" 
                class="text-[11px] font-bold text-amber-300 hover:text-amber-200 flex items-center space-x-1 cursor-pointer bg-white/10 px-2 py-0.5 rounded-lg"
              >
                <Sun v-if="isDark" class="w-3 h-3" />
                <Moon v-else class="w-3 h-3 text-indigo-300" />
                <span>{{ isDark ? 'Light' : 'Dark' }}</span>
              </button>
              <button 
                @click.stop="executeLogout" 
                class="text-[11px] font-bold text-red-400 hover:text-red-300 flex items-center space-x-1 cursor-pointer"
              >
                <LogOut class="w-3.5 h-3.5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-2.5">
            <div 
              @click.stop="launchApp('rpjpd')"
              class="bg-gradient-to-br from-[#308e87] to-[#1e5955] p-3 rounded-xl cursor-pointer hover:scale-[1.02] transition-all shadow-md flex flex-col justify-between h-20"
            >
              <Compass class="w-4 h-4 text-white/90" />
              <div>
                <p class="text-xs font-black text-white">RPJPD 2025–2045</p>
                <span class="text-[9px] text-white/70">5 Tab Visi &amp; Sasaran</span>
              </div>
            </div>

            <div 
              @click.stop="launchApp('rpjmd')"
              class="bg-gradient-to-br from-indigo-600 to-indigo-800 p-3 rounded-xl cursor-pointer hover:scale-[1.02] transition-all shadow-md flex flex-col justify-between h-20"
            >
              <Target class="w-4 h-4 text-white/90" />
              <div>
                <p class="text-xs font-black text-white">RPJMD 2025–2029</p>
                <span class="text-[9px] text-white/70">8 Tab Tujuan &amp; IKU</span>
              </div>
            </div>

            <div 
              @click.stop="launchApp('renstra')"
              class="bg-gradient-to-br from-blue-600 to-blue-800 p-3 rounded-xl cursor-pointer hover:scale-[1.02] transition-all shadow-md flex flex-col justify-between h-20"
            >
              <Layers class="w-4 h-4 text-white/90" />
              <div>
                <p class="text-xs font-black text-white">Renstra OPD</p>
                <span class="text-[9px] text-white/70">Rencana Strategis</span>
              </div>
            </div>

            <div 
              @click.stop="launchApp('capaian_kinerja')"
              class="bg-gradient-to-br from-amber-600 to-orange-700 p-3 rounded-xl cursor-pointer hover:scale-[1.02] transition-all shadow-md flex flex-col justify-between h-20"
            >
              <Activity class="w-4 h-4 text-white/90" />
              <div>
                <p class="text-xs font-black text-white">Capaian Kinerja</p>
                <span class="text-[9px] text-white/70">Progres Triwulanan</span>
              </div>
            </div>

            <div 
              @click.stop="launchApp('sdgs')"
              class="bg-gradient-to-br from-emerald-600 to-green-800 p-3 rounded-xl cursor-pointer hover:scale-[1.02] transition-all shadow-md flex flex-col justify-between h-20"
            >
              <Globe class="w-4 h-4 text-white/90" />
              <div>
                <p class="text-xs font-black text-white">SDG's Daerah</p>
                <span class="text-[9px] text-white/70">Tujuan Berkelanjutan</span>
              </div>
            </div>

            <div 
              @click.stop="launchApp('laporan')"
              class="bg-gradient-to-br from-cyan-600 to-blue-700 p-3 rounded-xl cursor-pointer hover:scale-[1.02] transition-all shadow-md flex flex-col justify-between h-20"
            >
              <FileText class="w-4 h-4 text-white/90" />
              <div>
                <p class="text-xs font-black text-white">Laporan Daerah</p>
                <span class="text-[9px] text-white/70">Cetak &amp; Rekapitulasi</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Logged In User Footer Banner in Start Menu -->
        <div class="p-3 rounded-xl bg-white/10 border border-white/15 flex items-center justify-between">
          <div class="flex items-center space-x-2.5 truncate">
            <div class="w-8 h-8 rounded-lg bg-[#308e87] text-white flex items-center justify-center font-bold text-xs shrink-0">
              {{ authStore.userFullName.charAt(0) }}
            </div>
            <div class="truncate">
              <p class="text-xs font-bold text-white truncate">{{ authStore.userFullName }}</p>
              <span class="text-[10px] text-slate-300 font-medium">{{ authStore.userRole }}</span>
            </div>
          </div>
          <button 
            @click.stop="executeLogout"
            class="px-3 py-1.5 rounded-lg text-xs font-black bg-red-600 hover:bg-red-700 text-white flex items-center space-x-1.5 shrink-0 transition-colors shadow-md cursor-pointer"
          >
            <LogOut class="w-3.5 h-3.5" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 2. SEARCH FLYOUT -->
    <div 
      v-if="windowStore.isSearchOpen"
      @mousedown.stop
      @click.stop
      class="fixed bottom-12 left-12 w-full sm:w-[480px] h-[400px] bg-[#0c192c]/95 dark:bg-[#09111e]/98 backdrop-blur-2xl border border-slate-700/80 rounded-2xl shadow-2xl p-4 flex flex-col z-[1000] animate-in fade-in duration-150"
    >
      <div class="flex items-center space-x-2 pb-3 border-b border-slate-700/80">
        <Search class="w-4 h-4 text-[#38bdf8]" />
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Ketik nama modul EMONEV..."
          class="w-full bg-transparent text-xs text-white placeholder-slate-400 focus:outline-none"
          autofocus
        />
      </div>
      <div class="flex-1 overflow-y-auto py-3 space-y-1.5">
        <div class="text-[10px] font-bold uppercase text-slate-400 px-1">12 Modul Tersedia</div>
        <div 
          v-for="app in filteredApps" 
          :key="app.id"
          @click.stop="launchApp(app.id)"
          class="p-2.5 rounded-xl hover:bg-white/10 cursor-pointer flex items-center space-x-3 transition-colors"
        >
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br flex items-center justify-center text-white" :class="app.iconColor">
            <component :is="getIcon(app.icon)" class="w-4 h-4" />
          </div>
          <div>
            <p class="text-xs font-bold text-white">{{ app.title }}</p>
            <span class="text-[10px] text-slate-400">{{ app.category }} • {{ app.badge }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. CALENDAR & CLOCK FLYOUT -->
    <div 
      v-if="windowStore.isCalendarOpen"
      @mousedown.stop
      @click.stop
      class="fixed bottom-12 right-2 w-80 bg-[#0c192c]/95 dark:bg-[#09111e]/98 backdrop-blur-2xl border border-slate-700/80 rounded-2xl shadow-2xl p-4 z-[1000] text-white animate-in fade-in duration-150"
    >
      <div class="pb-3 border-b border-slate-700/80">
        <h3 class="text-2xl font-black">{{ currentTime }}</h3>
        <p class="text-xs text-[#38bdf8] font-bold">{{ fullDateFormatted }}</p>
      </div>
      <div class="py-3 text-center">
        <div class="flex items-center justify-between text-xs font-bold mb-2 text-slate-300">
          <span>Agustus 2026</span>
          <span class="text-[10px] text-slate-400">Kota Tegal</span>
        </div>
        <div class="grid grid-cols-7 gap-1 text-[11px] font-bold text-slate-400 mb-1">
          <span>M</span><span>S</span><span>S</span><span>R</span><span>K</span><span>J</span><span>S</span>
        </div>
        <div class="grid grid-cols-7 gap-1 text-xs">
          <span v-for="d in 31" :key="d" class="py-1 rounded-lg hover:bg-white/10" :class="{ 'bg-[#38bdf8] text-slate-950 font-black shadow-md': d === 17 }">
            {{ d }}
          </span>
        </div>
      </div>
    </div>

    <!-- 4. ACTION CENTER FLYOUT -->
    <div 
      v-if="windowStore.isActionCenterOpen"
      @mousedown.stop
      @click.stop
      class="fixed bottom-12 right-0 w-80 sm:w-96 h-[480px] bg-[#0c192c]/95 dark:bg-[#09111e]/98 backdrop-blur-2xl border-l border-t border-slate-700/80 rounded-tl-2xl shadow-2xl p-4 z-[1000] text-white flex flex-col justify-between animate-in slide-in-from-right duration-150"
    >
      <div>
        <div class="flex items-center justify-between pb-3 border-b border-slate-700/80">
          <h3 class="text-xs font-black uppercase tracking-wider text-slate-300">Pusat Pemberitahuan</h3>
          <button class="text-[10px] text-[#38bdf8] font-bold hover:underline">Hapus Semua</button>
        </div>
        <div class="py-3 space-y-2 text-xs">
          <div class="p-2.5 rounded-xl bg-white/5 border border-white/10 space-y-1">
            <span class="font-bold text-[#38bdf8]">SIMLABA &amp; EMONEV Terhubung</span>
            <p class="text-[11px] text-slate-300">Backend FastAPI aktif di port 8000. Data terintegrasi real-time.</p>
          </div>
          <div class="p-2.5 rounded-xl bg-white/5 border border-white/10 space-y-1">
            <span class="font-bold text-emerald-400">12 Modul EMONEV Aktif</span>
            <p class="text-[11px] text-slate-300">Seluruh modul perencanaan &amp; pelaksanaan siap diakses.</p>
          </div>
        </div>
      </div>

      <!-- Quick Action Buttons -->
      <div class="grid grid-cols-3 gap-2 pt-3 border-t border-slate-700/80">
        <!-- Switch Dark / Light Theme Quick Action -->
        <button 
          @click="handleThemeToggle"
          class="p-2 rounded-xl flex flex-col items-center justify-center text-center transition-colors cursor-pointer"
          :class="isDark ? 'bg-amber-400/20 text-amber-300 hover:bg-amber-400/30' : 'bg-indigo-600/30 text-indigo-200 hover:bg-indigo-600/40'"
        >
          <Sun v-if="isDark" class="w-4 h-4 mb-1 text-amber-300" />
          <Moon v-else class="w-4 h-4 mb-1 text-indigo-300" />
          <span class="text-[9px] font-bold">{{ isDark ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>

        <button 
          @click="windowStore.nightLightActive = !windowStore.nightLightActive"
          class="p-2 rounded-xl flex flex-col items-center justify-center text-center transition-colors cursor-pointer"
          :class="windowStore.nightLightActive ? 'bg-[#38bdf8] text-slate-950 font-bold' : 'bg-white/10 text-slate-300'"
        >
          <Moon class="w-4 h-4 mb-1" />
          <span class="text-[9px]">Night Light</span>
        </button>

        <button @click.stop="executeLogout" class="p-2 rounded-xl bg-red-600/30 hover:bg-red-600 text-red-200 hover:text-white flex flex-col items-center justify-center text-center transition-colors cursor-pointer font-bold">
          <LogOut class="w-4 h-4 mb-1" />
          <span class="text-[9px]">Logout</span>
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Swal from 'sweetalert2'
import { useWindowStore } from '@/stores/windowStore'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import { 
  Search, MessageSquare, Menu, Power, Moon, Sun, LogOut,
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, LayoutDashboard, Settings, Trash2 
} from 'lucide-vue-next'

const windowStore = useWindowStore()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()
const searchQuery = ref('')

const iconMap = {
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, LayoutDashboard, Settings, Trash2 
}
function getIcon(name) {
  return iconMap[name] || Layers
}

function launchApp(appId) {
  windowStore.openApp(appId)
}

function handleThemeToggle() {
  toggleTheme()
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'info',
    title: isDark.value ? 'Beralih ke Mode Gelap (Dark Mode)' : 'Beralih ke Mode Terang (Light Mode)',
    showConfirmButton: false,
    timer: 1500
  })
}

// REALTIME CLOCK & DATE
const currentTime = ref('')
const currentDate = ref('')
const fullDateFormatted = ref('')
let timer = null

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', hour12: false })
  currentDate.value = now.toLocaleDateString('id-ID', { day: '2-digit', month: '2-digit', year: 'numeric' })
  fullDateFormatted.value = now.toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// Toggle popups
function toggleStartMenu() {
  const wasOpen = windowStore.isStartMenuOpen
  windowStore.closeAllPopups()
  windowStore.isStartMenuOpen = !wasOpen
}

function toggleSearch() {
  const wasOpen = windowStore.isSearchOpen
  windowStore.closeAllPopups()
  windowStore.isSearchOpen = !wasOpen
}

function toggleCalendar() {
  const wasOpen = windowStore.isCalendarOpen
  windowStore.closeAllPopups()
  windowStore.isCalendarOpen = !wasOpen
}

function toggleActionCenter() {
  const wasOpen = windowStore.isActionCenterOpen
  windowStore.closeAllPopups()
  windowStore.isActionCenterOpen = !wasOpen
}

function executeLogout() {
  authStore.logout()
  windowStore.closeAllPopups()
  windowStore.openWindows = []
  windowStore.activeWindowId = null
  windowStore.isLocked = false
  window.location.href = '/login'
}

const filteredApps = computed(() => {
  if (!searchQuery.value) return windowStore.appDefinitions
  const q = searchQuery.value.toLowerCase()
  return windowStore.appDefinitions.filter(a => a.title.toLowerCase().includes(q) || a.badge.toLowerCase().includes(q))
})
</script>
