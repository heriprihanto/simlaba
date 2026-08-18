import { ref, watchEffect } from 'vue'

// Get initial value from localStorage, default to false (Light Mode)
const getInitialTheme = () => {
  if (typeof window === 'undefined') return false
  const saved = localStorage.getItem('theme')
  return saved === 'dark'
}

const isDark = ref(getInitialTheme())

const applyTheme = () => {
  if (typeof document === 'undefined') return
  const html = document.documentElement
  const body = document.body

  if (isDark.value) {
    html.classList.add('dark')
    body.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    body.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

// Run applyTheme immediately
applyTheme()

export function useTheme() {
  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
    console.log('[SIMLABA Theme] Toggled isDark to:', isDark.value, 'HTML classes:', document.documentElement.className)
  }

  const setLight = () => {
    isDark.value = false
    applyTheme()
  }

  const setDark = () => {
    isDark.value = true
    applyTheme()
  }

  return {
    isDark,
    toggleTheme,
    setLight,
    setDark,
    initTheme: applyTheme
  }
}
