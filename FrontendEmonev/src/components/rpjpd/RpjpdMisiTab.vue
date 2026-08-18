<template>
  <div class="space-y-4">
    
    <!-- Toolbar -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <div class="relative w-full md:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQueryMisi"
            type="text" 
            placeholder="Cari uraian misi pembangunan..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#f39159]"
          />
        </div>

        <!-- View mode toggle -->
        <div class="flex items-center bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shrink-0">
          <button 
            @click="misiViewMode = 'grid'"
            :class="misiViewMode === 'grid' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
            class="px-3 py-1 text-xs font-bold rounded-lg transition-all"
          >
            Grid
          </button>
          <button 
            @click="misiViewMode = 'table'"
            :class="misiViewMode === 'table' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
            class="px-3 py-1 text-xs font-bold rounded-lg transition-all"
          >
            Tabel
          </button>
        </div>

        <button 
          @click="fetchMisiData"
          class="p-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer shrink-0"
          title="Segarkan Data Misi"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loadingMisi }" />
        </button>
      </div>

      <div class="flex items-center space-x-3 self-end md:self-center">
        <span class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <strong>{{ misiList.length }}</strong> Misi Pembangunan Daerah
        </span>
        <button 
          @click="openAddMisiModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#f39159] hover:bg-[#e27b41] text-white flex items-center space-x-1.5 shadow-sm shadow-[#f39159]/30 transition-all cursor-pointer"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Misi Daerah</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingMisi" class="py-16 flex flex-col items-center justify-center space-y-3 text-slate-400">
      <Loader2 class="w-8 h-8 animate-spin text-[#f39159]" />
      <span class="text-xs font-bold">Memuat Misi Daerah...</span>
    </div>

    <!-- Grid View Mode -->
    <div v-else-if="misiViewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="m in filteredMisiList" 
        :key="m.id || m.idmisi"
        class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 hover:border-[#f39159]/50 dark:hover:border-[#f39159]/50 rounded-2xl p-5 shadow-sm transition-all flex flex-col justify-between group relative"
      >
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="px-3 py-1 rounded-xl text-xs font-black bg-[#f39159] text-white shadow-sm shadow-[#f39159]/30">
                Misi {{ m.idmisi }}
              </span>
              <span class="text-[10px] font-mono text-slate-400">ID: {{ m.idmisi }}</span>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center space-x-1 opacity-80 group-hover:opacity-100 transition-opacity">
              <button 
                @click="openEditMisiModal(m)"
                class="p-1.5 rounded-lg text-slate-400 hover:text-[#f39159] hover:bg-[#f39159]/10 cursor-pointer"
                title="Edit Misi"
              >
                <Edit3 class="w-3.5 h-3.5" />
              </button>
              <button 
                @click="handleDeleteMisi(m)"
                class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                title="Hapus Misi"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          <p class="text-sm font-bold text-slate-900 dark:text-white leading-relaxed">
            {{ m.uraimisi }}
          </p>

          <div v-if="m.misi_pembangunan" class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60 text-xs">
            <span class="text-[10px] font-black uppercase text-slate-400 block mb-0.5">Misi Pembangunan:</span>
            <span class="text-slate-700 dark:text-slate-300 font-semibold">{{ m.misi_pembangunan }}</span>
          </div>

          <div v-if="m.misi_provinsi && m.misi_provinsi.length > 0" class="flex flex-wrap gap-1 items-center pt-1">
            <span class="text-[10px] font-bold text-slate-400 mr-1">Provinsi:</span>
            <span 
              v-for="(prov, pIdx) in m.misi_provinsi" 
              :key="pIdx"
              class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20"
            >
              {{ prov }}
            </span>
          </div>
        </div>

        <div class="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400">
          <span>Periode: {{ m.idperiode || '20252045' }}</span>
          <button 
            @click="$emit('selectMisiArah', m.idmisi)"
            class="text-[#f39159] hover:underline font-bold flex items-center space-x-1 cursor-pointer"
          >
            <span>Lihat Arah Kebijakan →</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Table View Mode -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
              <th class="py-3 px-4 w-20 text-center">ID Misi</th>
              <th class="py-3 px-4 min-w-[320px]">Uraian Misi Daerah</th>
              <th class="py-3 px-4 w-52">Misi Pembangunan</th>
              <th class="py-3 px-4 w-40 text-center">Misi Provinsi</th>
              <th class="py-3 px-4 w-24 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
            <tr v-for="m in filteredMisiList" :key="m.id || m.idmisi" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
              <td class="py-3 px-4 text-center font-black">
                <span class="px-2.5 py-1 rounded-lg text-xs bg-[#f39159] text-white">
                  {{ m.idmisi }}
                </span>
              </td>
              <td class="py-3 px-4 font-bold text-slate-900 dark:text-white leading-relaxed">
                {{ m.uraimisi }}
              </td>
              <td class="py-3 px-4 text-slate-600 dark:text-slate-300">
                {{ m.misi_pembangunan || '-' }}
              </td>
              <td class="py-3 px-4 text-center">
                <div class="flex flex-wrap justify-center gap-1" v-if="m.misi_provinsi && m.misi_provinsi.length > 0">
                  <span 
                    v-for="(prov, pIdx) in m.misi_provinsi" 
                    :key="pIdx"
                    class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-700 dark:text-amber-300"
                  >
                    {{ prov }}
                  </span>
                </div>
                <span v-else class="text-slate-400">-</span>
              </td>
              <td class="py-3 px-4 text-center">
                <div class="flex items-center justify-center space-x-1">
                  <button 
                    @click="openEditMisiModal(m)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-[#f39159] hover:bg-[#f39159]/10 cursor-pointer"
                    title="Edit Misi"
                  >
                    <Edit3 class="w-3.5 h-3.5" />
                  </button>
                  <button 
                    @click="handleDeleteMisi(m)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                    title="Hapus Misi"
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

    <!-- ==================== MODAL: TAMBAH / EDIT MISI DAERAH ==================== -->
    <div 
      v-if="showMisiModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showMisiModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#f39159]/10 text-[#f39159] flex items-center justify-center">
              <Flag class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditMisi ? 'Edit Misi Pembangunan' : 'Tambah Misi Pembangunan' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_misi</code></p>
            </div>
          </div>
          <button @click="showMisiModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveMisiData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor / ID Misi</label>
              <input 
                v-model="misiForm.idmisi" 
                type="text" 
                required
                placeholder="Contoh: 1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-bold"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut</label>
              <input 
                v-model.number="misiForm.urut" 
                type="number" 
                min="1"
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Misi Daerah</label>
            <textarea 
              v-model="misiForm.uraimisi" 
              rows="3" 
              required
              placeholder="Masukkan uraian misi pembangunan daerah..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none leading-relaxed"
            ></textarea>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Misi Pembangunan</label>
            <input 
              v-model="misiForm.misi_pembangunan" 
              type="text" 
              placeholder="Contoh: Transformasi Sosial, Transformasi Ekonomi..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Misi Provinsi (Pisahkan koma jika lebih dari satu)</label>
            <input 
              v-model="misiForm.misi_provinsi_text" 
              type="text" 
              placeholder="Contoh: 1, 2, 4" 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-mono"
            />
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showMisiModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingMisi"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#f39159] hover:bg-[#e27b41] text-white shadow-md shadow-[#f39159]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingMisi" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditMisi ? 'Simpan Perubahan' : 'Tambah Misi' }}</span>
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
import { Flag, Search, Plus, RotateCw, Loader2, Edit3, Trash2 } from 'lucide-vue-next'

