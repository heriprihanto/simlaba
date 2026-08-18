<template>
  <div class="w-screen h-screen overflow-hidden bg-[#071322] text-slate-100 font-sans select-none">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'

const authStore = useAuthStore()
const { initTheme } = useTheme()

onMounted(() => {
  initTheme()
  authStore.initializeAuth()
})
</script>
