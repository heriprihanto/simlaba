<template>
  <div class="space-y-6 pb-12">
    
    <!-- Page Header & Summary Bar -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2">
          <span class="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-wider bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4]">
            Sistem Informasi Geografis / GIS
          </span>
          <span class="text-xs text-slate-400 font-bold">• SIMLABA 2026</span>
        </div>
        <h1 class="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">Peta Lokasi Pekerjaan</h1>
        <p class="text-xs text-slate-500 dark:text-slate-400">Pemetaan Spasial Multi-Lokasi Paket Pekerjaan Pembangunan Kota Tegal T.A. 2026</p>
      </div>

      <!-- Quick Summary Badges -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
        <div class="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs">
          <span class="text-[10px] font-bold text-slate-400 block uppercase">Total Lokasi GIS</span>
          <span class="text-base font-black text-[#308e87] dark:text-[#3aada4]">{{ summary.total_lokasi_gis || 0 }} Lokasi</span>
        </div>
        <div class="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs">
          <span class="text-[10px] font-bold text-slate-400 block uppercase">Pekerjaan Terdaftar</span>
          <span class="text-base font-black text-slate-800 dark:text-slate-200">{{ summary.total_pekerjaan || 0 }} Paket</span>
        </div>
        <div class="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs">
          <span class="text-[10px] font-bold text-slate-400 block uppercase">Total Pagu</span>
          <span class="text-base font-black text-emerald-600 dark:text-emerald-400">Rp {{ formatNumber(summary.total_anggaran) }}</span>
        </div>
        <div class="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs">
          <span class="text-[10px] font-bold text-slate-400 block uppercase">Avg Fisik</span>
          <span class="text-base font-black text-purple-600 dark:text-purple-400">{{ summary.avg_realisasi_fisik ? summary.avg_realisasi_fisik.toFixed(1) : '0' }}%</span>
        </div>
      </div>
    </div>

    <!-- Filter Toolbar -->
    <div class="p-4 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
        <!-- Search Input -->
        <div class="relative flex-1">
          <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input 
            v-model="searchQuery" 
            @input="debounceFetch"
            type="text" 
            placeholder="Cari nama pekerjaan, lokasi, atau deskripsi..." 
            class="w-full pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]"
          />
        </div>

        <!-- OPD Filter -->
        <div class="w-full md:w-64">
          <select 
            v-model="selectedOpd" 
            @change="fetchData"
            class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87] cursor-pointer"
          >
            <option :value="null">-- Semua Perangkat Daerah (OPD) --</option>
            <option v-for="opd in opdOptions" :key="opd.id_sub_pd" :value="opd.id_sub_pd">
              {{ opd.nama_pd_singkat || opd.nama_pd }}
            </option>
          </select>
        </div>

        <!-- Jenis Pengadaan Filter -->
        <div class="w-full md:w-56">
          <select 
            v-model="selectedPengadaan" 
            @change="fetchData"
            class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87] cursor-pointer"
          >
            <option :value="null">-- Semua Jenis Pengadaan --</option>
            <option :value="1">Pengadaan Barang</option>
            <option :value="2">Jasa Konsultasi</option>
            <option :value="3">Jasa Lainnya</option>
            <option :value="4">Konstruksi</option>
          </select>
        </div>

        <!-- Refresh Button -->
        <button 
          @click="fetchData" 
          class="px-4 py-2 bg-[#308e87] hover:bg-[#277872] text-white rounded-xl font-bold text-xs flex items-center justify-center space-x-1.5 transition-colors cursor-pointer shrink-0 shadow-xs"
        >
          <RefreshCw class="w-3.5 h-3.5" :class="loading ? 'animate-spin' : ''" />
          <span>Muat Ulang</span>
        </button>
      </div>
    </div>

    <!-- Map & Side List Container -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      
      <!-- Leaflet Full Interactive Map -->
      <div class="lg:col-span-3 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm p-4 relative flex flex-col min-h-[600px]">
        <div id="peta-simlaba-full" class="w-full h-full min-h-[580px] rounded-2xl overflow-hidden shadow-inner z-0"></div>

        <!-- Floating Map Legend -->
        <div class="absolute bottom-8 right-8 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md p-3.5 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 text-[11px] z-[1000] space-y-2 max-w-xs">
          <h4 class="font-black text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800 pb-1 flex items-center space-x-1">
            <Layers class="w-3.5 h-3.5 text-[#308e87]" />
            <span>Keterangan Bentuk Geometri (PostGIS)</span>
          </h4>
          <div class="grid grid-cols-2 gap-1.5 text-[10px] font-bold">
            <div class="flex items-center space-x-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-[#308e87]"></span>
              <span>Titik 📍 (Point)</span>
            </div>
            <div class="flex items-center space-x-1.5">
              <span class="w-2.5 h-0.5 bg-blue-600"></span>
              <span>Garis 📈 (Line)</span>
            </div>
            <div class="flex items-center space-x-1.5">
              <span class="w-2.5 h-2.5 rounded-xs bg-emerald-500/50 border border-emerald-600"></span>
              <span>Polygon ⬡</span>
            </div>
            <div class="flex items-center space-x-1.5">
              <span class="w-2.5 h-2.5 rounded-xs bg-purple-500/50 border border-purple-600"></span>
              <span>Kotak 🔲</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Side Location List Panel -->
      <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm p-4 flex flex-col max-h-[630px]">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
          <h3 class="font-black text-slate-900 dark:text-white text-xs uppercase tracking-wider flex items-center space-x-1.5">
            <MapPin class="w-4 h-4 text-[#308e87]" />
            <span>Daftar Lokasi ({{ locations.length }})</span>
          </h3>
        </div>

        <div v-if="loading" class="flex-1 flex flex-col items-center justify-center p-6 space-y-2 text-slate-400">
          <Loader2 class="w-6 h-6 animate-spin text-[#308e87]" />
          <span class="text-xs font-bold">Memuat peta &amp; lokasi...</span>
        </div>

        <div v-else-if="locations.length === 0" class="flex-1 flex flex-col items-center justify-center p-6 text-center space-y-2 text-slate-400">
          <FileX class="w-8 h-8 opacity-40" />
          <span class="text-xs font-bold">Belum ada lokasi GIS terdaftar untuk filter ini.</span>
        </div>

        <div v-else class="flex-1 overflow-y-auto space-y-2 pt-3 pr-1">
          <div 
            v-for="item in locations" 
            :key="item.id_lokasi"
            @click="focusOnMap(item)"
            class="p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 hover:border-[#308e87] dark:hover:border-[#3aada4] transition-all cursor-pointer space-y-1.5 group shadow-xs"
          >
            <div class="flex items-center justify-between gap-1">
              <span class="px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-wider bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]">
                {{ item.jenis_geometry || 'Point' }}
              </span>
              <span class="text-[10px] font-bold text-slate-400 truncate max-w-[110px]">{{ item.nama_opd }}</span>
            </div>

            <h4 class="font-bold text-xs text-slate-900 dark:text-white leading-snug group-hover:text-[#308e87] transition-colors line-clamp-2">
              {{ item.nama_lokasi || item.nama_pekerjaan }}
            </h4>

            <div class="flex items-center justify-between text-[10px] font-bold border-t border-slate-200/50 dark:border-slate-700/50 pt-1.5 text-slate-500">
              <span>Pagu: Rp {{ formatNumber(item.pagu_anggaran) }}</span>
              <span class="text-purple-600 dark:text-purple-400">{{ item.realisasi_fisik ? item.realisasi_fisik.toFixed(1) : '0' }}%</span>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { 
  MapPin, 
  Search, 
  RefreshCw, 
  Loader2, 
  FileX, 
  Layers 
} from 'lucide-vue-next'

