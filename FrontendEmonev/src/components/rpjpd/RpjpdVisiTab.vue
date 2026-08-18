<template>
  <div class="space-y-6">
    
    <!-- 1. KARTU VISI UTAMA DAERAH -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#308e87] via-[#236b65] to-[#123835] text-white p-7 shadow-xl shadow-[#308e87]/20 border border-teal-500/20">
      <div class="absolute -right-10 -bottom-10 w-72 h-72 bg-white/5 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute right-6 top-6 opacity-10 pointer-events-none">
        <Compass class="w-44 h-44" />
      </div>

      <div class="relative z-10 space-y-4 max-w-4xl">
        <div class="flex flex-wrap items-center gap-2.5">
          <span class="px-3 py-1 rounded-full text-xs font-black bg-white/20 backdrop-blur-md text-white border border-white/30 tracking-wider uppercase flex items-center space-x-1.5">
            <Sparkles class="w-3.5 h-3.5" />
            <span>Visi Daerah RPJPD {{ visiData.idperiode || '2025–2045' }}</span>
          </span>
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-400/20 text-emerald-200 border border-emerald-400/30">
            Tabel: rpjpd_visi
          </span>
          <span class="px-3 py-1 rounded-full text-xs font-mono font-bold bg-white/10 text-white/90">
            Kode Pemda: {{ visiData.kodepemda || '3376' }}
          </span>
        </div>

        <div v-if="loadingVisi" class="py-6 flex items-center space-x-3 text-white/80">
          <Loader2 class="w-6 h-6 animate-spin" />
          <span class="text-sm font-semibold">Memuat Visi Daerah...</span>
        </div>

        <div v-else>
          <h2 class="text-2xl sm:text-3xl font-black tracking-tight leading-snug drop-shadow-sm">
            “{{ visiData.uraivisi || 'Kota Tegal yang Maju, Berakhlak, Sejahtera dan Berkelanjutan' }}”
          </h2>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-4 pt-3 border-t border-white/15 text-xs text-teal-100">
          <div class="flex items-center space-x-4">
            <span class="flex items-center space-x-1.5">
              <CheckCircle2 class="w-4 h-4 text-emerald-300" />
              <span>Status: <strong>Aktif / Terverifikasi</strong></span>
            </span>
            <span>ID Dokumen: <code class="font-mono bg-black/20 px-2 py-0.5 rounded">{{ visiData.id || 'default' }}</code></span>
          </div>

          <button 
            @click="openEditVisiModal"
            class="px-4 py-2 rounded-xl text-xs font-black bg-white text-[#308e87] hover:bg-teal-50 shadow-md shadow-black/10 transition-all flex items-center space-x-1.5 cursor-pointer"
          >
            <Edit3 class="w-3.5 h-3.5" />
            <span>Edit Visi Daerah</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 2. KARTU PENJELASAN POKOK-POKOK VISI -->
    <div class="space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center space-x-2">
            <span>Penjelasan Pokok-Pokok Visi</span>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#308e87]/10 text-[#308e87] border border-[#308e87]/20">
              {{ penjelasanVisiList.length }} Pokok Visi
            </span>
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Uraian mendalam arah capaian pokok-pokok visi pembangunan jangka panjang Kota Tegal (Tabel: <code class="font-mono">rpjpd_penjelasan_visi</code>)
          </p>
        </div>

        <div class="flex items-center space-x-2">
          <!-- View mode toggle -->
          <div class="flex items-center bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
            <button 
              @click="penjelasanViewMode = 'grid'"
              :class="penjelasanViewMode === 'grid' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
              class="px-3 py-1 text-xs font-bold rounded-lg transition-all"
            >
              Grid
            </button>
            <button 
              @click="penjelasanViewMode = 'table'"
              :class="penjelasanViewMode === 'table' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
              class="px-3 py-1 text-xs font-bold rounded-lg transition-all"
            >
              Tabel
            </button>
          </div>

          <button 
            @click="openAddPenjelasanModal"
            class="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#308e87] hover:bg-[#27756f] text-white flex items-center space-x-1.5 shadow-sm shadow-[#308e87]/30 transition-all cursor-pointer"
          >
            <Plus class="w-3.5 h-3.5" />
            <span>Tambah Pokok Visi</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loadingVisi" class="py-12 flex flex-col items-center justify-center space-y-3 text-slate-400">
        <Loader2 class="w-8 h-8 animate-spin text-[#308e87]" />
        <span class="text-xs font-bold">Memuat Penjelasan Visi...</span>
      </div>

      <!-- Grid Mode -->
      <div v-else-if="penjelasanViewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="item in penjelasanVisiList" 
          :key="item.id || item.kodepenjelasan"
          class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 hover:border-[#308e87]/40 dark:hover:border-[#308e87]/40 rounded-2xl p-5 shadow-sm transition-all group relative flex flex-col justify-between"
        >
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span class="px-2.5 py-1 rounded-lg text-xs font-black bg-[#308e87]/10 text-[#308e87] border border-[#308e87]/20">
                  #{{ item.no || item.kodepenjelasan }}
                </span>
                <span class="text-[10px] font-mono text-slate-400">Kode: {{ item.kodepenjelasan }}</span>
              </div>

              <!-- Quick action buttons -->
              <div class="flex items-center space-x-1 opacity-80 group-hover:opacity-100 transition-opacity">
                <button 
                  @click="openEditPenjelasanModal(item)"
                  class="p-1.5 rounded-lg text-slate-400 hover:text-[#308e87] hover:bg-[#308e87]/10 cursor-pointer"
                  title="Edit Pokok Visi"
                >
                  <Edit3 class="w-3.5 h-3.5" />
                </button>
                <button 
                  @click="handleDeletePenjelasan(item)"
                  class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                  title="Hapus Pokok Visi"
                >
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <h4 class="text-base font-black text-slate-900 dark:text-white tracking-tight">
              {{ item.pokokvisi }}
            </h4>

            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-normal">
              {{ item.penjelasanvisi }}
            </p>
          </div>

          <div class="pt-4 mt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400">
            <span>Periode: {{ item.idperiode || '20252045' }}</span>
            <span class="font-mono">Pemda: {{ item.kodepemda || '3376' }}</span>
          </div>
        </div>
      </div>

      <!-- Table Mode -->
      <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th class="py-3 px-4 w-16 text-center">No</th>
                <th class="py-3 px-4 w-24 text-center">Kode</th>
                <th class="py-3 px-4 w-52">Pokok Visi</th>
                <th class="py-3 px-4 min-w-[320px]">Penjelasan Pokok Visi</th>
                <th class="py-3 px-4 w-24 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
              <tr v-for="item in penjelasanVisiList" :key="item.id || item.kodepenjelasan" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
                <td class="py-3 px-4 text-center font-bold text-slate-700 dark:text-slate-300">{{ item.no || '-' }}</td>
                <td class="py-3 px-4 text-center font-mono font-bold text-[#308e87]">{{ item.kodepenjelasan }}</td>
                <td class="py-3 px-4 font-black text-slate-900 dark:text-white">{{ item.pokokvisi }}</td>
                <td class="py-3 px-4 text-slate-600 dark:text-slate-300 leading-relaxed">{{ item.penjelasanvisi }}</td>
                <td class="py-3 px-4 text-center">
                  <div class="flex items-center justify-center space-x-1">
                    <button 
                      @click="openEditPenjelasanModal(item)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-[#308e87] hover:bg-[#308e87]/10 cursor-pointer"
                      title="Edit Pokok Visi"
                    >
                      <Edit3 class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="handleDeletePenjelasan(item)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                      title="Hapus Pokok Visi"
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
    </div>

    <!-- ==================== MODAL 1: EDIT VISI DAERAH ==================== -->
    <div 
      v-if="showVisiModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showVisiModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Compass class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">Edit Visi Daerah RPJPD</h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_visi</code></p>
            </div>
          </div>
          <button @click="showVisiModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveVisiData" class="space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Visi Daerah</label>
            <textarea 
              v-model="visiForm.uraivisi" 
              rows="3" 
              required
              placeholder="Masukkan uraian visi RPJPD..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Periode</label>
              <input 
                v-model="visiForm.idperiode" 
                type="text" 
                disabled
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800/40 text-slate-500 cursor-not-allowed"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kode Pemda</label>
              <input 
                v-model="visiForm.kodepemda" 
                type="text" 
                disabled
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800/40 text-slate-500 cursor-not-allowed"
              />
            </div>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showVisiModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingVisi"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingVisi" class="w-3.5 h-3.5 animate-spin" />
              <span>Simpan Perubahan Visi</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== MODAL 2: TAMBAH / EDIT PENJELASAN VISI ==================== -->
    <div 
      v-if="showPenjelasanModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showPenjelasanModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-lg shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Sparkles class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditPenjelasan ? 'Edit Pokok Visi' : 'Tambah Pokok Visi' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_penjelasan_visi</code></p>
            </div>
          </div>
          <button @click="showPenjelasanModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="savePenjelasanData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">No Urut</label>
              <input 
                v-model.number="penjelasanForm.no" 
                type="number" 
                min="1"
                required
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kode Penjelasan</label>
              <input 
                v-model="penjelasanForm.kodepenjelasan" 
                type="text" 
                required
                placeholder="Contoh: 1581, 1582..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-mono"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Pokok Visi</label>
            <input 
              v-model="penjelasanForm.pokokvisi" 
              type="text" 
              required
              placeholder="Contoh: Maju, Berakhlak, Sejahtera..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Penjelasan Visi</label>
            <textarea 
              v-model="penjelasanForm.penjelasanvisi" 
              rows="4" 
              required
              placeholder="Masukkan uraian mendalam pokok visi ini..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none leading-relaxed"
            ></textarea>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showPenjelasanModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingPenjelasan"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingPenjelasan" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditPenjelasan ? 'Simpan Perubahan' : 'Tambah Pokok Visi' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { Compass, Sparkles, CheckCircle2, Edit3, Trash2, Plus, Loader2 } from 'lucide-vue-next'

const penjelasanViewMode = ref('grid')
const loadingVisi = ref(false)
const savingVisi = ref(false)
const savingPenjelasan = ref(false)

const visiData = ref({
  id: '',
  idperiode: '20252045',
  kodepemda: '3376',
  status: 1,
  check_value: '307',
  uraivisi: 'Kota Tegal yang Maju, Berakhlak, Sejahtera dan Berkelanjutan',
  visi_provinsi: '"20252045"',
  catatan: '[]',
  no: 2
})

const penjelasanVisiList = ref([])

const showVisiModal = ref(false)
const visiForm = ref({ id: '', uraivisi: '', idperiode: '', kodepemda: '' })

const showPenjelasanModal = ref(false)
const isEditPenjelasan = ref(false)
const currentPenjelasanId = ref(null)
const penjelasanForm = ref({
  no: 1,
  kodepenjelasan: '',
  pokokvisi: '',
  penjelasanvisi: ''
})

async function fetchRpjpdVisiData() {
  loadingVisi.value = true
  try {
    const res = await axios.get('/api/v1/rpjpd/visi-lengkap')
    if (res.data) {
      if (res.data.visi_utama) {
        visiData.value = res.data.visi_utama
      }
      if (res.data.daftar_penjelasan) {
        penjelasanVisiList.value = res.data.daftar_penjelasan
      }
    }
  } catch (err) {
    console.error('Error fetching RPJPD Visi data:', err)
  } finally {
    loadingVisi.value = false
  }
}

function openEditVisiModal() {
  visiForm.value = {
    id: visiData.value.id,
    uraivisi: visiData.value.uraivisi,
    idperiode: visiData.value.idperiode,
    kodepemda: visiData.value.kodepemda
  }
  showVisiModal.value = true
}

async function saveVisiData() {
  savingVisi.value = true
  try {
    await axios.put(`/api/v1/rpjpd/visi/${visiForm.value.id}`, {
      uraivisi: visiForm.value.uraivisi
    })
    showVisiModal.value = false
    await fetchRpjpdVisiData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Visi Daerah berhasil diperbarui',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan perubahan visi', 'error')
  } finally {
    savingVisi.value = false
  }
}

