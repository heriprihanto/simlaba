<template>
  <div class="w-screen h-screen overflow-hidden">
    <Desktop />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Desktop from '@/components/desktop/Desktop.vue'
import { useWindowStore } from '@/stores/windowStore'
import { useAuthStore } from '@/stores/auth'

const windowStore = useWindowStore()
const authStore = useAuthStore()

onMounted(() => {
  // Hanya buka dashboard otomatis jika pengguna sudah terotentikasi
  if (authStore.isAuthenticated) {
    setTimeout(() => {
      const screenW = window.innerWidth
      const screenH = window.innerHeight
      
      // Ikon desktop di sebelah kiri membutuhkan ruang sekitar 240px
      const leftMarginForIcons = 260
      const desiredWidth = 920
      const winWidth = Math.min(desiredWidth, Math.max(500, screenW - leftMarginForIcons - 30))
      const winHeight = Math.min(640, Math.max(400, screenH - 90))
      
      // Posisikan di sebelah kanan layar
      const winX = Math.max(leftMarginForIcons, screenW - winWidth - 30)
      const winY = 24

      windowStore.openApp('dashboard', {
        x: winX,
        y: winY,
        width: winWidth,
        height: winHeight
      })
    }, 250)
  }
})
</script>
