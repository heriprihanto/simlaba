import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useWindowStore = defineStore('windowStore', () => {
  // App definitions registry (Exact 12 EMONEV Icons)
  const appDefinitions = [
    {
      id: 'rpjpd',
      title: 'RPJPD',
      category: 'Perencanaan',
      desc: 'Rencana Pembangunan Jangka Panjang Daerah Kota Tegal 2025–2045',
      icon: 'Compass',
      iconColor: 'from-[#308e87] to-[#1e5955]',
      badge: '20 Tahun',
      defaultWidth: 1080,
      defaultHeight: 700,
      minWidth: 700,
      minHeight: 500
    },
    {
      id: 'rpjmd',
      title: 'RPJMD',
      category: 'Perencanaan',
      desc: 'Rencana Pembangunan Jangka Menengah Daerah Kota Tegal 2025–2029',
      icon: 'Target',
      iconColor: 'from-indigo-600 to-indigo-900',
      badge: '5 Tahun',
      defaultWidth: 1100,
      defaultHeight: 710,
      minWidth: 720,
      minHeight: 500
    },
    {
      id: 'renstra',
      title: 'Renstra',
      category: 'Perencanaan',
      desc: 'Rencana Strategis Perangkat Daerah Kota Tegal 5 Tahunan',
      icon: 'Layers',
      iconColor: 'from-blue-600 to-blue-800',
      badge: 'Renstra OPD',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'renja',
      title: 'Renja',
      category: 'Perencanaan',
      desc: 'Rencana Kerja Tahunan Perangkat Daerah Kota Tegal',
      icon: 'CalendarDays',
      iconColor: 'from-cyan-600 to-cyan-800',
      badge: 'Tahunan',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'perjanjian_kinerja',
      title: 'Perjanjian Kinerja',
      category: 'Perencanaan',
      desc: 'Penetapan dan Lembar Perjanjian Kinerja Kepala Perangkat Daerah',
      icon: 'FileSignature',
      iconColor: 'from-teal-600 to-teal-800',
      badge: 'Penetapan',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'capaian_kinerja',
      title: 'Capaian Kinerja',
      category: 'Pelaksanaan',
      desc: 'Pemantauan dan Pengukuran Capaian Kinerja Triwulanan OPD',
      icon: 'Activity',
      iconColor: 'from-amber-500 to-orange-600',
      badge: 'Triwulan',
      defaultWidth: 1020,
      defaultHeight: 660,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'sdgs',
      title: "SDG's",
      category: 'Pelaksanaan',
      desc: 'Indikator Sasaran Pembangunan Berkelanjutan (Sustainable Development Goals)',
      icon: 'Globe',
      iconColor: 'from-emerald-600 to-green-800',
      badge: 'SDGs Tegal',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'dak',
      title: 'Dana Alokasi Khusus',
      category: 'Pelaksanaan',
      desc: 'Pemantauan dan Pelaksanaan Realisasi Dana Alokasi Khusus (DAK)',
      icon: 'Coins',
      iconColor: 'from-purple-600 to-indigo-800',
      badge: 'DAK Fisik/Non',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'sinkronisasi_serapan',
      title: 'Sinkronisasi Serapan Anggaran',
      category: 'Pelaksanaan',
      desc: 'Sinkronisasi dan Rekonsiliasi Realisasi Anggaran Keuangan Perangkat Daerah',
      icon: 'GitMerge',
      iconColor: 'from-rose-600 to-pink-800',
      badge: 'Rekonsiliasi',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'pelaporan_kinerja',
      title: 'Pelaporan Kinerja',
      category: 'Pelaksanaan',
      desc: 'Pelaporan Progres Capaian Kinerja Program dan Subkegiatan OPD',
      icon: 'ClipboardCheck',
      iconColor: 'from-sky-600 to-blue-800',
      badge: 'Subkegiatan',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'evaluasi_kinerja',
      title: 'Evaluasi Kinerja',
      category: 'Pelaksanaan',
      desc: 'Evaluasi Hasil dan Dampak Capaian Kinerja Pembangunan Daerah',
      icon: 'BarChart3',
      iconColor: 'from-violet-600 to-purple-900',
      badge: 'Evaluasi',
      defaultWidth: 980,
      defaultHeight: 640,
      minWidth: 640,
      minHeight: 450
    },
    {
      id: 'laporan',
      title: 'Laporan (Tampilan Tetap)',
      category: 'Laporan',
      desc: 'Laporan Perkembangan Pembangunan, Realisasi Fisik & Keuangan',
      icon: 'FileText',
      iconColor: 'from-blue-500 to-cyan-700',
      badge: 'Dokumen',
      defaultWidth: 980,
      defaultHeight: 660,
      minWidth: 600,
      minHeight: 450
    }
  ]

  // State of all open windows
  const openWindows = ref([])
  const activeWindowId = ref(null)
  let zIndexCounter = ref(100)

  // Taskbar popup states
  const isStartMenuOpen = ref(false)
  const isActionCenterOpen = ref(false)
  const isCalendarOpen = ref(false)
  const isVolumeOpen = ref(false)
  const isNetworkOpen = ref(false)
  const isBatteryOpen = ref(false)
  const isSearchOpen = ref(false)

  // Lock Screen state
  const isLocked = ref(false)

  // Desktop context menu state
  const contextMenu = ref({
    show: false,
    x: 0,
    y: 0
  })

  // System settings state
  const volumeLevel = ref(85)
  const isMuted = ref(false)
  const batteryLevel = ref(92)
  const isCharging = ref(true)
  const wifiConnected = ref(true)
  const wifiSsid = ref('PEMKOT-TEGAL-SECURE-WIFI')
  const nightLightActive = ref(false)

  // Close all taskbar popups
  function closeAllPopups() {
    isStartMenuOpen.value = false
    isActionCenterOpen.value = false
    isCalendarOpen.value = false
    isVolumeOpen.value = false
    isNetworkOpen.value = false
    isBatteryOpen.value = false
    isSearchOpen.value = false
    contextMenu.value.show = false
  }

  // Open / Launch app
  function openApp(appId, customProps = {}) {
    closeAllPopups()
    let def = appDefinitions.find(a => a.id === appId)
    if (!def) {
      if (appId === 'dashboard') {
        def = {
          id: 'dashboard',
          title: 'Dashboard & Evaluasi Kinerja',
          category: 'Eksekutif',
          desc: 'Ringkasan Realisasi Anggaran, Fisik, dan Capaian Kinerja Daerah',
          icon: 'LayoutDashboard',
          iconColor: 'from-teal-500 to-emerald-700',
          badge: 'Eksekutif',
          defaultWidth: 920,
          defaultHeight: 640,
          minWidth: 550,
          minHeight: 400
        }
      } else {
        return
      }
    }

    const existing = openWindows.value.find(w => w.id === appId)
    if (existing) {
      if (existing.isMinimized) {
        existing.isMinimized = false
      }
      bringToFront(appId)
      return
    }

    // Default positioning or custom positioning
    const offset = (openWindows.value.length % 6) * 28
    const posX = customProps.x !== undefined ? customProps.x : Math.max(40, 60 + offset)
    const posY = customProps.y !== undefined ? customProps.y : Math.max(30, 40 + offset)
    const winWidth = customProps.width !== undefined ? customProps.width : Math.min(window.innerWidth - 80, def.defaultWidth)
    const winHeight = customProps.height !== undefined ? customProps.height : Math.min(window.innerHeight - 100, def.defaultHeight)

    zIndexCounter.value += 1
    const newWindow = {
      id: def.id,
      title: def.title,
      icon: def.icon,
      iconColor: def.iconColor,
      badge: def.badge,
      x: posX,
      y: posY,
      width: winWidth,
      height: winHeight,
      minWidth: def.minWidth,
      minHeight: def.minHeight,
      isMinimized: false,
      isMaximized: false,
      prevBounds: null,
      zIndex: zIndexCounter.value
    }

    openWindows.value.push(newWindow)
    activeWindowId.value = appId
  }

  // Close window
  function closeWindow(appId) {
    const idx = openWindows.value.findIndex(w => w.id === appId)
    if (idx !== -1) {
      openWindows.value.splice(idx, 1)
      if (activeWindowId.value === appId) {
        // focus topmost remaining window
        const visible = openWindows.value.filter(w => !w.isMinimized)
        if (visible.length > 0) {
          visible.sort((a, b) => b.zIndex - a.zIndex)
          activeWindowId.value = visible[0].id
        } else {
          activeWindowId.value = null
        }
      }
    }
  }

  // Minimize window
  function minimizeWindow(appId) {
    const win = openWindows.value.find(w => w.id === appId)
    if (win) {
      win.isMinimized = true
      if (activeWindowId.value === appId) {
        const visible = openWindows.value.filter(w => !w.isMinimized)
        if (visible.length > 0) {
          visible.sort((a, b) => b.zIndex - a.zIndex)
          activeWindowId.value = visible[0].id
        } else {
          activeWindowId.value = null
        }
      }
    }
  }

  // Toggle maximize / restore
  function maximizeWindow(appId) {
    const win = openWindows.value.find(w => w.id === appId)
    if (!win) return
    bringToFront(appId)

    if (win.isMaximized) {
      // restore
      win.isMaximized = false
      if (win.prevBounds) {
        win.x = win.prevBounds.x
        win.y = win.prevBounds.y
        win.width = win.prevBounds.width
        win.height = win.prevBounds.height
      }
    } else {
      // maximize
      win.prevBounds = { x: win.x, y: win.y, width: win.width, height: win.height }
      win.isMaximized = true
      win.x = 0
      win.y = 0
      win.width = window.innerWidth
      win.height = window.innerHeight - 48 // minus taskbar height
    }
  }

  // Focus / Bring to front
  function bringToFront(appId) {
    const win = openWindows.value.find(w => w.id === appId)
    if (win) {
      if (win.isMinimized) {
        win.isMinimized = false
      }
      zIndexCounter.value += 1
      win.zIndex = zIndexCounter.value
      activeWindowId.value = appId
    }
  }

  // Toggle minimize/restore from Taskbar
  function toggleTaskbarItem(appId) {
    const win = openWindows.value.find(w => w.id === appId)
    if (!win) {
      openApp(appId)
      return
    }

    if (win.isMinimized) {
      win.isMinimized = false
      bringToFront(appId)
    } else if (activeWindowId.value === appId) {
      minimizeWindow(appId)
    } else {
      bringToFront(appId)
    }
  }

  // Update window position during drag
  function updatePosition(appId, x, y) {
    const win = openWindows.value.find(w => w.id === appId)
    if (win && !win.isMaximized) {
      win.x = Math.max(-win.width + 100, Math.min(window.innerWidth - 60, x))
      win.y = Math.max(0, Math.min(window.innerHeight - 80, y))
    }
  }

  // Update window size during resize
  function updateSize(appId, width, height) {
    const win = openWindows.value.find(w => w.id === appId)
    if (win && !win.isMaximized) {
      win.width = Math.max(win.minWidth, width)
      win.height = Math.max(win.minHeight, height)
    }
  }

  // Show desktop / Minimize all
  function minimizeAll() {
    closeAllPopups()
    const anyOpen = openWindows.value.some(w => !w.isMinimized)
    if (anyOpen) {
      openWindows.value.forEach(w => { w.isMinimized = true })
      activeWindowId.value = null
    } else {
      openWindows.value.forEach(w => { w.isMinimized = false })
      if (openWindows.value.length > 0) {
        activeWindowId.value = openWindows.value[0].id
      }
    }
  }

  // Open context menu
  function openContextMenu(e) {
    closeAllPopups()
    contextMenu.value = {
      show: true,
      x: Math.min(window.innerWidth - 220, e.clientX),
      y: Math.min(window.innerHeight - 240, e.clientY)
    }
  }

  function lockSession() {
    closeAllPopups()
    isLocked.value = true
  }

  function unlockSession() {
    isLocked.value = false
  }

  return {
    appDefinitions,
    openWindows,
    activeWindowId,
    isStartMenuOpen,
    isActionCenterOpen,
    isCalendarOpen,
    isVolumeOpen,
    isNetworkOpen,
    isBatteryOpen,
    isSearchOpen,
    isLocked,
    contextMenu,
    volumeLevel,
    isMuted,
    batteryLevel,
    isCharging,
    wifiConnected,
    wifiSsid,
    nightLightActive,
    closeAllPopups,
    openApp,
    closeWindow,
    minimizeWindow,
    maximizeWindow,
    bringToFront,
    toggleTaskbarItem,
    updatePosition,
    updateSize,
    minimizeAll,
    openContextMenu,
    lockSession,
    unlockSession
  }
})
