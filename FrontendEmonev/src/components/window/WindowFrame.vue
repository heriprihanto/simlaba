<template>
  <div 
    v-show="!win.isMinimized"
    class="absolute flex flex-col bg-white dark:bg-[#0f172a] shadow-2xl overflow-hidden transition-all duration-75 select-none"
    :class="[
      win.isMaximized 
        ? 'rounded-none border-0' 
        : 'rounded-xl border border-slate-300/80 dark:border-slate-700/80',
      isActive 
        ? 'ring-1 ring-[#308e87]/40 shadow-black/40' 
        : 'opacity-95 shadow-black/20'
    ]"
    :style="{
      left: `${win.x}px`,
      top: `${win.y}px`,
      width: `${win.width}px`,
      height: `${win.height}px`,
      zIndex: win.zIndex
    }"
    @mousedown="handleMouseDown"
  >
    <!-- Windows 10 Titlebar -->
    <div 
      class="h-9 bg-slate-100 dark:bg-[#152238] border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-3 cursor-move shrink-0 select-none"
      @mousedown="startDrag"
      @dblclick="toggleMaximize"
    >
      <!-- Title & Icon -->
      <div class="flex items-center space-x-2 truncate">
        <component :is="iconComponent" class="w-4 h-4 text-[#308e87] dark:text-[#3aada4] shrink-0" />
        <span class="text-xs font-bold text-slate-800 dark:text-slate-200 truncate">{{ win.title }}</span>
        <span v-if="win.badge" class="px-1.5 py-0.2 rounded text-[9px] font-black uppercase bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] shrink-0">
          {{ win.badge }}
        </span>
      </div>

      <!-- Windows 10 Control Buttons (Minimize, Maximize, Close) -->
      <div class="flex items-center space-x-0.5 shrink-0 -mr-2" @mousedown.stop>
        <!-- Minimize -->
        <button 
          @click="minimize"
          class="w-8 h-8 flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-700/70 text-slate-600 dark:text-slate-300 transition-colors"
          title="Minimize"
        >
          <Minus class="w-3.5 h-3.5" />
        </button>

        <!-- Maximize / Restore -->
        <button 
          @click="toggleMaximize"
          class="w-8 h-8 flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-700/70 text-slate-600 dark:text-slate-300 transition-colors"
          :title="win.isMaximized ? 'Restore Down' : 'Maximize'"
        >
          <Square v-if="!win.isMaximized" class="w-3 h-3" />
          <Copy v-else class="w-3 h-3" />
        </button>

        <!-- Close -->
        <button 
          @click="close"
          class="w-9 h-8 flex items-center justify-center hover:bg-red-500 hover:text-white text-slate-600 dark:text-slate-300 transition-colors"
          title="Close"
        >
          <X class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>

    <!-- Window Body Content -->
    <div class="flex-1 overflow-hidden relative">
      <component :is="appComponent" />
    </div>

    <!-- Resizer (Bottom-right corner) -->
    <div 
      v-if="!win.isMaximized"
      class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize flex items-center justify-center"
      @mousedown.stop.prevent="startResize"
    >
      <div class="w-1.5 h-1.5 border-r-2 border-b-2 border-slate-400 dark:border-slate-600"></div>
    </div>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { useWindowStore } from '@/stores/windowStore'
import { 
  Minus, Square, Copy, X, 
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, LayoutDashboard, Settings, Trash2 
} from 'lucide-vue-next'

// App components mapping
import RpjpdApp from '@/components/apps/RpjpdApp.vue'
import RpjmdApp from '@/components/apps/RpjmdApp.vue'
import LaporanApp from '@/components/apps/LaporanApp.vue'
import DashboardApp from '@/components/apps/DashboardApp.vue'
import ModuleApp from '@/components/apps/ModuleApp.vue'

const props = defineProps({
  win: { type: Object, required: true }
})

const windowStore = useWindowStore()

const isActive = computed(() => windowStore.activeWindowId === props.win.id)

const iconMap = {
  Compass, Target, Layers, CalendarDays, FileSignature, 
  Activity, Globe, Coins, GitMerge, ClipboardCheck, 
  BarChart3, FileText, LayoutDashboard, Settings, Trash2
}
const iconComponent = computed(() => iconMap[props.win.icon] || Layers)

const appComponent = computed(() => {
  if (props.win.id === 'dashboard') return DashboardApp
  if (props.win.id === 'rpjpd') return RpjpdApp
  if (props.win.id === 'rpjmd') return RpjmdApp
  if (props.win.id === 'laporan') return LaporanApp
  // Dynamic module handler with appId prop
  return () => h(ModuleApp, { appId: props.win.id })
})

function handleMouseDown() {
  windowStore.bringToFront(props.win.id)
}

function minimize() {
  windowStore.minimizeWindow(props.win.id)
}

function toggleMaximize() {
  windowStore.maximizeWindow(props.win.id)
}

function close() {
  windowStore.closeWindow(props.win.id)
}

// DRAG HANDLING
function startDrag(e) {
  if (props.win.isMaximized) return
  windowStore.bringToFront(props.win.id)

  const startX = e.clientX
  const startY = e.clientY
  const initialX = props.win.x
  const initialY = props.win.y

  function onMouseMove(moveEvent) {
    const deltaX = moveEvent.clientX - startX
    const deltaY = moveEvent.clientY - startY
    windowStore.updatePosition(props.win.id, initialX + deltaX, initialY + deltaY)
  }

  function onMouseUp() {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

// RESIZE HANDLING
function startResize(e) {
  windowStore.bringToFront(props.win.id)
  const startX = e.clientX
  const startY = e.clientY
  const initialWidth = props.win.width
  const initialHeight = props.win.height

  function onMouseMove(moveEvent) {
    const deltaX = moveEvent.clientX - startX
    const deltaY = moveEvent.clientY - startY
    windowStore.updateSize(props.win.id, initialWidth + deltaX, initialHeight + deltaY)
  }

  function onMouseUp() {
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}
</script>
