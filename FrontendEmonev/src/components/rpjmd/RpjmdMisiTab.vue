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
            placeholder="Cari uraian misi RPJMD..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>

        <!-- View mode toggle -->
        <div class="flex items-center bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shrink-0">
          <button 
            @click="misiViewMode = 'grid'"
            :class="misiViewMode === 'grid' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
            class="px-3 py-1 text-xs font-bold rounded-lg transition-all cursor-pointer"
          >
            Grid
          </button>
          <button 
            @click="misiViewMode = 'table'"
            :class="misiViewMode === 'table' ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'"
            class="px-3 py-1 text-xs font-bold rounded-lg transition-all cursor-pointer"
          >
            Tabel
          </button>
        </div>

        <button 
          @click="fetchMisiData"
          class="p-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer shrink-0"
          title="Segarkan Data Misi RPJMD"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loadingMisi }" />
        </button>
      </div>

      <div class="flex items-center space-x-3 self-end md:self-center">
        <span class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <strong>{{ misiList.length }}</strong> Misi RPJMD (Tabel: <code class="font-mono text-[10px]">rpjmd_misi</code>)
        </span>
        <button 
          @click="openAddMisiModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#308e87] hover:bg-[#27756f] text-white flex items-center space-x-1.5 shadow-sm shadow-[#308e87]/30 transition-all cursor-pointer"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Misi RPJMD</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingMisi" class="py-16 flex flex-col items-center justify-center space-y-3 text-slate-400">
      <Loader2 class="w-8 h-8 animate-spin text-[#308e87]" />
      <span class="text-xs font-bold">Memuat Misi RPJMD...</span>
    </div>

    <!-- Grid View Mode -->
    <div v-else-if="misiViewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="m in filteredMisiList" 
        :key="m.idmisi"
        class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 hover:border-[#308e87]/50 dark:hover:border-[#308e87]/50 rounded-2xl p-5 shadow-sm transition-all flex flex-col justify-between group relative"
      >
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="px-3 py-1 rounded-xl text-xs font-black bg-[#308e87] text-white shadow-sm shadow-[#308e87]/30">
                Misi {{ m.urut || 1 }}
              </span>
              <span class="text-[10px] font-mono text-slate-400">UUID: {{ (m.idmisi || '').substring(0, 8) }}...</span>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center space-x-1 opacity-80 group-hover:opacity-100 transition-opacity">
              <button 
                @click="openEditMisiModal(m)"
                class="p-1.5 rounded-lg text-slate-400 hover:text-[#308e87] hover:bg-[#308e87]/10 cursor-pointer"
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
        </div>

        <div class="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-[10px] text-slate-400">
          <span>Urutan: #{{ m.urut }}</span>
          <span v-if="m.postdate" class="font-mono">Tgl: {{ new Date(m.postdate).toLocaleDateString('id-ID') }}</span>
        </div>
      </div>
    </div>

    <!-- Table View Mode -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
              <th class="py-3 px-4 w-20 text-center">Urutan</th>
              <th class="py-3 px-4 min-w-[360px]">Uraian Misi RPJMD Kota Tegal (Tabel: rpjmd_misi)</th>
              <th class="py-3 px-4 w-40 text-center">ID / UUID</th>
              <th class="py-3 px-4 w-24 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
            <tr v-for="m in filteredMisiList" :key="m.idmisi" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
              <td class="py-3 px-4 text-center font-black">
                <span class="px-2.5 py-1 rounded-lg text-xs bg-[#308e87] text-white">
                  Misi {{ m.urut }}
                </span>
              </td>
              <td class="py-3 px-4 font-bold text-slate-900 dark:text-white leading-relaxed">
                {{ m.uraimisi }}
              </td>
              <td class="py-3 px-4 text-center font-mono text-[10px] text-slate-400">
                {{ (m.idmisi || '').substring(0, 13) }}...
              </td>
              <td class="py-3 px-4 text-center">
                <div class="flex items-center justify-center space-x-1">
                  <button 
                    @click="openEditMisiModal(m)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-[#308e87] hover:bg-[#308e87]/10 cursor-pointer"
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

    <!-- ==================== MODAL: TAMBAH / EDIT MISI RPJMD ==================== -->
    <div 
      v-if="showMisiModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showMisiModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Flag class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditMisi ? 'Edit Misi RPJMD' : 'Tambah Misi RPJMD' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjmd_misi</code></p>
            </div>
          </div>
          <button @click="showMisiModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveMisiData" class="space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut Misi</label>
            <input 
              v-model.number="misiForm.urut" 
              type="number" 
              min="1"
              required
              placeholder="Contoh: 1, 2, 3..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Misi RPJMD</label>
            <textarea 
              v-model="misiForm.uraimisi" 
              rows="4" 
              required
              placeholder="Masukkan uraian misi RPJMD..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none leading-relaxed font-semibold"
            ></textarea>
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
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
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
  urut: 1
})

const filteredMisiList = computed(() => {
  if (!searchQueryMisi.value) return misiList.value
  const q = searchQueryMisi.value.toLowerCase()
  return misiList.value.filter(m => 
    (m.uraimisi && m.uraimisi.toLowerCase().includes(q)) || 
    (m.urut && m.urut.toString().includes(q))
  )
})

async function fetchMisiData() {
  loadingMisi.value = true
  try {
    const res = await axios.get('/api/v1/rpjmd/misi')
    if (Array.isArray(res.data)) {
      misiList.value = res.data
    }
  } catch (err) {
    console.error('Error fetching RPJMD Misi data:', err)
  } finally {
    loadingMisi.value = false
  }
}

function openAddMisiModal() {
  isEditMisi.value = false
  currentMisiId.value = null
  misiForm.value = {
    idmisi: '',
    uraimisi: '',
    urut: misiList.value.length + 1
  }
  showMisiModal.value = true
}

function openEditMisiModal(m) {
  isEditMisi.value = true
  currentMisiId.value = m.idmisi
  misiForm.value = {
    idmisi: m.idmisi,
    uraimisi: m.uraimisi,
    urut: m.urut || 1
  }
  showMisiModal.value = true
}

async function saveMisiData() {
  savingMisi.value = true
  try {
    const payload = {
      uraimisi: misiForm.value.uraimisi,
      urut: misiForm.value.urut
    }

    if (isEditMisi.value) {
      await axios.put(`/api/v1/rpjmd/misi/${currentMisiId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjmd/misi', payload)
    }
    showMisiModal.value = false
    await fetchMisiData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditMisi.value ? 'Misi RPJMD berhasil diperbarui' : 'Misi RPJMD baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Misi RPJMD', 'error')
  } finally {
    savingMisi.value = false
  }
}

async function handleDeleteMisi(m) {
  const result = await Swal.fire({
    title: 'Hapus Misi RPJMD?',
    html: `Apakah Anda yakin ingin menghapus Misi [<strong>Misi ${m.urut}</strong>]: <br/>"${m.uraimisi.substring(0, 80)}..."?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjmd/misi/${m.idmisi}`)
      await fetchMisiData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Misi RPJMD berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Misi RPJMD', 'error')
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
