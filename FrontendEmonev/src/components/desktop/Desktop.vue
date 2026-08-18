<template>
  <div 
    class="relative w-screen h-screen overflow-hidden select-none transition-colors duration-300"
    :class="[
      windowStore.nightLightActive ? 'sepia-[0.25]' : '',
      isDark ? 'theme-dark' : 'theme-light'
    ]"
    @contextmenu.prevent="windowStore.openContextMenu($event)"
  >
    <!-- Windows 10 Dynamic Wallpaper Background (Clicking background closes popups) -->
    <div 
      @mousedown="handleDesktopMouseDown"
      class="absolute inset-0 z-0 cursor-default transition-all duration-500"
      :class="isDark 
        ? 'bg-gradient-to-br from-[#071322] via-[#0b1f3a] to-[#04101e]' 
        : 'bg-gradient-to-br from-[#e0ecf8] via-[#c9def2] to-[#b8d4ee]'"
    >
      <!-- Windows 10 Bloom / Light Beams Ambient Art -->
      <div 
        class="absolute top-1/4 left-1/3 w-96 h-96 rounded-full blur-3xl pointer-events-none transition-opacity duration-500"
        :class="isDark ? 'bg-[#0078d7]/20 opacity-100' : 'bg-[#0078d7]/30 opacity-70'"
      ></div>
      <div 
        class="absolute bottom-1/3 right-1/4 w-[500px] h-[500px] rounded-full blur-3xl pointer-events-none transition-opacity duration-500"
        :class="isDark ? 'bg-[#308e87]/20 opacity-100' : 'bg-[#308e87]/25 opacity-70'"
      ></div>
      <div 
        class="absolute inset-0 opacity-[0.04] pointer-events-none"
        :style="{ backgroundImage: 'radial-gradient(' + (isDark ? '#ffffff' : '#0f172a') + ' 1px, transparent 1px)', backgroundSize: '24px 24px' }"
      ></div>
      
      <!-- Subtle Windows 10 Logo in Center Background -->
      <div class="absolute inset-0 flex items-center justify-center pointer-events-none" :class="isDark ? 'opacity-5' : 'opacity-10'">
        <div class="grid grid-cols-2 gap-4 w-72 h-72">
          <div :class="isDark ? 'bg-white' : 'bg-slate-900'" class="rounded-lg"></div>
          <div :class="isDark ? 'bg-white' : 'bg-slate-900'" class="rounded-lg"></div>
          <div :class="isDark ? 'bg-white' : 'bg-slate-900'" class="rounded-lg"></div>
          <div :class="isDark ? 'bg-white' : 'bg-slate-900'" class="rounded-lg"></div>
        </div>
      </div>
    </div>

    <!-- Desktop Icons Grid (Top Left to Bottom) -->
    <div class="relative z-10 p-4 grid grid-flow-col grid-rows-6 gap-2.5 w-max max-h-[calc(100vh-48px)] pointer-events-auto">
      <div
        v-for="app in windowStore.appDefinitions"
        :key="app.id"
        @click.stop="handleIconClick(app.id)"
        @dblclick.stop="windowStore.openApp(app.id)"
        class="w-24 h-24 rounded-xl flex flex-col items-center justify-center p-2 text-center cursor-pointer transition-all border group select-none relative"
        :class="[
          selectedIconId === app.id 
            ? (isDark ? 'bg-white/20 border-white/40 ring-1 ring-white/40' : 'bg-slate-900/15 border-slate-900/30 ring-1 ring-slate-900/30 shadow-md')
            : (isDark ? 'border-transparent hover:bg-white/15 hover:border-white/20' : 'border-transparent hover:bg-white/40 hover:border-white/60')
        ]"
      >
        <!-- Icon Container -->
        <div 
          class="w-12 h-12 rounded-2xl bg-gradient-to-br flex items-center justify-center text-white shadow-xl shadow-black/30 mb-1.5 transition-transform group-hover:scale-110"
          :class="app.iconColor"
        >
          <component :is="getIcon(app.icon)" class="w-6 h-6" />
        </div>

        <!-- Label -->
        <span 
          class="text-[11px] font-bold line-clamp-2 leading-tight"
          :class="isDark 
            ? 'text-white drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]' 
            : 'text-slate-800 drop-shadow-[0_1px_2px_rgba(255,255,255,0.9)]'"
        >
          {{ app.title.split('—')[0] }}
        </span>
      </div>
    </div>

    <!-- Active Windows Layer (Only individual windows have pointer-events-auto) -->
    <div class="absolute inset-0 z-20 pointer-events-none overflow-hidden">
      <WindowFrame 
        v-for="win in windowStore.openWindows" 
        :key="win.id" 
        :win="win" 
        class="pointer-events-auto"
      />
    </div>

    <!-- Desktop Context Menu (Right Click) -->
    <div 
      v-if="windowStore.contextMenu.show"
      @click.stop
      class="fixed z-[2000] w-56 bg-[#0c192c]/95 dark:bg-[#09111e]/98 backdrop-blur-2xl border border-slate-700/80 rounded-2xl shadow-2xl p-1.5 text-xs text-slate-200 animate-in fade-in zoom-in-95 duration-100"
      :style="{ left: `${windowStore.contextMenu.x}px`, top: `${windowStore.contextMenu.y}px` }"
    >
      <button 
        @click="handleMenuAction('refresh')"
        class="w-full px-3 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-white/10 text-left transition-colors font-medium"
      >
        <RotateCw class="w-4 h-4 text-slate-400" />
        <span>Segarkan (Refresh)</span>
      </button>

      <button 
        @click="handleMenuAction('sort')"
        class="w-full px-3 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-white/10 text-left transition-colors font-medium"
      >
        <ArrowDownUp class="w-4 h-4 text-slate-400" />
        <span>Urutkan Ikon</span>
      </button>

      <div class="h-px bg-slate-700/60 my-1"></div>

      <!-- Switch Dark / Light Mode -->
      <button 
        @click="handleThemeToggle"
        class="w-full px-3 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-white/10 text-left transition-colors font-medium text-amber-300"
      >
        <Sun v-if="isDark" class="w-4 h-4 text-amber-300" />
        <Moon v-else class="w-4 h-4 text-indigo-400" />
        <span>{{ isDark ? 'Mode Terang (Light Mode)' : 'Mode Gelap (Dark Mode)' }}</span>
      </button>

      <button 
        @click="windowStore.openApp('dashboard')"
        class="w-full px-3 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-white/10 text-left transition-colors font-medium"
      >
        <LayoutDashboard class="w-4 h-4 text-teal-400" />
        <span>Buka Dashboard</span>
      </button>

      <button 
        @click="confirmLogout"
        class="w-full px-3 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-red-500/20 text-left transition-colors font-medium text-red-400"
      >
        <LogOut class="w-4 h-4" />
        <span>Keluar (Logout)</span>
      </button>

      <div class="h-px bg-slate-700/60 my-1"></div>

      <button 
        @click="windowStore.minimizeAll"
        class="w-full px-3 py-2 rounded-xl flex items-center space-x-2.5 hover:bg-white/10 text-left transition-colors font-medium"
      >
        <Monitor class="w-4 h-4 text-emerald-400" />
        <span>Tampilkan Desktop</span>
      </button>
    </div>

    <!-- Taskbar Component -->
    <Taskbar />

  </div>
