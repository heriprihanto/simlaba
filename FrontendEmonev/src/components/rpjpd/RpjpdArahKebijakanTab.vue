<template>
  <div class="space-y-4">
    
    <!-- Filter & Toolbar -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-3 shadow-sm">
      <div class="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
        <!-- Search input -->
        <div class="relative w-full sm:w-64">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQueryArah"
            type="text" 
            placeholder="Cari arah kebijakan..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>

        <!-- Filter Periode RPJMD Dropdown -->
        <div class="flex items-center space-x-1.5">
          <label class="text-[11px] font-bold text-slate-500 dark:text-slate-400">Periode:</label>
          <select 
            v-model="selectedTahap"
            class="px-3 py-2 text-xs font-bold rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="">Semua Periode</option>
            <option value="1">1 (2025–2029)</option>
            <option value="2">2 (2030–2034)</option>
            <option value="3">3 (2035–2039)</option>
            <option value="4">4 (2040–2045)</option>
          </select>
        </div>

        <!-- Filter Misi Dropdown -->
        <div class="flex items-center space-x-1.5">
          <label class="text-[11px] font-bold text-slate-500 dark:text-slate-400">Misi:</label>
          <select 
            v-model="selectedMisiArah"
            class="px-3 py-2 text-xs font-bold rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-amber-500 max-w-[180px] truncate"
          >
            <option value="">Semua Misi</option>
            <option v-for="m in misiList" :key="m.idmisi" :value="m.idmisi">
              Misi {{ m.idmisi }}: {{ m.uraimisi.substring(0, 30) }}...
            </option>
          </select>
        </div>

        <button 
          @click="fetchArahKebijakanData"
          class="p-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer shrink-0"
          title="Segarkan Data Arah Kebijakan"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loadingArah }" />
        </button>
      </div>

      <div class="flex items-center space-x-3 self-end md:self-center">
        <span class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <strong>{{ filteredArahKebijakanList.length }}</strong> Arah Kebijakan
        </span>
        <button 
          @click="openAddArahModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-600 hover:bg-amber-700 text-white flex items-center space-x-1.5 shadow-sm shadow-amber-600/30 transition-all cursor-pointer"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Arah Kebijakan</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingArah" class="py-16 flex flex-col items-center justify-center space-y-3 text-slate-400">
      <Loader2 class="w-8 h-8 animate-spin text-amber-500" />
      <span class="text-xs font-bold">Memuat Arah Kebijakan...</span>
    </div>

    <!-- Table View with 4 Columns for Periode Pelaksanaan RPJMD -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-100/90 dark:bg-slate-800/90 text-[10px] font-black uppercase tracking-wider text-slate-600 dark:text-slate-300">
              <th rowspan="2" class="py-3 px-4 w-16 text-center border-r border-slate-200 dark:border-slate-700/80">No / ID</th>
              <th rowspan="2" class="py-3 px-4 min-w-[200px] border-r border-slate-200 dark:border-slate-700/80">Sasaran Pembangunan</th>
              <th rowspan="2" class="py-3 px-4 min-w-[280px] border-r border-slate-200 dark:border-slate-700/80">Uraian Arah Kebijakan (Tabel: rpjpd_arah_kebijakan)</th>
              <th colspan="4" class="py-2 px-2 text-center border-b border-r border-slate-200 dark:border-slate-700/80 bg-amber-500/10 text-amber-700 dark:text-amber-300 font-black">
                Periode Pelaksanaan RPJMD
              </th>
              <th rowspan="2" class="py-3 px-4 text-center w-24">Aksi</th>
            </tr>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-amber-50/5 dark:bg-amber-950/20 text-[10px] font-bold text-slate-600 dark:text-slate-300">
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-blue-700 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20">
                1<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2025–2029)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-teal-700 dark:text-teal-400 bg-teal-50/40 dark:bg-teal-950/20">
                2<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2030–2034)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-amber-700 dark:text-amber-400 bg-amber-50/40 dark:bg-amber-950/20">
                3<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2035–2039)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-emerald-700 dark:text-emerald-400 bg-emerald-50/40 dark:bg-emerald-950/20">
                4<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2040–2045)</span>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
            <tr v-if="filteredArahKebijakanList.length === 0">
              <td colspan="8" class="py-8 text-center text-slate-400 italic">
                Tidak ada data Arah Kebijakan yang sesuai dengan filter.
              </td>
            </tr>

            <tr 
              v-for="(item, idx) in filteredArahKebijakanList" 
              :key="item.id || idx"
              class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
            >
              <!-- No / ID -->
              <td class="py-3.5 px-4 text-center font-black border-r border-slate-100 dark:border-slate-800/60">
                <span class="px-2.5 py-1 rounded-lg text-xs font-black bg-amber-500/10 text-amber-700 dark:text-amber-400">
                  #{{ item.idarahkebijakan || (idx + 1) }}
                </span>
              </td>
              
              <!-- Sasaran (Menggantikan Misi) -->
              <td class="py-3.5 px-4 border-r border-slate-100 dark:border-slate-800/60">
                <div class="space-y-1">
                  <div class="flex items-center space-x-1.5" v-if="item.idsasaran">
                    <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300">
                      Kode: {{ item.idsasaran }}
                    </span>
                  </div>
                  <p class="text-xs font-semibold text-slate-800 dark:text-slate-200 leading-snug">
                    {{ item.uraisasaran || '-' }}
                  </p>
                </div>
              </td>

              <!-- Uraian Arah Kebijakan -->
              <td class="py-3.5 px-4 font-bold text-slate-900 dark:text-white leading-relaxed border-r border-slate-100 dark:border-slate-800/60">
                {{ item.arahkebijakan }}
              </td>

              <!-- Kolom Periode Pelaksanaan RPJMD: 1 -->
              <td class="py-3.5 px-2 text-center border-r border-slate-100 dark:border-slate-800/60 bg-blue-50/20 dark:bg-blue-950/10">
                <span 
                  v-if="isPeriodeActive(item, '1')" 
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-blue-500 text-white font-black text-xs shadow-sm"
                  title="Periode 1 (2025–2029)"
                >
                  ✓
                </span>
                <span v-else class="text-slate-300 dark:text-slate-600 font-bold">-</span>
              </td>

              <!-- Kolom Periode Pelaksanaan RPJMD: 2 -->
              <td class="py-3.5 px-2 text-center border-r border-slate-100 dark:border-slate-800/60 bg-teal-50/20 dark:bg-teal-950/10">
                <span 
                  v-if="isPeriodeActive(item, '2')" 
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-teal-500 text-white font-black text-xs shadow-sm"
                  title="Periode 2 (2030–2034)"
                >
                  ✓
                </span>
                <span v-else class="text-slate-300 dark:text-slate-600 font-bold">-</span>
              </td>

              <!-- Kolom Periode Pelaksanaan RPJMD: 3 -->
              <td class="py-3.5 px-2 text-center border-r border-slate-100 dark:border-slate-800/60 bg-amber-50/20 dark:bg-amber-950/10">
                <span 
                  v-if="isPeriodeActive(item, '3')" 
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-500 text-white font-black text-xs shadow-sm"
                  title="Periode 3 (2035–2039)"
                >
                  ✓
                </span>
                <span v-else class="text-slate-300 dark:text-slate-600 font-bold">-</span>
              </td>

              <!-- Kolom Periode Pelaksanaan RPJMD: 4 -->
              <td class="py-3.5 px-2 text-center border-r border-slate-100 dark:border-slate-800/60 bg-emerald-50/20 dark:bg-emerald-950/10">
                <span 
                  v-if="isPeriodeActive(item, '4')" 
                  class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500 text-white font-black text-xs shadow-sm"
                  title="Periode 4 (2040–2045)"
                >
                  ✓
                </span>
                <span v-else class="text-slate-300 dark:text-slate-600 font-bold">-</span>
              </td>

              <!-- Actions -->
              <td class="py-3.5 px-4 text-center">
                <div class="flex items-center justify-center space-x-1">
                  <button 
                    @click="openEditArahModal(item)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-950/40 cursor-pointer"
                    title="Edit Arah Kebijakan"
                  >
                    <Edit3 class="w-3.5 h-3.5" />
                  </button>
                  <button 
                    @click="handleDeleteArah(item)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                    title="Hapus Arah Kebijakan"
                  >
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ==================== MODAL: TAMBAH / EDIT ARAH KEBIJAKAN ==================== -->
    <div 
      v-if="showArahModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showArahModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
              <Milestone class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditArah ? 'Edit Arah Kebijakan' : 'Tambah Arah Kebijakan' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_arah_kebijakan</code></p>
            </div>
          </div>
          <button @click="showArahModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveArahData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor / ID Arah Kebijakan</label>
              <input 
                v-model="arahForm.idarahkebijakan" 
                type="text" 
                required
                placeholder="Contoh: 1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none font-bold"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Misi Terkait</label>
              <select 
                v-model="arahForm.idmisi" 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none font-bold"
              >
                <option v-for="m in misiList" :key="m.idmisi" :value="m.idmisi">
                  Misi {{ m.idmisi }}: {{ m.uraimisi.substring(0, 45) }}...
                </option>
              </select>
            </div>
          </div>

          <!-- Pilihan Multi-Periode Pelaksanaan RPJMD 1, 2, 3, 4 -->
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1.5">
              Periode Pelaksanaan RPJMD (Bisa Pilih Lebih dari 1)
            </label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <label 
                v-for="p in [
                  { key: '1', label: '1 (2025–2029)', color: 'blue' },
                  { key: '2', label: '2 (2030–2034)', color: 'teal' },
                  { key: '3', label: '3 (2035–2039)', color: 'amber' },
                  { key: '4', label: '4 (2040–2045)', color: 'emerald' }
                ]"
                :key="p.key"
                class="flex items-center space-x-2 p-2 rounded-xl border cursor-pointer transition-all"
                :class="arahForm.selectedTahapan && arahForm.selectedTahapan.includes(p.key) 
                  ? 'border-amber-500 bg-amber-50/50 dark:bg-amber-950/30' 
                  : 'border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/40'"
              >
                <input 
                  type="checkbox" 
                  :value="p.key"
                  v-model="arahForm.selectedTahapan"
                  class="rounded text-amber-600 focus:ring-amber-500 w-4 h-4"
                />
                <span class="text-xs font-bold text-slate-700 dark:text-slate-200">
                  {{ p.label }}
                </span>
              </label>
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Sasaran Terkait</label>
            <input 
              v-model="arahForm.uraisasaran" 
              type="text" 
              placeholder="Contoh: Meningkatnya Daya Saing Perekonomian..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Arah Kebijakan</label>
            <textarea 
              v-model="arahForm.arahkebijakan" 
              rows="4" 
              required
              placeholder="Masukkan uraian arah kebijakan pembangunan daerah..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-amber-500 focus:outline-none leading-relaxed"
            ></textarea>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showArahModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingArah"
              class="px-5 py-2 rounded-xl font-black text-xs bg-amber-600 hover:bg-amber-700 text-white shadow-md shadow-amber-600/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingArah" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditArah ? 'Simpan Perubahan' : 'Tambah Arah Kebijakan' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { Milestone, Search, Plus, RotateCw, Loader2, Edit3, Trash2 } from 'lucide-vue-next'

