<template>
  <div class="space-y-6 pb-12">

    <!-- Header Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] dark:from-[#0f1729] dark:via-[#162032] dark:to-[#1a2940] p-6 text-white shadow-lg">
      <div class="absolute inset-0 opacity-[0.05]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;40&quot; height=&quot;40&quot; viewBox=&quot;0 0 40 40&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot; fill-rule=&quot;evenodd&quot;%3E%3Cpath d=&quot;M0 40L40 0H20L0 20M40 40V20L20 40&quot;/%3E%3C/g%3E%3C/svg%3E')"></div>
      <div class="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2 mb-2">
            <span class="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest bg-[#3aada4] text-white shadow-sm shadow-[#3aada4]/30">
              Pusat Laporan
            </span>
            <span class="text-xs text-white/60 font-semibold">SIMLABA Kota Tegal</span>
          </div>
          <h1 class="text-2xl font-black tracking-tight text-white">Laporan & Rekapitulasi Pembangunan</h1>
          <p class="text-xs text-[#3aada4] mt-1 font-semibold">Pilih jenis laporan RKO, RFK, atau Rekapitulasi untuk ekspor dokumen (Web, PDF, Excel, Word)</p>
        </div>
      </div>
    </div>

    <!-- 2 Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- KOLOM KIRI: TREEVIEW JENIS LAPORAN (4 Cols) -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div class="lg:col-span-4 space-y-4">
        <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm p-4">
          
          <div class="flex items-center justify-between pb-3 mb-3 border-b-2 border-slate-100 dark:border-slate-800">
            <div class="flex items-center space-x-2">
              <FileText class="w-5 h-5 text-[#308e87] dark:text-[#3aada4]" />
              <h2 class="font-black text-sm text-slate-900 dark:text-white">Jenis Laporan</h2>
            </div>
            <span class="text-[10px] font-bold text-slate-400">Treeview</span>
          </div>

          <!-- Treeview Container -->
          <div class="space-y-2 text-xs">
            
            <!-- CATEGORY 1: RKO -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden">
              <button 
                @click="toggleCategory('rko')"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/60 flex items-center justify-between font-black text-slate-800 dark:text-slate-200 hover:bg-[#308e87]/5 transition-colors cursor-pointer"
              >
                <div class="flex items-center space-x-2">
                  <ChevronRight 
                    class="w-4 h-4 text-[#308e87] transition-transform duration-200" 
                    :class="expandedCategories.rko ? 'rotate-90' : ''" 
                  />
                  <Folder class="w-4 h-4 text-[#308e87]" />
                  <span>Rencana Kerja Operasional (RKO)</span>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[9px] font-black bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4]">7</span>
              </button>

              <div v-show="expandedCategories.rko" class="bg-white dark:bg-[#141d30] divide-y divide-slate-100 dark:divide-slate-800/40">
                <button 
                  v-for="item in rkoItems" 
                  :key="item.id"
                  @click="selectReport(item)"
                  class="w-full pl-9 pr-3 py-2 text-left font-semibold text-[11px] flex items-center justify-between transition-all cursor-pointer group"
                  :class="selectedReport?.id === item.id 
                    ? 'bg-[#308e87] text-white font-bold' 
                    : 'text-slate-700 dark:text-slate-300 hover:bg-[#308e87]/8 dark:hover:bg-slate-800/50 hover:text-[#308e87]'"
                >
                  <span class="truncate">{{ item.label }}</span>
                  <ChevronRight class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity shrink-0 ml-1" />
                </button>
              </div>
            </div>

            <!-- CATEGORY 2: RFK -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden">
              <button 
                @click="toggleCategory('rfk')"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/60 flex items-center justify-between font-black text-slate-800 dark:text-slate-200 hover:bg-[#308e87]/5 transition-colors cursor-pointer"
              >
                <div class="flex items-center space-x-2">
                  <ChevronRight 
                    class="w-4 h-4 text-[#f39159] transition-transform duration-200" 
                    :class="expandedCategories.rfk ? 'rotate-90' : ''" 
                  />
                  <Folder class="w-4 h-4 text-[#f39159]" />
                  <span>Realisasi Fisik & Keuangan (RFK)</span>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[9px] font-black bg-[#f39159]/10 text-[#f39159] dark:text-[#f8b088]">6</span>
              </button>

              <div v-show="expandedCategories.rfk" class="bg-white dark:bg-[#141d30] divide-y divide-slate-100 dark:divide-slate-800/40">
                <button 
                  v-for="item in rfkItems" 
                  :key="item.id"
                  @click="selectReport(item)"
                  class="w-full pl-9 pr-3 py-2 text-left font-semibold text-[11px] flex items-center justify-between transition-all cursor-pointer group"
                  :class="selectedReport?.id === item.id 
                    ? 'bg-[#f39159] text-white font-bold' 
                    : 'text-slate-700 dark:text-slate-300 hover:bg-[#f39159]/8 dark:hover:bg-slate-800/50 hover:text-[#f39159]'"
                >
                  <span class="truncate">{{ item.label }}</span>
                  <ChevronRight class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity shrink-0 ml-1" />
                </button>
              </div>
            </div>

            <!-- CATEGORY 3: REKAPITULASI -->
            <div class="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden">
              <button 
                @click="toggleCategory('rekap')"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/60 flex items-center justify-between font-black text-slate-800 dark:text-slate-200 hover:bg-blue-500/5 transition-colors cursor-pointer"
              >
                <div class="flex items-center space-x-2">
                  <ChevronRight 
                    class="w-4 h-4 text-blue-500 transition-transform duration-200" 
                    :class="expandedCategories.rekap ? 'rotate-90' : ''" 
                  />
                  <Folder class="w-4 h-4 text-blue-500" />
                  <span>Rekapitulasi Laporan</span>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[9px] font-black bg-blue-500/10 text-blue-600 dark:text-blue-400">5</span>
              </button>

              <div v-show="expandedCategories.rekap" class="bg-white dark:bg-[#141d30] divide-y divide-slate-100 dark:divide-slate-800/40">
                <button 
                  v-for="item in rekapItems" 
                  :key="item.id"
                  @click="selectReport(item)"
                  class="w-full pl-9 pr-3 py-2 text-left font-semibold text-[11px] flex items-center justify-between transition-all cursor-pointer group"
                  :class="selectedReport?.id === item.id 
                    ? 'bg-blue-600 text-white font-bold' 
                    : 'text-slate-700 dark:text-slate-300 hover:bg-blue-500/8 dark:hover:bg-slate-800/50 hover:text-blue-600'"
                >
                  <span class="truncate">{{ item.label }}</span>
                  <ChevronRight class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity shrink-0 ml-1" />
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════ -->
      <!-- KOLOM KANAN: FORM PARAMETER FILTER (8 Cols) -->
      <!-- ═══════════════════════════════════════════════════════════ -->
      <div class="lg:col-span-8 space-y-5">
        <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm p-6 space-y-6">
          
          <!-- Selected Report Header -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <span class="text-[10px] font-black uppercase tracking-wider text-[#308e87] dark:text-[#3aada4] block">
                Kategori: {{ selectedReport?.categoryName }}
              </span>
              <h3 class="text-base font-black text-slate-900 dark:text-white mt-0.5">
                {{ selectedReport?.label }}
              </h3>
            </div>
            <span class="self-start sm:self-auto px-3 py-1 rounded-lg text-xs font-black bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20">
              ID: {{ selectedReport?.id }}
            </span>
          </div>

          <!-- Parameter Filter Form -->
          <form ref="myFormLaporan" @submit.prevent="generateReport" method="post" target="_blank" class="space-y-5 text-xs">
            
            <!-- Input Text / Hidden for Form Submit payload -->
            <input type="hidden" name="report_name" :value="selectedReport?.id || ''" />
            <input type="hidden" name="pid_sub_pd" :value="filter.id_sub_pd !== null ? filter.id_sub_pd : ''" />
            <input type="hidden" name="puser" value="admin"/>

            <!-- 1. Combobox OPD (Searchable) -->
            <div id="opd-combobox-wrapper" class="relative">
              <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">
                Perangkat Daerah (OPD) <span class="text-red-400">*</span>
              </label>

              <!-- Trigger Box -->
              <div 
                @click="toggleOpdDropdown"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-bold flex items-center justify-between cursor-pointer hover:border-[#308e87] transition-colors"
                :class="{ 'border-[#308e87] ring-2 ring-[#308e87]/20': isOpdDropdownOpen }"
              >
                <div class="flex items-center space-x-2.5 min-w-0">
                  <Building2 class="w-4 h-4 text-[#308e87] shrink-0" />
                  <span class="truncate text-xs font-black">{{ selectedOpdLabel }}</span>
                </div>

                <div class="flex items-center space-x-1 shrink-0 ml-2">
                  <button 
                    v-if="filter.id_sub_pd !== null" 
                    type="button" 
                    @click.stop="clearOpdSelection" 
                    class="p-0.5 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-400 hover:text-slate-600 transition-colors"
                    title="Reset pilihan OPD"
                  >
                    <X class="w-3.5 h-3.5" />
                  </button>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200" :class="{ 'rotate-180': isOpdDropdownOpen }" />
                </div>
              </div>

              <!-- Dropdown Menu -->
              <div 
                v-if="isOpdDropdownOpen" 
                class="absolute left-0 right-0 top-full mt-1.5 bg-white dark:bg-[#18243b] border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl z-50 overflow-hidden space-y-2 p-2.5 animate-in fade-in duration-150"
              >
                <!-- Search Input Header -->
                <div class="relative">
                  <Search class="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input 
                    type="text" 
                    v-model="opdSearchQuery" 
                    placeholder="Ketik nama atau kode OPD untuk mencari..."
                    ref="opdSearchInput"
                    @click.stop
                    class="w-full pl-9 pr-8 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-bold focus:outline-none focus:ring-2 focus:ring-[#308e87] text-slate-900 dark:text-white"
                  />
                  <button 
                    v-if="opdSearchQuery" 
                    type="button"
                    @click.stop="opdSearchQuery = ''" 
                    class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 cursor-pointer"
                  >
                    <X class="w-3.5 h-3.5" />
                  </button>
                </div>

                <!-- OPD Options List -->
                <div class="max-h-60 overflow-y-auto space-y-1 pr-1 custom-scrollbar">
                  
                  <!-- Option List: Filtered OPDs -->
                  <div 
                    v-for="opd in filteredOpdOptions" 
                    :key="'combobox-opd-' + opd.id_sub_pd"
                    @click="selectOpd(opd.id_sub_pd)"
                    class="px-3 py-2.5 rounded-xl text-xs font-bold cursor-pointer transition-colors flex items-center justify-between"
                    :class="filter.id_sub_pd === opd.id_sub_pd ? 'bg-[#308e87] text-white shadow-sm' : 'hover:bg-slate-100 dark:hover:bg-slate-800/60 text-slate-700 dark:text-slate-200'"
                  >
                    <div class="truncate mr-2 min-w-0">
                      <span class="font-mono text-[10px] opacity-75 mr-1.5">[{{ opd.kode }}]</span>
                      <span>{{ opd.nama_pd }}</span>
                    </div>
                    <CheckCircle2 v-if="filter.id_sub_pd === opd.id_sub_pd" class="w-4 h-4 shrink-0" />
                  </div>

                  <!-- Empty Search State -->
                  <div v-if="filteredOpdOptions.length === 0" class="p-4 text-center text-slate-400 text-xs font-bold">
                    Tidak ditemukan OPD dengan kata kunci "{{ opdSearchQuery }}"
                  </div>
                </div>
              </div>
            </div>

            <!-- 2. Grid Tahun & Bulan -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <!-- Tahun -->
              <div>
                <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">
                  Tahun Anggaran <span class="text-red-400">*</span>
                </label>
                <select 
                  name="ptahun"
                  v-model="filter.tahun"
                  required
                  class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-bold focus:outline-none focus:border-[#308e87]"
                >
                  <option v-for="yr in yearOptions" :key="yr" :value="yr">T.A. {{ yr }}</option>
                </select>
              </div>

              <!-- Bulan -->
              <div>
                <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">
                  Bulan Laporan
                </label>
                <select 
                  name="pbulan"
                  v-model="filter.bulan"
                  class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-bold focus:outline-none focus:border-[#308e87]"
                >
                  <option v-for="(mName, mIdx) in monthOptions" :key="mIdx" :value="mIdx + 1">
                    Bulan {{ mIdx + 1 }} - {{ mName }}
                  </option>
                </select>
              </div>
            </div>

            <!-- 3. Footer Text -->
            <div>
              <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">
                Footer Text (Teks Catatan Kaki Dokumen)
              </label>
              <input 
                name="pfooter"
                v-model="filter.footer_text"
                type="text"
                placeholder="Contoh: Kota Tegal, 2026 • Dicetak melalui SIMLABA"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-medium focus:outline-none focus:border-[#308e87]"
              />
            </div>

            <!-- 4. Format Output Selection (Web, PDF, Excel, Word) -->
            <div>
              <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-2 uppercase tracking-wider text-[10px]">
                Format Output Cetak Laporan <span class="text-red-400">*</span>
              </label>
              
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                
                <!-- Web / HTML -->
                <label 
                  class="p-3 rounded-xl border-2 cursor-pointer flex flex-col items-center justify-center transition-all"
                  :class="filter.format === 'html' 
                    ? 'border-[#308e87] bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] shadow-sm' 
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/40'"
                >
                  <input type="radio" name="format" v-model="filter.format" value="html" class="sr-only" />
                  <Globe class="w-5 h-5" />
                  <span class="font-black text-xs">Web</span>
                </label>

                <!-- PDF -->
                <label 
                  class="p-3 rounded-xl border-2 cursor-pointer flex flex-col items-center justify-center transition-all"
                  :class="filter.format === 'pdf' 
                    ? 'border-red-500 bg-red-500/10 text-red-600 dark:text-red-400 shadow-sm' 
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/40'"
                >
                  <input type="radio" name="format" v-model="filter.format" value="pdf" class="sr-only" />
                  <FileText class="w-5 h-5" />
                  <span class="font-black text-xs">PDF Document</span>
                </label>

                <!-- Excel -->
                <label 
                  class="p-3 rounded-xl border-2 cursor-pointer flex flex-col items-center justify-center transition-all"
                  :class="filter.format === 'xls' 
                    ? 'border-emerald-500 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 shadow-sm' 
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/40'"
                >
                  <input type="radio" name="format" v-model="filter.format" value="xls" class="sr-only" />
                  <FileSpreadsheet class="w-5 h-5" />
                  <span class="font-black text-xs">Excel (.xlsx)</span>
                </label>

                <!-- Word -->
                <label 
                  class="p-3 rounded-xl border-2 cursor-pointer flex flex-col items-center justify-center transition-all"
                  :class="filter.format === 'docx' 
                    ? 'border-blue-500 bg-blue-500/10 text-blue-600 dark:text-blue-400 shadow-sm' 
                    : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/40'"
                >
                  <input type="radio" name="format" v-model="filter.format" value="docx" class="sr-only" />
                  <FileCode class="w-5 h-5" />
                  <span class="font-black text-xs">Word (.docx)</span>
                </label>

              </div>
            </div>

            <!-- Generate Action Buttons -->
            <div class="pt-4 border-t-2 border-slate-100 dark:border-slate-800/50 flex flex-col sm:flex-row items-center justify-end gap-3">
              <button 
                type="button" 
                @click="resetFilter"
                class="w-full sm:w-auto px-4 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold rounded-xl text-xs cursor-pointer"
              >
                Reset Filter
              </button>

              <button 
                type="submit" 
                :disabled="generating"
                class="w-full sm:w-auto px-6 py-2.5 bg-gradient-to-r from-[#308e87] via-[#3aada4] to-[#308e87] text-white text-xs font-black rounded-xl shadow-lg shadow-[#308e87]/25 flex items-center justify-center space-x-2 shrink-0 transition-all hover:shadow-xl hover:shadow-[#308e87]/35 active:scale-[0.98] cursor-pointer disabled:opacity-50"
              >
                <Loader2 v-if="generating" class="w-4 h-4 animate-spin" />
                <Printer v-else-if="filter.format === 'html' || filter.format === 'pdf'" class="w-4 h-4" />
                <Download v-else class="w-4 h-4" />
                <span>{{ getActionButtonText() }}</span>
              </button>
            </div>

          </form>
        </div>

        <!-- Preview Notification Box -->
        <div v-if="generatedResult" class="p-5 rounded-2xl bg-emerald-50 dark:bg-emerald-950/20 border-2 border-emerald-400/30 text-emerald-800 dark:text-emerald-300 space-y-2 animate-fade-up">
          <div class="flex items-center space-x-2 font-black text-sm">
            <CheckCircle class="w-5 h-5 text-emerald-600" />
            <span>Laporan Berhasil Diproses!</span>
          </div>
          <p class="text-xs">
            Laporan <strong>{{ generatedResult.reportLabel }}</strong> untuk <strong>{{ generatedResult.opdName }}</strong> (T.A. {{ generatedResult.tahun }}) telah siap disajikan dalam format <strong>{{ generatedResult.format.toUpperCase() }}</strong>.
          </p>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
import { 
  FileText, 
  Folder, 
  ChevronRight, 
  Globe, 
  FileSpreadsheet, 
  FileCode, 
  Printer, 
  Download, 
  Loader2, 
  CheckCircle,
  Building2,
  Search,
  ChevronDown,
  CheckCircle2,
  X
} from 'lucide-vue-next'

const authStore = useAuthStore()

// Treeview Expand States
const expandedCategories = ref({
  rko: true,
  rfk: true,
  rekap: true
})

const toggleCategory = (cat) => {
  expandedCategories.value[cat] = !expandedCategories.value[cat]
}

// Treeview Items Definition
const rkoItems = [
  { id: 'rko_semua', category: 'rko', categoryName: 'RKO', label: 'RKO (Semua)' },
  { id: 'rko_1', category: 'rko', categoryName: 'RKO', label: 'RKO Bagian I-III (Visi Misi, Alokasi Anggaran, Struktur Organisasi)' },
  { id: 'rko_4', category: 'rko', categoryName: 'RKO', label: 'RKO Bagian IV (Tabel Program dan Kegiatan yang dilaksanakan)' },
  { id: 'rko_5', category: 'rko', categoryName: 'RKO', label: 'RKO Bagian V (Paket Pekerjaan dan Jadwal Pelaksanaan)' },
  { id: 'rko_6', category: 'rko', categoryName: 'RKO', label: 'RKO Bagian VI (Rencana Pengeluaran Anggaran)' },
  { id: 'rko_7', category: 'rko', categoryName: 'RKO', label: 'RKO Bagian VII (Target Fisik Kegiatan yang dilaksanakan)' },
  { id: 'rko_8', category: 'rko', categoryName: 'RKO', label: 'RKO Bagian VIII (Penutup)' }
]

const rfkItems = [
  { id: 'rfk_1', category: 'rfk', categoryName: 'RFK', label: 'RFK 1' },
  { id: 'rfk_2', category: 'rfk', categoryName: 'RFK', label: 'RFK 2' },
  { id: 'rfk_3', category: 'rfk', categoryName: 'RFK', label: 'RFK 3' },
  { id: 'pro_sn', category: 'rfk', categoryName: 'RFK', label: 'ProSN' },
  { id: 'progres_pokir', category: 'rfk', categoryName: 'RFK', label: 'Progres Kegiatan Pokir' },
  { id: 'progres_musrenbang', category: 'rfk', categoryName: 'RFK', label: 'Progres Kegiatan Musrenbang' }
]

const rekapItems = [
  { id: 'rekap_bulanan', category: 'rekap', categoryName: 'Rekapitulasi', label: 'Rekap Bulanan' },
  { id: 'rekap_pengiriman', category: 'rekap', categoryName: 'Rekapitulasi', label: 'Rekap Pengiriman Laporan' },
  { id: 'peringkat_realisasi', category: 'rekap', categoryName: 'Rekapitulasi', label: 'Peringkat Realisasi' },
  { id: 'laporan_deviasi', category: 'rekap', categoryName: 'Rekapitulasi', label: 'Laporan Deviasi' },
  { id: 'rekap_anggaran_bidang', category: 'rekap', categoryName: 'Rekapitulasi', label: 'Rekapitulasi Anggaran Berdasarkan Bidang' }
]

// Currently selected report
const selectedReport = ref(rkoItems[0])

const selectReport = (item) => {
  selectedReport.value = item
  generatedResult.value = null
}

const getCurrentMonthNumber = () => {
  return new Date().getMonth() + 1
}

const getTodayFormattedDate = () => {
  const today = new Date()
  const months = [
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
  ]
  const day = today.getDate()
  const month = months[today.getMonth()]
  const year = today.getFullYear()
  return `Tegal, ${day} ${month} ${year}`
}

// Filter Form Model
const filter = ref({
  id_sub_pd: null,
  tahun: 2026,
  bulan: getCurrentMonthNumber(),
  footer_text: getTodayFormattedDate(),
  format: 'html'
})

const yearOptions = [2026, 2025, 2024, 2023]
const monthOptions = [
  'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
  'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]

const opdOptions = ref([])
const generating = ref(false)
const generatedResult = ref(null)

const fetchOpdList = async () => {
  try {
    const res = await axios.get('/api/v1/personel/opd')
    const opdData = res.data
    opdOptions.value = opdData

    // Auto-select first allowed OPD for role_id > 5 users
    const user = authStore.user
    if (user && user.role_id > 5 && opdData.length > 0) {
      filter.value.id_sub_pd = opdData[0].id_sub_pd
    }
  } catch (err) {
    console.warn('Gagal memuat OPD options:', err)
  }
}

const getActionButtonText = () => {
  switch (filter.value.format) {
    case 'html': return 'Tampilkan Laporan (Web)'
    case 'pdf': return 'Cetak Dokumen PDF'
    case 'xls': return 'Unduh File Excel'
    case 'docx': return 'Unduh File Word'
    default: return 'Tampilkan'
  }
}

const isOpdDropdownOpen = ref(false)
const opdSearchQuery = ref('')
const opdSearchInput = ref(null)

const selectedOpdLabel = computed(() => {
  if (filter.value.id_sub_pd === null) {
    return '[0.00.0.00.000] Kota Tegal'
  }
  const found = opdOptions.value.find(o => o.id_sub_pd === filter.value.id_sub_pd)
  return found ? `[${found.kode}] ${found.nama_pd}` : '[0.00.0.00.000] Kota Tegal'
})

const filteredOpdOptions = computed(() => {
  if (!opdSearchQuery.value || !opdSearchQuery.value.trim()) {
    return opdOptions.value
  }
  const q = opdSearchQuery.value.toLowerCase().trim()
  return opdOptions.value.filter(opd => 
    (opd.nama_pd && opd.nama_pd.toLowerCase().includes(q)) ||
    (opd.kode && opd.kode.toLowerCase().includes(q))
  )
})

const selectOpd = (idSubPd) => {
  filter.value.id_sub_pd = idSubPd
  isOpdDropdownOpen.value = false
  opdSearchQuery.value = ''
}

const clearOpdSelection = () => {
  filter.value.id_sub_pd = null
  isOpdDropdownOpen.value = false
  opdSearchQuery.value = ''
}

const toggleOpdDropdown = () => {
  isOpdDropdownOpen.value = !isOpdDropdownOpen.value
  if (isOpdDropdownOpen.value) {
    setTimeout(() => {
      if (opdSearchInput.value) {
        opdSearchInput.value.focus()
      }
    }, 50)
  }
}

const closeOpdDropdownOnClickOutside = (event) => {
  if (isOpdDropdownOpen.value) {
    const wrapper = document.getElementById('opd-combobox-wrapper')
    if (wrapper && !wrapper.contains(event.target)) {
      isOpdDropdownOpen.value = false
    }
  }
}

const resetFilter = () => {
  filter.value = {
    id_sub_pd: null,
    tahun: 2026,
    bulan: getCurrentMonthNumber(),
    footer_text: getTodayFormattedDate(),
    format: 'html'
  }
  generatedResult.value = null
  isOpdDropdownOpen.value = false
  opdSearchQuery.value = ''
}

const myFormLaporan = ref(null)


const generateReport = (event) => {

  if (!selectedReport.value) return
  
  generating.value = false

  const reportId = selectedReport.value.id
  const backendUrl = import.meta.env.VITE_API_BASE_URL || ''

  myFormLaporan.value.action = `${backendUrl}/laporan/${reportId}`
  myFormLaporan.value.submit() 

  /*
  if (!selectedReport.value) return
  generating.value = true
  
  const reportId = selectedReport.value.id
  const opdObj = opdOptions.value.find(o => o.id_sub_pd === filter.value.id_sub_pd)
  const opdName = opdObj ? opdObj.nama_pd : 'Semua Perangkat Daerah (Kota Tegal)'

   

  generatedResult.value = {
    reportLabel: selectedReport.value.label,
    opdName,
    tahun: filter.value.tahun,
    format: filter.value.format
  }

  const query = {}
  if (filter.value.id_sub_pd !== null && filter.value.id_sub_pd !== undefined) {
    query.id_sub_pd = filter.value.id_sub_pd
  }
  if (filter.value.tahun) query.tahun = filter.value.tahun
  if (filter.value.bulan !== undefined && filter.value.bulan !== null) {
    query.bulan = filter.value.bulan
  }
  if (filter.value.footer_text) query.footer_text = filter.value.footer_text
  if (filter.value.format) query.format = filter.value.format

  const routeData = router.resolve({
    path: `/report/${reportId}`,
    query
  })

  setTimeout(() => {
    generating.value = false
    window.open(routeData.href, '_blank')
  }, 300)
  */
}

onMounted(() => {
  fetchOpdList()
  window.addEventListener('click', closeOpdDropdownOnClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('click', closeOpdDropdownOnClickOutside)
})
</script>