</template>

<script setup>
import { ref } from 'vue'
import Swal from 'sweetalert2'
import { useWindowStore } from '@/stores/windowStore'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import WindowFrame from '@/components/window/WindowFrame.vue'
import Taskbar from '@/components/taskbar/Taskbar.vue'
import { 
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, RotateCw, ArrowDownUp, 
  FolderPlus, Sliders, Monitor, Lock, LogOut, LayoutDashboard, Sun, Moon 
} from 'lucide-vue-next'

const windowStore = useWindowStore()
const authStore = useAuthStore()
const { isDark, toggleTheme } = useTheme()
const selectedIconId = ref(null)

const iconMap = {
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, LayoutDashboard
}
function getIcon(name) {
  return iconMap[name] || Layers
}

function handleIconClick(appId) {
  selectedIconId.value = appId
  windowStore.openApp(appId)
}

function handleDesktopMouseDown() {
  selectedIconId.value = null
  windowStore.closeAllPopups()
}

function handleThemeToggle() {
  toggleTheme()
  windowStore.closeAllPopups()
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'info',
    title: isDark.value ? 'Beralih ke Mode Gelap (Dark Mode)' : 'Beralih ke Mode Terang (Light Mode)',
    showConfirmButton: false,
    timer: 1500
  })
}

function confirmLogout() {
  windowStore.closeAllPopups()
  authStore.logout()
  windowStore.openWindows = []
  windowStore.activeWindowId = null
  windowStore.isLocked = false
  window.location.href = '/login'
}

function handleMenuAction(action) {
  windowStore.closeAllPopups()
  if (action === 'refresh') {
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Desktop disegarkan',
      showConfirmButton: false,
      timer: 1500
    })
  } else if (action === 'sort') {
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'info',
      title: 'Ikon diurutkan',
      showConfirmButton: false,
      timer: 1500
    })
  }
}
</script>