const props = defineProps({
  initialMisi: {
    type: String,
    default: ''
  }
})

const searchQueryArah = ref('')
const selectedTahap = ref('')
const selectedMisiArah = ref(props.initialMisi || '')
const loadingArah = ref(false)
const savingArah = ref(false)

const arahKebijakanList = ref([])
const misiList = ref([])

const showArahModal = ref(false)
const isEditArah = ref(false)
const currentArahId = ref(null)
const arahForm = ref({
  idarahkebijakan: '',
  urut: 1,
  no: 1,
  idmisi: '1',
  selectedTahapan: ['1'],
  uraisasaran: '',
  arahkebijakan: ''
})

const filteredArahKebijakanList = computed(() => {
  return arahKebijakanList.value.filter(item => {
    const matchTahap = !selectedTahap.value || (
      Array.isArray(item.periode_rpjmd_pelaksanaan) && item.periode_rpjmd_pelaksanaan.map(String).includes(String(selectedTahap.value))
    )
    const matchMisi = !selectedMisiArah.value || item.idmisi === selectedMisiArah.value
    const q = searchQueryArah.value.toLowerCase()
    const matchSearch = !q || 
      (item.arahkebijakan && item.arahkebijakan.toLowerCase().includes(q)) ||
      (item.uraisasaran && item.uraisasaran.toLowerCase().includes(q)) ||
      (item.idarahkebijakan && item.idarahkebijakan.toLowerCase().includes(q))
    return matchTahap && matchMisi && matchSearch
  })
})