defineEmits(['selectMisiArah'])

const searchQueryMisi = ref('')
const misiViewMode = ref('grid')
const loadingMisi = ref(false)
const savingMisi = ref(false)

const misiList = ref([])

const showMisiModal = ref(false)
const isEditMisi = ref(false)
const currentMisiId = ref(null)
const misiForm = ref({
  idmisi: '',
  uraimisi: '',
  urut: 1,
  no: 1,
  misi_pembangunan: '',
  misi_provinsi_text: ''
})

const filteredMisiList = computed(() => {
  if (!searchQueryMisi.value) return misiList.value
  const q = searchQueryMisi.value.toLowerCase()
  return misiList.value.filter(m => 
    (m.uraimisi && m.uraimisi.toLowerCase().includes(q)) || 
    (m.idmisi && m.idmisi.toLowerCase().includes(q)) ||
    (m.misi_pembangunan && m.misi_pembangunan.toLowerCase().includes(q))
  )
})

async function fetchMisiData() {
  loadingMisi.value = true
  try {
    const res = await axios.get('/api/v1/rpjpd/misi')
    if (Array.isArray(res.data)) {
      misiList.value = res.data
    }
  } catch (err) {
    console.error('Error fetching RPJPD Misi data:', err)
  } finally {
    loadingMisi.value = false
  }
}

function openAddMisiModal() {
  isEditMisi.value = false
  currentMisiId.value = null
  misiForm.value = {
    idmisi: (misiList.value.length + 1).toString(),
    uraimisi: '',
    urut: misiList.value.length + 1,
    no: misiList.value.length + 1,
    misi_pembangunan: '',
    misi_provinsi_text: ''
  }
  showMisiModal.value = true
}

function openEditMisiModal(m) {
  isEditMisi.value = true
  currentMisiId.value = m.id
  const provStr = Array.isArray(m.misi_provinsi) ? m.misi_provinsi.join(', ') : (m.misi_provinsi || '')
  misiForm.value = {
    idmisi: m.idmisi,
    uraimisi: m.uraimisi,
    urut: m.urut || m.no || 1,
    no: m.no || 1,
    misi_pembangunan: m.misi_pembangunan || '',
    misi_provinsi_text: provStr
  }
  showMisiModal.value = true
}

async function saveMisiData() {
  savingMisi.value = true
  try {
    const provArray = misiForm.value.misi_provinsi_text
      ? misiForm.value.misi_provinsi_text.split(',').map(s => s.trim()).filter(Boolean)
      : []

    const payload = {
      idmisi: misiForm.value.idmisi,
      uraimisi: misiForm.value.uraimisi,
      urut: misiForm.value.urut,
      no: misiForm.value.no,
      misi_pembangunan: misiForm.value.misi_pembangunan,
      misi_provinsi: provArray
    }

    if (isEditMisi.value) {
      await axios.put(`/api/v1/rpjpd/misi/${currentMisiId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/misi', {
        ...payload,
        idperiode: '20252045',
        kodepemda: '3376'
      })
    }
    showMisiModal.value = false
    await fetchMisiData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditMisi.value ? 'Misi berhasil diperbarui' : 'Misi baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Misi', 'error')
  } finally {
    savingMisi.value = false
  }
}

async function handleDeleteMisi(m) {
  const result = await Swal.fire({
    title: 'Hapus Misi Daerah?',
    html: `Apakah Anda yakin ingin menghapus Misi [<strong>Misi ${m.idmisi}</strong>]: <br/>"${m.uraimisi.substring(0, 80)}..."?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/misi/${m.id}`)
      await fetchMisiData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Misi berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Misi', 'error')
    }
  }
}

onMounted(() => {
  fetchMisiData()
})

defineExpose({
  fetchMisiData,
  misiList
})
</script>