const locations = ref([])
const opdOptions = ref([])
const summary = ref({})
const loading = ref(false)

const searchQuery = ref('')
const selectedOpd = ref(null)
const selectedPengadaan = ref(null)

let mapInstance = null
let geoJsonLayerGroup = null
let debounceTimer = null

const formatNumber = (num) => {
  if (!num) return '0'
  const val = Number(num)
  if (val >= 1_000_000_000) {
    return (val / 1_000_000_000).toFixed(2) + ' M'
  } else if (val >= 1_000_000) {
    return (val / 1_000_000).toFixed(1) + ' Jt'
  }
  return val.toLocaleString('id-ID')
}

const fetchOpdList = async () => {
  try {
    const res = await axios.get('/api/v1/rko/opd', { params: { tahun: 2026 } })
    opdOptions.value = res.data
  } catch (err) {
    console.warn('Gagal memuat OPD list:', err)
  }
}

const fetchSummary = async () => {
  try {
    const res = await axios.get('/api/v1/peta/summary', { params: { tahun: 2026 } })
    summary.value = res.data
  } catch (err) {
    console.warn('Gagal memuat summary peta:', err)
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = { tahun: 2026 }
    if (selectedOpd.value) params.id_sub_pd = selectedOpd.value
    if (selectedPengadaan.value) params.jenis_pengadaan = selectedPengadaan.value
    if (searchQuery.value.trim()) params.search = searchQuery.value.trim()

    const res = await axios.get('/api/v1/peta/locations', { params })
    locations.value = res.data
    renderLocationsOnMap()
  } catch (err) {
    console.warn('Gagal memuat data peta locations:', err)
  } finally {
    loading.value = false
  }
}