function isPeriodeActive(item, periodeKey) {
  if (!item || !item.periode_rpjmd_pelaksanaan) return false
  if (Array.isArray(item.periode_rpjmd_pelaksanaan)) {
    return item.periode_rpjmd_pelaksanaan.map(String).includes(String(periodeKey))
  }
  return String(item.periode_rpjmd_pelaksanaan) === String(periodeKey)
}

async function fetchArahKebijakanData() {
  loadingArah.value = true
  try {
    const res = await axios.get('/api/v1/rpjpd/arah-kebijakan')
    if (Array.isArray(res.data)) {
      arahKebijakanList.value = res.data
    }
  } catch (err) {
    console.error('Error fetching RPJPD Arah Kebijakan data:', err)
  } finally {
    loadingArah.value = false
  }
}

async function fetchMisiList() {
  try {
    const res = await axios.get('/api/v1/rpjpd/misi')
    if (Array.isArray(res.data)) {
      misiList.value = res.data
    }
  } catch (err) {
    console.error('Error fetching Misi for dropdown:', err)
  }
}

function openAddArahModal() {
  isEditArah.value = false
  currentArahId.value = null
  arahForm.value = {
    idarahkebijakan: (arahKebijakanList.value.length + 1).toString(),
    urut: arahKebijakanList.value.length + 1,
    no: arahKebijakanList.value.length + 1,
    idmisi: misiList.value[0]?.idmisi || '1',
    selectedTahapan: ['1'],
    uraisasaran: '',
    arahkebijakan: ''
  }
  showArahModal.value = true
}