function openAddPenjelasanModal() {
  isEditPenjelasan.value = false
  currentPenjelasanId.value = null
  penjelasanForm.value = {
    no: penjelasanVisiList.value.length + 1,
    kodepenjelasan: (1580 + penjelasanVisiList.value.length + 1).toString(),
    pokokvisi: '',
    penjelasanvisi: ''
  }
  showPenjelasanModal.value = true
}

function openEditPenjelasanModal(item) {
  isEditPenjelasan.value = true
  currentPenjelasanId.value = item.id
  penjelasanForm.value = {
    no: item.no || 1,
    kodepenjelasan: item.kodepenjelasan,
    pokokvisi: item.pokokvisi,
    penjelasanvisi: item.penjelasanvisi
  }
  showPenjelasanModal.value = true
}

async function savePenjelasanData() {
  savingPenjelasan.value = true
  try {
    const payload = {
      no: penjelasanForm.value.no,
      kodepenjelasan: penjelasanForm.value.kodepenjelasan,
      pokokvisi: penjelasanForm.value.pokokvisi,
      penjelasanvisi: penjelasanForm.value.penjelasanvisi
    }
    if (isEditPenjelasan.value) {
      await axios.put(`/api/v1/rpjpd/penjelasan-visi/${currentPenjelasanId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/penjelasan-visi', {
        ...payload,
        idperiode: visiData.value.idperiode || '20252045',
        kodepemda: visiData.value.kodepemda || '3376'
      })
    }
    showPenjelasanModal.value = false
    await fetchRpjpdVisiData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditPenjelasan.value ? 'Pokok Visi berhasil diperbarui' : 'Pokok Visi baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Pokok Visi', 'error')
  } finally {
    savingPenjelasan.value = false
  }
}

async function handleDeletePenjelasan(item) {
  const result = await Swal.fire({
    title: 'Hapus Pokok Visi?',
    text: `Apakah Anda yakin ingin menghapus pokok visi "${item.pokokvisi}"?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/penjelasan-visi/${item.id}`)
      await fetchRpjpdVisiData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Pokok Visi berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus data', 'error')
    }
  }
}

onMounted(() => {
  fetchRpjpdVisiData()
})

defineExpose({
  fetchRpjpdVisiData,
  penjelasanVisiList
})
</script>