const debounceFetch = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    fetchData()
  }, 400)
}

const initMap = () => {
  const mapEl = document.getElementById('peta-simlaba-full')
  if (!mapEl) return

  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }

  // Kota Tegal default center [-6.86942, 109.13824]
  mapInstance = L.map('peta-simlaba-full').setView([-6.86942, 109.13824], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | SIMLABA Kota Tegal'
  }).addTo(mapInstance)

  geoJsonLayerGroup = L.featureGroup().addTo(mapInstance)
}

const renderLocationsOnMap = () => {
  if (!mapInstance || !geoJsonLayerGroup) return
  geoJsonLayerGroup.clearLayers()

  if (locations.value.length === 0) return

  locations.value.forEach((loc) => {
    const jenisGeom = loc.jenis_geometry || 'Point'
    const color = jenisGeom === 'Point' ? '#308e87' : jenisGeom === 'LineString' ? '#2563eb' : '#10b981'

    const popupHtml = `
      <div class="p-3 font-sans max-w-xs space-y-2">
        <div class="flex items-center justify-between gap-2 border-b border-slate-100 pb-1.5">
          <span class="text-[9px] font-extrabold px-2 py-0.5 rounded-full uppercase bg-[#308e87]/20 text-[#308e87]">
            ${jenisGeom}
          </span>
          <span class="text-[10px] font-bold text-slate-500">${loc.nama_opd}</span>
        </div>

        <div>
          <h3 class="font-bold text-xs text-slate-900 leading-snug">${loc.nama_pekerjaan}</h3>
          <p class="text-[11px] text-slate-500 mt-0.5">${loc.nama_lokasi || loc.lokasi_text || 'Kota Tegal'}</p>
        </div>

        <div class="bg-slate-50 p-2 rounded-xl text-[11px] space-y-1 font-semibold text-slate-700">
          <div class="flex justify-between">
            <span>Pagu Anggaran:</span>
            <span class="font-black text-slate-900">Rp ${Number(loc.pagu_anggaran).toLocaleString('id-ID')}</span>
          </div>
          <div class="flex justify-between">
            <span>Realisasi Keuangan:</span>
            <span class="font-bold text-emerald-700">Rp ${Number(loc.realisasi_keuangan).toLocaleString('id-ID')}</span>
          </div>
          <div class="flex justify-between">
            <span>Realisasi Fisik:</span>
            <span class="font-black text-purple-700">${Number(loc.realisasi_fisik).toFixed(1)}%</span>
          </div>
        </div>
      </div>
    `

    if (loc.geojson && loc.geojson.type) {
      const geoLayer = L.geoJSON(loc.geojson, {
        style: { color: color, weight: 4, opacity: 0.85, fillOpacity: 0.35 }
      })
      geoLayer.bindPopup(popupHtml)
      geoJsonLayerGroup.addLayer(geoLayer)
    } else if (loc.lat && loc.lng) {
      const customIcon = L.divIcon({
        className: 'simlaba-custom-pin',
        html: `<div style="background-color: ${color}; width: 22px; height: 22px; border: 3px solid white; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.35);"></div>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      })
      const marker = L.marker([loc.lat, loc.lng], { icon: customIcon })
      marker.bindPopup(popupHtml)
      geoJsonLayerGroup.addLayer(marker)
    }
  })

  if (geoJsonLayerGroup.getLayers().length > 0) {
    try {
      mapInstance.fitBounds(geoJsonLayerGroup.getBounds(), { padding: [40, 40] })
    } catch (e) {}
  }
}

const focusOnMap = (item) => {
  if (!mapInstance) return
  if (item.lat && item.lng) {
    mapInstance.setView([item.lat, item.lng], 16, { animate: true })
  }
}

onMounted(async () => {
  fetchOpdList()
  fetchSummary()
  await nextTick()
  initMap()
  fetchData()
})
</script>
