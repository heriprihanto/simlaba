import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import PersonelView from '@/views/PersonelView.vue'
import PengaturanView from '@/views/PengaturanView.vue'
import LaporanView from '@/views/LaporanView.vue'
import RkoView from '@/views/RkoView.vue'
import RfkView from '@/views/RfkView.vue'
import PetaView from '@/views/PetaView.vue'
import PlaceholderView from '@/views/PlaceholderView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/personel',
    name: 'personel',
    component: PersonelView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rko',
    name: 'rko',
    component: RkoView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rfk',
    name: 'rfk',
    component: RfkView,
    meta: { requiresAuth: true }
  },
  {
    path: '/laporan',
    name: 'laporan',
    component: LaporanView,
    meta: { requiresAuth: true }
  },
  {
    path: '/pengaturan',
    name: 'pengaturan',
    component: PengaturanView,
    meta: { requiresAuth: true }
  },
  {
    path: '/peta',
    name: 'peta',
    component: PetaView,
    meta: { requiresAuth: true }
  },
  {
    path: '/report/:id',
    name: 'report-detail',
    component: () => import('@/views/ReportDetailView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
