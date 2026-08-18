<template>
  <div class="space-y-6">
    
    <!-- 1. KARTU VISI UTAMA DAERAH RPJMD -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#1a4845] via-[#245f5a] to-[#308e87] text-white p-7 sm:p-8 shadow-xl shadow-[#308e87]/20 border border-teal-500/20">
      <div class="absolute -right-10 -bottom-10 w-72 h-72 bg-white/5 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute right-6 top-6 opacity-10 pointer-events-none">
        <Compass class="w-44 h-44" />
      </div>

      <div class="relative z-10 space-y-4 max-w-4xl">
        <div class="flex flex-wrap items-center gap-2.5">
          <span class="px-3 py-1 rounded-full text-xs font-black bg-[#3aada4] text-white shadow-md shadow-[#3aada4]/30 tracking-wider uppercase flex items-center space-x-1.5">
            <Sparkles class="w-3.5 h-3.5" />
            <span>Visi Kepala Daerah RPJMD {{ visiData.idperiode || '2025–2029' }}</span>
          </span>
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-white/10 text-white/90 border border-white/20">
            Tabel: rpjmd_visi
          </span>
          <span class="px-3 py-1 rounded-full text-xs font-mono font-bold bg-black/20 text-white/90">
            Pagu: {{ visiData.tahunpagu || '2026 - 2030' }}
          </span>
        </div>

        <div v-if="loadingVisi" class="py-6 flex items-center space-x-3 text-white/80">
          <Loader2 class="w-6 h-6 animate-spin" />
          <span class="text-sm font-semibold">Memuat Visi RPJMD...</span>
        </div>

        <div v-else>
          <h2 class="text-2xl sm:text-3xl font-black tracking-tight leading-snug drop-shadow-sm">
            “{{ visiData.uraivisi || 'Tegal Berdikari Dan Sejahtera, Menjadi Kota Idaman' }}”
          </h2>
        </div>

        <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-white/15 text-xs text-teal-100">
          <div class="flex items-center space-x-4">
            <span class="flex items-center space-x-1.5">
              <CheckCircle2 class="w-4 h-4 text-emerald-300" />
              <span>Status: <strong>Aktif / Terverifikasi</strong></span>
            </span>
            <span>Kode Pemda: <code class="font-mono bg-black/20 px-2 py-0.5 rounded">{{ visiData.kodepemda || '3376' }}</code></span>
          </div>

          <button 
            @click="openEditVisiModal"
            class="px-4 py-2 rounded-xl text-xs font-black bg-white text-[#1a4845] hover:bg-teal-50 shadow-md shadow-black/10 transition-all flex items-center space-x-1.5 cursor-pointer"
          >
            <Edit3 class="w-3.5 h-3.5" />
            <span>Edit Visi RPJMD</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 2. POKOK-POKOK PENJABARAN VISI KOTA IDAMAN -->
    <div class="space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center space-x-2">
            <span>Fokus Penjabaran Visi RPJMD</span>
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-[#308e87]/10 text-[#308e87] border border-[#308e87]/20">
              4 Pilar Utama
            </span>
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Penjabaran arah pembangunan jangka menengah Kota Tegal berdasarkan visi kepala daerah terpilih.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div 
          v-for="(item, idx) in pokokVisiList" 
          :key="idx"
          class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-5 shadow-sm hover:border-[#308e87]/40 transition-colors"
        >
          <div class="flex items-center space-x-3 mb-2.5">
            <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-[#308e87] to-[#245f5a] text-white font-black text-xs flex items-center justify-center shadow-sm">
              {{ idx + 1 }}
            </div>
            <h4 class="text-sm font-black text-slate-900 dark:text-white">{{ item.kataKunci }}</h4>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{{ item.penjelasan }}</p>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: EDIT VISI RPJMD ==================== -->
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
              <h3 class="text-base font-black text-slate-900 dark:text-white">Edit Visi RPJMD</h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjmd_visi</code></p>
            </div>
          </div>
          <button @click="showVisiModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveVisiData" class="space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Visi RPJMD</label>
            <textarea 
              v-model="visiForm.uraivisi" 
              rows="3" 
              required
              placeholder="Masukkan uraian visi RPJMD..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-semibold leading-relaxed"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Periode RPJMD</label>
              <input 
                v-model="visiForm.idperiode" 
                type="text" 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Tahun Pagu</label>
              <input 
                v-model="visiForm.tahunpagu" 
                type="text" 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
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

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { Compass, Sparkles, CheckCircle2, Edit3, Loader2 } from 'lucide-vue-next'

const loadingVisi = ref(false)
const savingVisi = ref(false)

const visiData = ref({
  id: '',
  idperiode: '2025 - 2029',
  tahunpagu: '2026 - 2030',
  status: 1,
  uraivisi: 'Tegal Berdikari Dan Sejahtera, Menjadi Kota Idaman',
  kodepemda: '3376',
  no: 1
})

const pokokVisiList = ref([
  {
    kataKunci: 'Berdikari',
    penjelasan: 'Kemandirian ekonomi daerah bertumpu pada keunggulan maritim, UMKM tangguh, inovasi perikanan, serta optimalisasi PAD berbasis digital.'
  },
  {
    kataKunci: 'Sejahtera',
    penjelasan: 'Peningkatan kualitas hidup warga melalui jaminan layanan pendidikan inklusif, faskes paripurna, penurunan kemiskinan ekstrem, dan jaring pengaman sosial.'
  },
  {
    kataKunci: 'Kota Idaman',
    penjelasan: 'Mewujudkan Kota Tegal yang Indah, Damai, Aman, Maju, Agamis, dan Nyaman untuk seluruh lapisan masyarakat dan wisatawan.'
  },
  {
    kataKunci: 'Berkelanjutan',
    penjelasan: 'Pembangunan infrastruktur perkotaan yang tangguh bencana banjir rob, ramah lingkungan, dan mendukung ekonomi sirkular hijau.'
  }
])

const showVisiModal = ref(false)
const visiForm = ref({ id: '', uraivisi: '', idperiode: '', tahunpagu: '' })

async function fetchRpjmdVisiData() {
  loadingVisi.value = true
  try {
    const res = await axios.get('/api/v1/rpjmd/visi')
    if (res.data) {
      visiData.value = res.data
    }
  } catch (err) {
    console.error('Error fetching RPJMD Visi data:', err)
  } finally {
    loadingVisi.value = false
  }
}

function openEditVisiModal() {
  visiForm.value = {
    id: visiData.value.id,
    uraivisi: visiData.value.uraivisi,
    idperiode: visiData.value.idperiode,
    tahunpagu: visiData.value.tahunpagu
  }
  showVisiModal.value = true
}

async function saveVisiData() {
  savingVisi.value = true
  try {
    await axios.put(`/api/v1/rpjmd/visi/${visiForm.value.id}`, {
      uraivisi: visiForm.value.uraivisi,
      idperiode: visiForm.value.idperiode,
      tahunpagu: visiForm.value.tahunpagu
    })
    showVisiModal.value = false
    await fetchRpjmdVisiData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: 'Visi RPJMD berhasil diperbarui',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan perubahan visi RPJMD', 'error')
  } finally {
    savingVisi.value = false
  }
}

onMounted(() => {
  fetchRpjmdVisiData()
})

defineExpose({
  fetchRpjmdVisiData,
  visiData
})
</script>