function openEditArahModal(item) {
  isEditArah.value = true
  currentArahId.value = item.id
  const currentTahapList = Array.isArray(item.periode_rpjmd_pelaksanaan) && item.periode_rpjmd_pelaksanaan.length > 0 
    ? item.periode_rpjmd_pelaksanaan.map(String) 
    : ['1']
  arahForm.value = {
    idarahkebijakan: item.idarahkebijakan,
    urut: item.urut || item.no || 1,
    no: item.no || 1,
    idmisi: item.idmisi || '1',
    selectedTahapan: currentTahapList,
    uraisasaran: item.uraisasaran || '',
    arahkebijakan: item.arahkebijakan
  }
  showArahModal.value = true
}

async function saveArahData() {
  if (!arahForm.value.selectedTahapan || arahForm.value.selectedTahapan.length === 0) {
    Swal.fire('Perhatian', 'Pilih minimal satu Periode Pelaksanaan RPJMD (1, 2, 3, atau 4)', 'warning')
    return
  }

  savingArah.value = true
  try {
    const payload = {
      idarahkebijakan: arahForm.value.idarahkebijakan,
      urut: arahForm.value.urut,
      no: arahForm.value.no,
      idmisi: arahForm.value.idmisi,
      periode_rpjmd_pelaksanaan: arahForm.value.selectedTahapan,
      uraisasaran: arahForm.value.uraisasaran,
      arahkebijakan: arahForm.value.arahkebijakan
    }

    if (isEditArah.value) {
      await axios.put(`/api/v1/rpjpd/arah-kebijakan/${currentArahId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/arah-kebijakan', {
        ...payload,
        idperiode: '20252045',
        kodepemda: '3376'
      })
    }
    showArahModal.value = false
    await fetchArahKebijakanData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditArah.value ? 'Arah Kebijakan berhasil diperbarui' : 'Arah Kebijakan baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Arah Kebijakan', 'error')
  } finally {
    savingArah.value = false
  }
}

async function handleDeleteArah(item) {
  const result = await Swal.fire({
    title: 'Hapus Arah Kebijakan?',
    html: `Apakah Anda yakin ingin menghapus Arah Kebijakan [<strong>#${item.idarahkebijakan}</strong>]: <br/>"${item.arahkebijakan.substring(0, 80)}..."?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/arah-kebijakan/${item.id}`)
      await fetchArahKebijakanData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Arah Kebijakan berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Arah Kebijakan', 'error')
    }
  }
}

function setMisiFilter(idmisi) {
  selectedMisiArah.value = idmisi
}

onMounted(() => {
  fetchArahKebijakanData()
  fetchMisiList()
})

defineExpose({
  fetchArahKebijakanData,
  arahKebijakanList,
  setMisiFilter
})
</script>
