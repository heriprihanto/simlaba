<template>
  <div class="min-h-screen flex flex-col bg-[#F8F8F4] dark:bg-[#090d16] text-slate-900 dark:text-slate-100 transition-colors duration-300">
    <!-- Top Horizontal Navigation Bar -->
    <TopNavbar v-if="showNavbar" />

    <!-- Main Content Area -->
    <main class="flex-1" :class="{ 'max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6': showNavbar }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
import TopNavbar from '@/components/TopNavbar.vue'

const route = useRoute()
const authStore = useAuthStore()
const { initTheme } = useTheme()

const showNavbar = computed(() => {
  return route.name !== 'login' && authStore.isAuthenticated
})

onMounted(() => {
  initTheme()
  authStore.initializeAuth()
})
</script>
