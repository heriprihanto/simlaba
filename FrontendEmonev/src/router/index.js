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
import RpjpdView from '@/views/RpjpdView.vue'
import RpjmdView from '@/views/RpjmdView.vue'

import DesktopView from '@/views/DesktopView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true, title: 'Login — EMONEV OS' }
  },
  {
    path: '/',
    name: 'desktop',
    component: DesktopView,
    meta: { requiresAuth: true, title: 'EMONEV OS Desktop' }
  },
  // PERENCANAAN
  {
    path: '/perencanaan/rpjpd',
    name: 'perencanaan-rpjpd',
    component: RpjpdView,
    meta: { 
      requiresAuth: true, 
      category: 'Perencanaan', 
      title: 'RPJPD', 
      description: 'Rencana Pembangunan Jangka Panjang Daerah Kota Tegal.' 
    }
  },
  {
    path: '/perencanaan/rpjmd',
    name: 'perencanaan-rpjmd',
    component: RpjmdView,
    meta: { 
      requiresAuth: true, 
      category: 'Perencanaan', 
      title: 'RPJMD', 
      description: 'Rencana Pembangunan Jangka Menengah Daerah Kota Tegal.' 
    }
  },
  {
    path: '/perencanaan/renstra',
    name: 'perencanaan-renstra',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Perencanaan', 
      title: 'Renstra', 
      description: 'Rencana Strategis Perangkat Daerah Kota Tegal.' 
    }
  },
  {
    path: '/perencanaan/renja',
    name: 'perencanaan-renja',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Perencanaan', 
      title: 'Renja', 
      description: 'Rencana Kerja Perangkat Daerah Kota Tegal.' 
    }
  },
  {
    path: '/perencanaan/perjanjian-kinerja',
    name: 'perencanaan-perjanjian-kinerja',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Perencanaan', 
      title: 'Perjanjian Kinerja', 
      description: 'Penetapan dan Lembar Perjanjian Kinerja Perangkat Daerah.' 
    }
  },
  // PELAKSANAAN
  {
    path: '/pelaksanaan/capaian-kinerja-triwulanan',
    name: 'pelaksanaan-capaian-triwulanan',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Pelaksanaan', 
      title: 'Capaian Kinerja Triwulanan', 
      description: 'Pemantauan dan Pengukuran Capaian Kinerja Triwulanan OPD.' 
    }
  },
  {
    path: '/pelaksanaan/sdgs',
    name: 'pelaksanaan-sdgs',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Pelaksanaan', 
      title: "SDG's", 
      description: 'Pencapaian Indikator Sasaran Pembangunan Berkelanjutan (Sustainable Development Goals).' 
    }
  },
  {
    path: '/pelaksanaan/dana-alokasi-khusus',
    name: 'pelaksanaan-dak',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Pelaksanaan', 
      title: 'Dana Alokasi Khusus (DAK)', 
      description: 'Pemantauan dan Pelaksanaan Realisasi Dana Alokasi Khusus.' 
    }
  },
  {
    path: '/pelaksanaan/sinkronisasi-serapan-anggaran',
    name: 'pelaksanaan-sinkronisasi-serapan',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Pelaksanaan', 
      title: 'Sinkronisasi Serapan Anggaran', 
      description: 'Sinkronisasi dan Rekonsiliasi Realisasi Anggaran Keuangan Perangkat Daerah.' 
    }
  },
  {
    path: '/pelaksanaan/pelaporan-kinerja',
    name: 'pelaksanaan-pelaporan-kinerja',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Pelaksanaan', 
      title: 'Pelaporan Kinerja', 
      description: 'Pelaporan Progres Capaian Kinerja Program dan Subkegiatan OPD.' 
    }
  },
  {
    path: '/pelaksanaan/evaluasi-kinerja',
    name: 'pelaksanaan-evaluasi-kinerja',
    component: PlaceholderView,
    meta: { 
      requiresAuth: true, 
      category: 'Pelaksanaan', 
      title: 'Evaluasi Kinerja', 
      description: 'Evaluasi Hasil dan Dampak Capaian Kinerja Pembangunan Daerah.' 
    }
  },
  // LAPORAN (TAMPILAN TETAP)
  {
    path: '/laporan',
    name: 'laporan',
    component: LaporanView,
    meta: { requiresAuth: true, title: 'Laporan' }
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
