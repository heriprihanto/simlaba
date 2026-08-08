<template>
  <div class="space-y-6 pb-12" @click="closeMenu">
    
    <!-- Executive Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] dark:from-[#0f1729] dark:via-[#162032] dark:to-[#1a2940] p-6 sm:p-7 text-white shadow-lg transition-colors duration-300">
      <div class="absolute inset-0 opacity-[0.05]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;40&quot; height=&quot;40&quot; viewBox=&quot;0 0 40 40&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot; fill-rule=&quot;evenodd&quot;%3E%3Cpath d=&quot;M0 40L40 0H20L0 20M40 40V20L20 40&quot;/%3E%3C/g%3E%3C/svg%3E')"></div>
      <div class="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          
          <h1 class="text-2xl font-black tracking-tight text-white">
            {{ viewMode === 'list' ? 'Rencana Kerja Operasional (RKO)' : selectedOpdDetail?.opd?.nama_pd }}
          </h1>
          <p class="text-xs text-[#3aada4] mt-1 font-semibold">
            {{ viewMode === 'list' ? `Daftar Perangkat Daerah, alokasi anggaran, subkegiatan, dan paket pekerjaan T.A. ${selectedTahun}` : `T.A. ${selectedTahun}` }}
          </p>
        </div>

        <!-- Right Controls (Back Button / Year Selector) -->
        <div class="flex items-center space-x-2">
          <button 
            v-if="viewMode === 'detail'"
            @click="backToList"
            class="px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur text-white text-xs font-bold rounded-xl border border-white/20 flex items-center space-x-1.5 transition-all cursor-pointer"
          >
            <ArrowLeft class="w-4 h-4" />
            <span>Kembali ke Daftar OPD</span>
          </button>

          <div class="flex items-center space-x-2" style="display: none;">
            <label class="text-xs text-white/70 font-bold shrink-0">Tahun:</label>
            <select 
              v-model="selectedTahun"
              @change="onTahunChange"
              class="px-3.5 py-2 bg-white/10 hover:bg-white/20 backdrop-blur text-white text-xs font-black rounded-xl border border-white/20 focus:outline-none focus:ring-2 focus:ring-[#3aada4] cursor-pointer"
            >
              <option v-for="yr in [2026, 2025, 2024, 2023]" :key="yr" :value="yr" class="text-slate-900">
                T.A. {{ yr }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- LEVEL 1: RKO OPD LIST TABLE -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="viewMode === 'list'" class="space-y-4">
      
      <!-- Search Controls -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="relative w-full sm:w-96">
          <Search class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-[11px]" />
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Cari Kode atau Nama Perangkat Daerah..."
            class="w-full pl-10 pr-9 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-[#308e87] transition-all shadow-sm" 
          />
          <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-3 top-[11px] text-slate-400 hover:text-[#308e87]">
            <X class="w-4 h-4" />
          </button>
        </div>

        <span class="text-xs font-bold text-slate-500 dark:text-slate-400">
          Menampilkan <strong class="text-[#308e87] dark:text-[#3aada4]">{{ filteredOpdList.length }}</strong> dari {{ opdList.length }} OPD
        </span>
      </div>

      <!-- OPD List Table -->
      <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-4 w-12 text-center">No</th>
                <th class="py-3.5 px-4 w-48">Kode OPD</th>
                <th class="py-3.5 px-4">Nama Perangkat Daerah</th>
                <th class="py-3.5 px-4 text-right">Total Anggaran</th>
                <th class="py-3.5 px-4 text-center">Jumlah Subkegiatan</th>
                <th class="py-3.5 px-4 text-center">Jumlah Pekerjaan</th>
                <th class="py-3.5 px-4 text-center">Status RKO</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/40">
              <tr v-if="loading">
                <td colspan="8" class="py-20 text-center">
                  <Loader2 class="w-7 h-7 animate-spin mx-auto mb-2 text-[#308e87]" />
                  <span class="font-bold text-xs text-slate-400">Memuat data RKO Perangkat Daerah...</span>
                </td>
              </tr>

              <tr v-else-if="filteredOpdList.length === 0">
                <td colspan="8" class="py-20 text-center">
                  <FileX class="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p class="font-bold text-xs text-slate-500 dark:text-slate-400">Tidak ada data RKO OPD ditemukan</p>
                </td>
              </tr>

              <tr 
                v-for="(item, idx) in filteredOpdList" 
                :key="item.id_sub_pd"
                @click="openOpdDetail(item)"
                class="even:bg-[#308e87]/[0.02] dark:even:bg-[#308e87]/[0.04] hover:bg-[#308e87]/[0.06] dark:hover:bg-[#308e87]/[0.08] transition-colors cursor-pointer group"
              >
                <!-- No -->
                <td class="py-3.5 px-4 text-center font-black text-slate-400 dark:text-slate-500 border-b border-slate-100 dark:border-slate-800/40">
                  {{ idx + 1 }}
                </td>

                <!-- Kode OPD -->
                <td class="py-3.5 px-4 font-mono font-bold text-[#308e87] dark:text-[#3aada4] text-[11px] border-b border-slate-100 dark:border-slate-800/40">
                  <span class="px-2 py-0.5 rounded-md bg-[#308e87]/10 dark:bg-[#308e87]/15 border border-[#308e87]/20">
                    {{ item.kode || '-' }}
                  </span>
                </td>

                <!-- Nama OPD (Clickable) -->
                <td class="py-3.5 px-4 font-bold text-slate-800 dark:text-slate-200 group-hover:text-[#308e87] dark:group-hover:text-[#3aada4] transition-colors border-b border-slate-100 dark:border-slate-800/40">
                  <div class="hover:underline cursor-pointer flex items-center space-x-1.5">
                    <Building2 class="w-4 h-4 text-[#308e87] shrink-0" />
                    <span>{{ item.nama_pd }}</span>
                  </div>
                </td>

                <!-- Total Anggaran (Merah jika Terdapat Perbedaan Pagu Renja vs Pekerjaan) -->
                <td class="py-3.5 px-4 text-right font-black border-b border-slate-100 dark:border-slate-800/40">
                  <div v-if="item.is_pagu_mismatch" class="flex flex-col items-end">
                    <div class="flex items-center space-x-1 text-red-600 dark:text-red-400 font-black text-xs">
                      <AlertTriangle class="w-3.5 h-3.5 shrink-0 text-red-600 dark:text-red-400" />
                      <span>{{ formatRupiah(item.total_anggaran_pekerjaan) }}</span>
                    </div>
                    <span class="text-[10px] font-bold text-red-500/90 dark:text-red-400/90 block leading-tight">
                      DPA: {{ formatRupiah(item.total_anggaran_renja) }}
                    </span>
                  </div>
                  <div v-else class="text-slate-900 dark:text-white font-black">
                    {{ formatRupiah(item.total_anggaran_pekerjaan) }}
                  </div>
                </td>

                <!-- Jumlah Subkegiatan -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40">
                  <span 
                    class="inline-flex items-center px-3 py-1 rounded-full text-[11px] font-black"
                    :class="item.jumlah_subkegiatan > 0 ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'"
                  >
                    <Layers class="w-3.5 h-3.5 mr-1" />
                    {{ item.jumlah_subkegiatan }} Subkegiatan
                  </span>
                </td>

                <!-- Jumlah Pekerjaan -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40">
                  <span 
                    class="inline-flex items-center px-3 py-1 rounded-full text-[11px] font-black"
                    :class="item.jumlah_pekerjaan > 0 ? 'bg-[#f39159]/10 text-[#f39159] dark:text-[#f8b088] border border-[#f39159]/20' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'"
                  >
                    <Briefcase class="w-3.5 h-3.5 mr-1" />
                    {{ item.jumlah_pekerjaan }} Paket
                  </span>
                </td>

                <!-- Status RKO -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40">
                  <span 
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider"
                    :class="{
                      'bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30': item.status_rko === 'DRAFT' || !item.status_rko,
                      'bg-blue-500/15 text-blue-700 dark:text-blue-300 border border-blue-500/30': item.status_rko === 'SUBMITTED',
                      'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30': item.status_rko === 'APPROVED',
                      'bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30': item.status_rko === 'REJECTED'
                    }"
                  >
                    <CheckCircle2 v-if="item.status_rko === 'APPROVED'" class="w-3 h-3 mr-1 text-emerald-600 shrink-0" />
                    <Send v-else-if="item.status_rko === 'SUBMITTED'" class="w-3 h-3 mr-1 text-blue-600 shrink-0" />
                    <span>
                      {{ 
                        item.status_rko === 'APPROVED' ? 'DISETUJUI ADMIN' :
                        item.status_rko === 'SUBMITTED' ? 'DISUBMIT OPD' :
                        item.status_rko === 'REJECTED' ? 'REVISI' : 'DRAFT'
                      }}
                    </span>
                  </span>
                </td>

                
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- LEVEL 2: RKO OPD DETAIL (TREEVIEW TABEL CASCADING GRID) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-else-if="viewMode === 'detail'" class="space-y-5">
      
      <!-- OPD Header & Summary Badges -->
      <div class="p-5 rounded-2xl bg-white dark:bg-[#141d30] border-2 border-slate-100 dark:border-slate-800/50 shadow-sm space-y-4">
        
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-4 border-b border-slate-100 dark:border-slate-800/50">
          <div>
            <span class="text-[10px] font-black text-[#308e87] dark:text-[#3aada4] uppercase tracking-wider block">
              Kode OPD: {{ selectedOpdDetail?.opd?.kode }}
            </span>
            <h2 class="text-lg font-black text-slate-900 dark:text-white mt-0.5">
              {{ selectedOpdDetail?.opd?.nama_pd }}
            </h2>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <!-- Status Badge: SUBMITTED (Blue) -->
            <span 
              v-if="selectedOpdDetail?.status_rko === 'SUBMITTED'"
              class="px-3 py-1.5 rounded-xl bg-blue-500/15 text-blue-700 dark:text-blue-300 border border-blue-500/30 font-black text-xs flex items-center space-x-1"
            >
              <Send class="w-3.5 h-3.5 text-blue-600 shrink-0" />
              <span>Disubmit OPD ({{ selectedOpdDetail?.submitted_by || 'OPD' }})</span>
            </span>

            <!-- Status Badge: APPROVED (Emerald) -->
            <span 
              v-else-if="selectedOpdDetail?.status_rko === 'APPROVED'"
              class="px-3 py-1.5 rounded-xl bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 font-black text-xs flex items-center space-x-1"
            >
              <CheckCircle2 class="w-4 h-4 text-emerald-600 shrink-0" />
              <span>Disetujui Admin ({{ selectedOpdDetail?.approved_by || 'Bappeda' }})</span>
            </span>

            <!-- Status Badge: DRAFT / REJECTED (Amber) -->
            <span 
              v-else
              class="px-3 py-1.5 rounded-xl bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30 font-black text-xs flex items-center space-x-1"
            >
              <span>Status: DRAFT</span>
            </span>

            <!-- Submit RKO Button (OPD Users when DRAFT) -->
            <button 
              v-if="selectedOpdDetail?.status_rko === 'DRAFT' || !selectedOpdDetail?.status_rko"
              @click="openSubmitModal"
              class="px-4 py-1.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-black text-xs flex items-center space-x-1.5 shadow-md shadow-emerald-600/30 active:scale-95 transition-all cursor-pointer"
            >
              <Send class="w-3.5 h-3.5" />
              <span>Submit RKO</span>
            </button>

            <!-- Admin Approve Button -->
            <button 
              v-if="isAdmin && selectedOpdDetail?.status_rko === 'SUBMITTED'"
              @click="doApproveRko"
              :disabled="actionLoading"
              class="px-4 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs flex items-center space-x-1.5 shadow-md shadow-emerald-600/30 active:scale-95 transition-all cursor-pointer"
            >
              <CheckCircle2 class="w-3.5 h-3.5" />
              <span>Approve RKO</span>
            </button>

            <!-- Admin Unlock / Reject Button -->
            <button 
              v-if="isAdmin && (selectedOpdDetail?.status_rko === 'SUBMITTED' || selectedOpdDetail?.status_rko === 'APPROVED')"
              @click="doRejectRko"
              :disabled="actionLoading"
              class="px-3.5 py-1.5 rounded-xl bg-rose-500/10 text-rose-700 dark:text-rose-300 border border-rose-500/30 hover:bg-rose-500/20 font-bold text-xs flex items-center space-x-1 cursor-pointer transition-colors"
            >
              <Lock class="w-3.5 h-3.5 text-rose-600" />
              <span>Buka Kunci / Revisi</span>
            </button>

            <button 
              @click="toggleAll(true)"
              class="px-3 py-1.5 rounded-xl bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20 hover:bg-[#308e87]/20 font-bold text-xs cursor-pointer transition-colors"
            >
              + 
            </button>
            <button 
              @click="toggleAll(false)"
              class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-xs cursor-pointer transition-colors"
            >
              - 
            </button>
          </div>
        </div>

        <!-- OPD Locked Alert Banner -->
        <div 
          v-if="selectedOpdDetail?.is_locked || (['SUBMITTED', 'APPROVED'].includes(selectedOpdDetail?.status_rko) && !isAdmin)"
          class="p-3.5 rounded-2xl bg-amber-500/10 border-2 border-amber-500/30 text-amber-900 dark:text-amber-100 text-xs font-extrabold flex items-center space-x-3 shadow-xs"
        >
          <Lock class="w-5 h-5 text-amber-600 shrink-0 animate-pulse" />
          <div>
            <span class="font-black text-amber-800 dark:text-amber-200">🔒 Data RKO Terkunci (Telah Disubmit / Disetujui Admin)</span>
            <p class="font-semibold text-[11px] text-amber-700 dark:text-amber-300 mt-0.5 leading-snug">
              Data RKO OPD tidak dapat ditambah, diubah, atau dihapus oleh OPD. Hubungi Admin BAPPEDA jika membutuhkan pembukaan kuncian untuk revisi.
            </p>
          </div>
        </div>

        <!-- 4 Summary Badges -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div class="p-3 rounded-xl bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20">
            <span class="text-[10px] font-bold block uppercase tracking-wider">Anggaran Subkegiatan (DPA)</span>
            <span class="font-black text-sm block mt-0.5">{{ formatRupiah(selectedOpdDetail?.total_anggaran_renja) }}</span>
          </div>
          <div class="p-3 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
            <span class="text-[10px] font-bold block uppercase tracking-wider">Anggaran Pekerjaan</span>
            <span class="font-black text-sm block mt-0.5">{{ formatRupiah(selectedOpdDetail?.total_anggaran_pekerjaan) }}</span>
          </div>
          <div class="p-3 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            <span class="text-[10px] font-bold block uppercase tracking-wider">Total Subkegiatan</span>
            <span class="font-black text-sm block mt-0.5">{{ selectedOpdDetail?.total_subkegiatan || 0 }} Subkegiatan</span>
          </div>
          <div class="p-3 rounded-xl bg-[#f39159]/10 text-[#f39159] dark:text-[#f8b088] border border-[#f39159]/20">
            <span class="text-[10px] font-bold block uppercase tracking-wider">Total Paket Pekerjaan</span>
            <span class="font-black text-sm block mt-0.5">{{ selectedOpdDetail?.total_pekerjaan || 0 }} Paket</span>
          </div>
        </div>

      </div>

      <!-- Loading State -->
      <div v-if="loadingDetail" class="py-20 text-center bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800">
        <Loader2 class="w-8 h-8 animate-spin mx-auto mb-2 text-[#308e87]" />
        <span class="font-bold text-xs text-slate-400">Memuat Treeview Tabel RKO Perangkat Daerah...</span>
      </div>

      <!-- 27-COLUMN TREEVIEW TABEL CASCADING GRID WITH FRONT AKSI COLUMN -->
      <div v-else-if="selectedOpdDetail?.programs?.length > 0" class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <!-- Group Header Row 1 -->
              <tr class="bg-[#308e87]/10 dark:bg-[#308e87]/20 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b border-[#308e87]/20 text-center">
                <!-- 1. AKSI COLUMN (STICKY LEFT 0) -->
                <th rowspan="2" class="py-3 px-2 border-r border-slate-200 dark:border-slate-800 w-24 text-center min-w-[90px] sticky left-0 bg-[#308e87]/15 dark:bg-[#141d30] z-20" title="Aksi">
                  <Settings class="w-4 h-4 mx-auto text-[#308e87] dark:text-[#3aada4]" />
                </th>
                <!-- 2. KODE & URAIAN CASCADING (STICKY LEFT 90px) -->
                <th rowspan="2" class="py-3 px-4 text-left border-r border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-[90px] bg-[#308e87]/15 dark:bg-[#141d30] z-20">
                  Program > Kegiatan > Subkegiatan > Pekerjaan
                </th>
                <!-- 3. ANGGARAN RENJA -->
                <th rowspan="2" class="py-3 px-3 border-r border-slate-200 dark:border-slate-800 min-w-[130px] text-right">
                  Anggaran DPA
                </th>
                <!-- 4. ANGGARAN PEKERJAAN -->
                <th rowspan="2" class="py-3 px-3 border-r border-slate-200 dark:border-slate-800 min-w-[130px] text-right">
                  Anggaran Pekerjaan
                </th>
                <!-- 5. TARGET FISIK (12 COLS) -->
                <th colspan="12" class="py-2 px-2 border-r border-slate-200 dark:border-slate-800 bg-emerald-500/10 text-emerald-700 dark:text-emerald-400">
                  Target Fisik (%)
                </th>
                <!-- 6. TARGET KEUANGAN (12 COLS) -->
                <th colspan="12" class="py-2 px-2 bg-blue-500/10 text-blue-700 dark:text-blue-400">
                  Target Keuangan (%)
                </th>
              </tr>

              <!-- Month Subheaders Row 2 -->
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-slate-700 dark:text-slate-300 font-black text-[10px] text-center border-b-2 border-[#308e87]/20">
                <!-- Target Fisik Months -->
                <th v-for="m in monthShorts" :key="'tf-' + m" class="py-1.5 px-1 border-r border-slate-150 dark:border-slate-800/60 w-11 bg-emerald-500/5">{{ m }}</th>
                <!-- Target Keuangan Months -->
                <th v-for="m in monthShorts" :key="'tk-' + m" class="py-1.5 px-1 border-r border-slate-150 dark:border-slate-800/60 w-11 bg-blue-500/5">{{ m }}</th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/40">
              
              <!-- LOOP PROGRAM (LEVEL 1) -->
              <template v-for="prog in selectedOpdDetail.programs" :key="'prog-' + prog.kode">
                
                <!-- PROGRAM ROW -->
                <tr 
                  @click="toggleNode('prog-' + prog.kode)"
                  class="bg-slate-50/90 dark:bg-slate-800/70 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer group font-bold text-slate-900 dark:text-white"
                >
                  <!-- Aksi Column (Sticky Left 0) -->
                  <td class="py-3 px-2 text-center border-r border-b border-slate-200 dark:border-slate-800 sticky left-0 bg-slate-50 dark:bg-[#141d30] z-20 text-slate-400 font-normal">
                    -
                  </td>

                  <!-- Uraian Program (Sticky Left 90px) -->
                  <td class="py-3 px-4 border-r border-b border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-[90px] bg-slate-50 dark:bg-[#141d30] z-20">
                    <div class="flex items-center space-x-2 min-w-0 max-w-[330px]">
                      <ChevronRight 
                        class="w-4 h-4 text-[#308e87] transition-transform duration-200 shrink-0" 
                        :class="expandedNodes['prog-' + prog.kode] ? 'rotate-90' : ''" 
                      />
                      <Folder class="w-4 h-4 text-[#308e87] shrink-0" />
                      <span class="px-1.5 py-0.5 rounded font-mono font-black text-[10px] bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20 shrink-0">
                        {{ prog.kode }}
                      </span>
                      <span class="font-black text-xs leading-snug group-hover:text-[#308e87] transition-colors truncate">
                        {{ prog.nama }}
                      </span>
                    </div>
                  </td>

                  <!-- Anggaran Renja -->
                  <td class="py-3 px-3 text-right font-black text-slate-900 dark:text-white border-r border-b border-slate-200 dark:border-slate-800">
                    {{ formatRupiah(prog.anggaran_renja) }}
                  </td>

                  <!-- Anggaran Pekerjaan -->
                  <td class="py-3 px-3 text-right font-black text-[#308e87] dark:text-[#3aada4] border-r border-b border-slate-200 dark:border-slate-800">
                    {{ formatRupiah(prog.anggaran_pekerjaan) }}
                  </td>

                  <!-- Target Fisik Months (12 Cols) -->
                  <td v-for="(v, mIdx) in prog.target_fisik" :key="'prog-tf-' + mIdx" class="py-2 px-1 text-center font-bold text-[10px] border-r border-slate-150 dark:border-slate-800/50 bg-emerald-500/[0.03]">
                    {{ formatPercent(v) }}
                  </td>

                  <!-- Target Keuangan Months (12 Cols) -->
                  <td v-for="(v, mIdx) in prog.target_keuangan" :key="'prog-tk-' + mIdx" class="py-2 px-1 text-center font-bold text-[10px] border-r border-slate-150 dark:border-slate-800/50 bg-blue-500/[0.03]">
                    {{ formatPercent(v) }}
                  </td>
                </tr>

                <!-- LOOP KEGIATAN (LEVEL 2) -->
                <template v-if="expandedNodes['prog-' + prog.kode]" v-for="keg in prog.kegiatan" :key="'keg-' + keg.kode">
                  
                  <!-- KEGIATAN ROW -->
                  <tr 
                    @click="toggleNode('keg-' + keg.kode)"
                    class="bg-blue-50/30 dark:bg-blue-950/20 hover:bg-blue-50/60 dark:hover:bg-blue-950/30 transition-colors cursor-pointer group"
                  >
                    <!-- Aksi Column (Sticky Left 0) -->
                    <td class="py-2.5 px-2 text-center border-r border-b border-slate-200 dark:border-slate-800 sticky left-0 bg-blue-50/30 dark:bg-[#141d30] z-20 text-slate-400 font-normal">
                      -
                    </td>

                    <!-- Uraian Kegiatan (Sticky Left 90px, Indented Level 1) -->
                    <td class="py-2.5 px-4 pl-9 border-r border-b border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-[90px] bg-blue-50/30 dark:bg-[#141d30] z-20">
                      <div class="flex items-center space-x-2 min-w-0 max-w-[310px]">
                        <ChevronRight 
                          class="w-3.5 h-3.5 text-blue-500 transition-transform duration-200 shrink-0" 
                          :class="expandedNodes['keg-' + keg.kode] ? 'rotate-90' : ''" 
                        />
                        <Layers class="w-3.5 h-3.5 text-blue-500 shrink-0" />
                        <span class="px-1.5 py-0.5 rounded font-mono font-black text-[9px] bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20 shrink-0">
                          {{ keg.kode }}
                        </span>
                        <span class="font-bold text-slate-800 dark:text-slate-200 text-xs leading-snug group-hover:text-blue-600 transition-colors truncate">
                          {{ keg.nama }}
                        </span>
                      </div>
                    </td>

                    <!-- Anggaran Renja -->
                    <td class="py-2.5 px-3 text-right font-bold text-slate-800 dark:text-slate-200 border-r border-b border-slate-200 dark:border-slate-800">
                      {{ formatRupiah(keg.anggaran_renja) }}
                    </td>

                    <!-- Anggaran Pekerjaan -->
                    <td class="py-2.5 px-3 text-right font-black text-blue-600 dark:text-blue-400 border-r border-b border-slate-200 dark:border-slate-800">
                      {{ formatRupiah(keg.anggaran_pekerjaan) }}
                    </td>

                    <!-- Target Fisik Months (12 Cols) -->
                    <td v-for="(v, mIdx) in keg.target_fisik" :key="'keg-tf-' + mIdx" class="py-2 px-1 text-center font-semibold text-[10px] border-r border-slate-150 dark:border-slate-800/50 bg-emerald-500/[0.02]">
                      {{ formatPercent(v) }}
                    </td>

                    <!-- Target Keuangan Months (12 Cols) -->
                    <td v-for="(v, mIdx) in keg.target_keuangan" :key="'keg-tk-' + mIdx" class="py-2 px-1 text-center font-semibold text-[10px] border-r border-slate-150 dark:border-slate-800/50 bg-blue-500/[0.02]">
                      {{ formatPercent(v) }}
                    </td>
                  </tr>

                  <!-- LOOP SUBKEGIATAN (LEVEL 3) -->
                  <template v-if="expandedNodes['keg-' + keg.kode]" v-for="sub in keg.subkegiatan" :key="'sub-' + sub.kode">
                    
                    <!-- SUBKEGIATAN ROW -->
                    <tr 
                      @click="toggleNode('sub-' + sub.kode)"
                      class="bg-emerald-50/30 dark:bg-emerald-950/20 hover:bg-emerald-50/50 dark:hover:bg-emerald-950/30 transition-colors cursor-pointer group"
                    >
                      <!-- Aksi Column (Sticky Left 0: [+ Pekerjaan] Button) -->
                      <td class="py-2.5 px-1.5 text-center border-r border-b border-slate-200 dark:border-slate-800 sticky left-0 bg-emerald-50/30 dark:bg-[#141d30] z-20">
                        <button 
                          v-if="!selectedOpdDetail?.is_locked"
                          @click.stop="openCreateModal(sub)"
                          class="px-2 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-[10px] rounded-lg transition-all flex items-center justify-center space-x-0.5 shadow-sm mx-auto cursor-pointer"
                          title="Tambah Paket Pekerjaan Baru"
                        >
                          <Plus class="w-3 h-3" />
                          <span>Pekerjaan</span>
                        </button>
                        <span v-else class="text-[10px] font-bold text-amber-600/80 dark:text-amber-400/80 flex items-center justify-center">
                          <Lock class="w-3 h-3 mr-0.5" /> Terkunci
                        </span>
                      </td>

                      <!-- Uraian Subkegiatan (Sticky Left 90px, Indented Level 2) -->
                      <td class="py-2.5 px-4 pl-14 border-r border-b border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-[90px] bg-emerald-50/30 dark:bg-[#141d30] z-20">
                        <div class="flex items-center space-x-2 min-w-0 max-w-[290px]">
                          <ChevronRight 
                            class="w-3.5 h-3.5 text-emerald-600 transition-transform duration-200 shrink-0" 
                            :class="expandedNodes['sub-' + sub.kode] ? 'rotate-90' : ''" 
                          />
                          <span class="px-1.5 py-0.5 rounded font-mono font-black text-[9px] bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 shrink-0">
                            {{ sub.kode }}
                          </span>
                          <span class="font-bold text-slate-800 dark:text-slate-200 text-xs leading-snug group-hover:text-emerald-600 transition-colors truncate">
                            {{ sub.nama }}
                          </span>
                        </div>
                      </td>

                      <!-- Anggaran Renja Subkegiatan -->
                      <td 
                        class="py-2.5 px-3 text-right font-black border-r border-b border-slate-200 dark:border-slate-800 transition-colors"
                        :class="Math.abs((sub.anggaran_renja || 0) - (sub.anggaran_pekerjaan || 0)) > 1 
                          ? 'bg-red-500/20 text-red-600 dark:text-red-400 font-black' 
                          : 'text-emerald-700 dark:text-emerald-400'"
                      >
                        <div class="flex items-center justify-end space-x-1">
                          <AlertTriangle v-if="Math.abs((sub.anggaran_renja || 0) - (sub.anggaran_pekerjaan || 0)) > 1" class="w-3.5 h-3.5 text-red-500 shrink-0" title="Anggaran DPA dan Pekerjaan Berbeda!" />
                          <span>{{ formatRupiah(sub.anggaran_renja) }}</span>
                        </div>
                      </td>

                      <!-- Anggaran Pekerjaan Subkegiatan -->
                      <td 
                        class="py-2.5 px-3 text-right font-black border-r border-b border-slate-200 dark:border-slate-800 transition-colors"
                        :class="Math.abs((sub.anggaran_renja || 0) - (sub.anggaran_pekerjaan || 0)) > 1 
                          ? 'bg-red-500/20 text-red-600 dark:text-red-400 font-black' 
                          : 'text-slate-800 dark:text-slate-200'"
                      >
                        {{ formatRupiah(sub.anggaran_pekerjaan) }}
                      </td>

                      <!-- Target Fisik Months (12 Cols) -->
                      <td v-for="(v, mIdx) in sub.target_fisik" :key="'sub-tf-' + mIdx" class="py-2 px-1 text-center font-bold text-[10px] text-emerald-700 dark:text-emerald-400 border-r border-slate-150 dark:border-slate-800/50 bg-emerald-500/[0.03]">
                        {{ formatPercent(v) }}
                      </td>

                      <!-- Target Keuangan Months (12 Cols) -->
                      <td v-for="(v, mIdx) in sub.target_keuangan" :key="'sub-tk-' + mIdx" class="py-2 px-1 text-center font-bold text-[10px] text-blue-700 dark:text-blue-400 border-r border-slate-150 dark:border-slate-800/50 bg-blue-500/[0.03]">
                        {{ formatPercent(v) }}
                      </td>
                    </tr>

                    <!-- LOOP PEKERJAAN (LEVEL 4) -->
                    <template v-if="expandedNodes['sub-' + sub.kode]" v-for="(pek, pIdx) in sub.pekerjaan" :key="'pek-' + pek.id">
                      
                      <!-- PEKERJAAN ROW -->
                      <tr class="hover:bg-[#308e87]/5 transition-colors">
                        <!-- Aksi Column (Sticky Left 0: Side-by-side Edit & Delete Icons) -->
                        <td class="py-2 px-1 text-center border-r border-b border-slate-150 dark:border-slate-800/60 sticky left-0 bg-white dark:bg-[#141d30] z-20">
                          <div class="flex items-center justify-center space-x-1">
                            <template v-if="!selectedOpdDetail?.is_locked">
                              <button 
                                @click.stop="openEditModal(pek, sub)"
                                class="p-1 rounded-md bg-blue-500/10 hover:bg-blue-500/20 text-blue-600 dark:text-blue-400 transition-colors cursor-pointer"
                                title="Edit Pekerjaan"
                              >
                                <Pencil class="w-3.5 h-3.5" />
                              </button>
                              <button 
                                @click.stop="confirmDeletePekerjaan(pek)"
                                class="p-1 rounded-md bg-red-500/10 hover:bg-red-500/20 text-red-600 dark:text-red-400 transition-colors cursor-pointer"
                                title="Hapus Pekerjaan"
                              >
                                <Trash2 class="w-3.5 h-3.5" />
                              </button>
                            </template>
                            <span v-else class="text-[10px] font-bold text-amber-600/80 dark:text-amber-400/80 flex items-center justify-center" title="Data RKO Terkunci (Telah Disubmit/Disetujui)">
                              <Lock class="w-3 h-3" />
                            </span>
                          </div>
                        </td>

                        <!-- Uraian Pekerjaan (Sticky Left 90px, Indented Level 3) -->
                        <td class="py-2 px-4 pl-20 border-r border-b border-slate-150 dark:border-slate-800/60 w-[360px] max-w-[360px] sticky left-[90px] bg-white dark:bg-[#141d30] z-20">
                          <div class="flex items-center space-x-2 min-w-0 max-w-[270px]">
                            <Briefcase class="w-3.5 h-3.5 text-[#f39159] shrink-0" />
                            <span class="font-bold text-slate-800 dark:text-slate-200 text-xs leading-snug truncate">
                              {{ pek.nomor_pekerjaan ? pek.nomor_pekerjaan + '.' : (pIdx + 1) + '.' }} {{ pek.nama_pekerjaan }}
                            </span>
                            <span v-if="pek.nomor_rup" class="px-1 py-0.5 rounded font-mono text-[8px] bg-slate-100 dark:bg-slate-800 text-slate-400 border border-slate-200 dark:border-slate-700 shrink-0">
                              RUP: {{ pek.nomor_rup }}
                            </span>
                          </div>
                        </td>

                        <!-- Anggaran Renja Pekerjaan (Dash) -->
                        <td class="py-2 px-3 text-right font-medium text-slate-400 border-r border-b border-slate-150 dark:border-slate-800/60">
                          -
                        </td>

                        <!-- Anggaran Pekerjaan (Pagu) -->
                        <td class="py-2 px-3 text-right font-black text-slate-900 dark:text-white border-r border-b border-slate-150 dark:border-slate-800/60">
                          {{ formatRupiah(pek.pagu_anggaran) }}
                        </td>

                        <!-- Target Fisik Months (12 Cols) -->
                        <td v-for="(v, mIdx) in pek.target_fisik" :key="'pek-tf-' + mIdx" class="py-2 px-1 text-center font-medium text-[10px] text-slate-700 dark:text-slate-300 border-r border-slate-100 dark:border-slate-800/40">
                          {{ formatPercent(v) }}
                        </td>

                        <!-- Target Keuangan Months (12 Cols) -->
                        <td v-for="(v, mIdx) in pek.target_keuangan" :key="'pek-tk-' + mIdx" class="py-2 px-1 text-center font-medium text-[10px] text-slate-700 dark:text-slate-300 border-r border-slate-100 dark:border-slate-800/40">
                          {{ formatPercent(v) }}
                        </td>
                      </tr>

                    </template>

                  </template>

                </template>

              </template>

            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL FORM: TAMBAH / EDIT PEKERJAAN (LENGKAP) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200 my-auto">
        
        <!-- Modal Header -->
        <div class="px-6 py-4 bg-gradient-to-r from-[#1a4845] to-[#308e87] text-white flex items-center justify-between">
          <div>
            <span class="text-[10px] font-black uppercase tracking-widest text-[#3aada4]">Form Kelola Pekerjaan</span>
            <h3 class="text-base font-black">{{ isEditMode ? 'Edit Paket Pekerjaan' : 'Tambah Paket Pekerjaan Baru' }}</h3>
          </div>
          <button @click="showModal = false" class="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors cursor-pointer">
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Modal Body (Form Lengkap) -->
        <form @submit.prevent="savePekerjaan" class="p-6 space-y-6 overflow-y-auto flex-1 text-xs">
          
          <!-- Section 1: Informasi Pekerjaan -->
          <div class="space-y-4">
            <h4 class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-[11px] pb-1 border-b border-slate-200 dark:border-slate-800 flex items-center space-x-1.5">
              <Briefcase class="w-4 h-4 text-[#308e87]" />
              <span>Informasi Paket Pekerjaan</span>
            </h4>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <!-- Subkegiatan Name (Readonly) -->
              <div class="sm:col-span-2 lg:col-span-3 space-y-1">
                <label class="font-bold text-slate-600 dark:text-slate-400">Subkegiatan Target</label>
                <input type="text" :value="targetSubkegiatanName" readonly class="w-full px-3.5 py-2.5 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-600 dark:text-slate-300" />
              </div>

              <!-- Nomor Pekerjaan -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Nomor Pekerjaan</label>
                <input v-model.number="form.nomor_pekerjaan" type="number" placeholder="Contoh: 1" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-mono text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

              <!-- Nama Pekerjaan -->
              <div class="sm:col-span-2 space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Nama Paket Pekerjaan <span class="text-red-500">*</span></label>
                <input v-model="form.nama_pekerjaan" type="text" required placeholder="Contoh: Belanja Modal Pengadaan Peralatan..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

              

              <!-- Keterangan Pekerjaan -->
              <div class="sm:col-span-2 lg:col-span-3 space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Keterangan Pekerjaan</label>
                <textarea v-model="form.ket_pekerjaan" rows="2" placeholder="Keterangan rincian paket pekerjaan..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]"></textarea>
              </div>

              <!-- Anggaran (pagu_anggaran) -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Anggaran (Rp) <span class="text-red-500">*</span></label>
                <input v-model.number="form.pagu_anggaran" type="number" step="any" required min="0" placeholder="0" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-black text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

              <!-- Volume -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Volume</label>
                <input v-model.number="form.volume" type="number" step="any" placeholder="0" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

              <!-- Satuan -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Satuan</label>
                <input v-model="form.satuan" type="text" placeholder="Contoh: Paket, Unit, Meter..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

              <!-- Jenis Paket -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Jenis Paket</label>
                <select v-model.number="form.jenis_paket" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
                  <option :value="1">1 - Penyedia</option>
                  <option :value="2">2 - Swakelola</option>
                </select>
              </div>

              <!-- Jenis Pekerjaan (jenis_pengadaan) -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Jenis Pekerjaan</label>
                <select v-model.number="form.jenis_pengadaan" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
                  <option :value="1">1 - Pengadaan Barang</option>
                  <option :value="2">2 - Jasa Konsultasi</option>
                  <option :value="3">3 - Jasa Lainnya</option>
                  <option :value="4">4 - Konstruksi</option>
                </select>
              </div>

              <!-- Nomor RUP -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Nomor RUP</label>
                <input v-model="form.nomor_rup" type="text" placeholder="Contoh: 493012" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-mono text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

              <!-- PPK (Pejabat Pembuat Komitmen) -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Nama PPK (Pilih Personel)</label>
                <select v-model="form.nama_ppk" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
                  <option value="">-- Pilih PPK dari Personel --</option>
                  <option v-for="p in personelOptions" :key="'ppk-' + p.id" :value="p.nama">
                    {{ p.nama }} {{ p.jabatan ? '(' + p.jabatan + ')' : '' }}
                  </option>
                </select>
              </div>

              <!-- PPTK (Pejabat Pelaksana Teknis Kegiatan) -->
              <div class="space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Nama PPTK (Pilih Personel)</label>
                <select v-model="form.nama_pptk" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
                  <option value="">-- Pilih PPTK dari Personel --</option>
                  <option v-for="p in personelOptions" :key="'pptk-' + p.id" :value="p.nama">
                    {{ p.nama }} {{ p.jabatan ? '(' + p.jabatan + ')' : '' }}
                  </option>
                </select>
              </div>

              <!-- Sumber Dana (ref_sumberdana - Searchable Combobox) -->
              <div class="sm:col-span-2 lg:col-span-3 space-y-1 relative">
                <label class="font-bold text-slate-700 dark:text-slate-300">Sumber Dana</label>

                <div class="relative">
                  <!-- Trigger Button -->
                  <button
                    type="button"
                    @click="isSumberDanaDropdownOpen = !isSumberDanaDropdownOpen"
                    class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-left flex items-center justify-between font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87] transition-colors cursor-pointer"
                  >
                    <span v-if="selectedSumberDanaObj" class="truncate">
                      <span class="font-mono text-[#308e87] dark:text-[#3aada4] font-extrabold mr-1.5">[{{ selectedSumberDanaObj.kode_dana }}]</span>
                      <span>{{ selectedSumberDanaObj.nama_dana }}</span>
                    </span>
                    <span v-else class="text-slate-400 font-normal">-- Pilih Sumber Dana (Ketik untuk Mencari...) --</span>
                    <ChevronDown class="w-4 h-4 text-slate-400 shrink-0 ml-2 transition-transform duration-200" :class="isSumberDanaDropdownOpen ? 'rotate-180' : ''" />
                  </button>

                  <!-- Searchable Dropdown Popup -->
                  <div 
                    v-if="isSumberDanaDropdownOpen"
                    class="absolute z-50 mt-1.5 w-full bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl p-2.5 space-y-2 animate-in fade-in zoom-in-95 duration-150"
                  >
                    <!-- Search Input Box -->
                    <div class="relative">
                      <Search class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                      <input 
                        v-model="sumberDanaSearchQuery"
                        type="text"
                        placeholder="Cari kode atau nama sumber dana..."
                        class="w-full pl-9 pr-8 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]"
                        autoFocus
                      />
                      <button 
                        v-if="sumberDanaSearchQuery" 
                        type="button" 
                        @click="sumberDanaSearchQuery = ''"
                        class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                      >
                        <X class="w-3.5 h-3.5" />
                      </button>
                    </div>

                    <!-- Options List -->
                    <div class="max-h-56 overflow-y-auto space-y-1 p-1">
                      <div 
                        @click="selectSumberDanaOption(null)"
                        class="p-2 rounded-xl text-xs font-bold text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 cursor-pointer flex items-center justify-between"
                      >
                        <span>-- Tanpa Sumber Dana --</span>
                        <Check v-if="!form.id_sumber_dana" class="w-4 h-4 text-[#308e87]" />
                      </div>

                      <template v-if="filteredSumberDanaOptions.length > 0">
                        <div 
                          v-for="sd in filteredSumberDanaOptions"
                          :key="'sd-opt-' + sd.id_dana"
                          @click="selectSumberDanaOption(sd)"
                          class="p-2 rounded-xl text-xs transition-colors cursor-pointer flex items-center justify-between"
                          :class="form.id_sumber_dana === sd.id_dana ? 'bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] font-extrabold border border-[#308e87]/30' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800/80 font-medium'"
                        >
                          <div class="flex items-center space-x-2 truncate pr-2">
                            <span class="font-mono text-[11px] font-black px-1.5 py-0.5 rounded bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300 shrink-0">
                              {{ sd.kode_dana }}
                            </span>
                            <span class="truncate">{{ sd.nama_dana }}</span>
                          </div>
                          <Check v-if="form.id_sumber_dana === sd.id_dana" class="w-4 h-4 text-[#308e87] shrink-0 ml-2" />
                        </div>
                      </template>
                      <div v-else class="p-3 text-center text-xs text-slate-400 font-bold">
                        Tidak ditemukan sumber dana yang cocok.
                      </div>
                    </div>

                  </div>
                </div>
              </div>

              <!-- Swakelola specific fields -->
              <template v-if="form.jenis_paket === 2">
                <!-- Tipe Swakelola -->
                <div class="space-y-1">
                  <label class="font-bold text-slate-700 dark:text-slate-300">Tipe Swakelola</label>
                  <select v-model.number="form.tipe_swa" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
                    <option :value="null">-- Pilih Tipe Swakelola --</option>
                    <option :value="1">1 - Tipe 1</option>
                    <option :value="2">2 - Tipe 2</option>
                    <option :value="3">3 - Tipe 3</option>
                    <option :value="4">4 - Tipe 4</option>
                  </select>
                </div>

                <!-- Penyelenggara Swakelola -->
                <div class="sm:col-span-2 space-y-1">
                  <label class="font-bold text-slate-700 dark:text-slate-300">Penyelenggara Swakelola</label>
                  <input v-model="form.penyelenggara_swa" type="text" placeholder="Nama instansi/kelompok penyelenggara..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
                </div>
              </template>

              <!-- Penyedia specific field -->
              <template v-if="form.jenis_paket === 1">
                <!-- Metode Pemilihan Penyedia -->
                <div class="sm:col-span-2 lg:col-span-3 space-y-1">
                  <label class="font-bold text-slate-700 dark:text-slate-300">Metode Pemilihan Penyedia</label>
                  <select v-model.number="form.metode" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
                    <option :value="null">-- Pilih Metode Pemilihan --</option>
                    <option :value="1">1 - Lelang</option>
                    <option :value="2">2 - Seleksi Umum</option>
                    <option :value="3">3 - Lelang Sederhana</option>
                    <option :value="4">4 - Pengadaan Langsung</option>
                    <option :value="5">5 - Penunjukan Langsung</option>
                    <option :value="6">6 - E-Purchasing</option>
                    <option :value="7">7 - Swakelola</option>
                  </select>
                </div>
              </template>

            </div>
          </div>

          <!-- Section 2: Jadwal Pelaksanaan, Pemilihan & Kontrak -->
          <div class="space-y-4 pt-2">
            <h4 class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-[11px] pb-1 border-b border-slate-200 dark:border-slate-800 flex items-center space-x-1.5">
              <Calendar class="w-4 h-4 text-[#308e87]" />
              <span>Jadwal Pelaksanaan, Pemilihan &amp; Kontrak</span>
            </h4>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <!-- Pelaksanaan Pekerjaan (Multiselect Combobox) -->
              <div :class="Number(form.jenis_paket) === 2 ? 'sm:col-span-3' : ''" class="p-3.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3 relative">
                <div class="flex items-center justify-between">
                  <span class="font-black text-xs text-[#308e87] dark:text-[#3aada4]">Pelaksanaan Pekerjaan</span>
                  <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]">
                    {{ (form.pelaksanaan_bulan || []).length }} Bulan Dipilih
                  </span>
                </div>

                <!-- Multiselect Dropdown Toggle Trigger -->
                <div class="relative">
                  <button 
                    type="button"
                    @click="isPelaksanaanDropdownOpen = !isPelaksanaanDropdownOpen"
                    class="w-full px-3 py-2 bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-xs font-bold text-left flex items-center justify-between focus:outline-none focus:border-[#308e87] cursor-pointer transition-colors"
                  >
                    <div class="flex flex-wrap gap-1 items-center max-h-16 overflow-y-auto pr-2">
                      <template v-if="form.pelaksanaan_bulan && form.pelaksanaan_bulan.length > 0">
                        <span 
                          v-for="mIdx in [...form.pelaksanaan_bulan].sort((a,b) => a-b)" 
                          :key="'p-badge-' + mIdx"
                          class="inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-black bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20"
                        >
                          {{ monthNames[mIdx - 1] }}
                        </span>
                      </template>
                      <span v-else class="text-slate-400 font-normal">-- Pilih Bulan Pelaksanaan (Multiselect) --</span>
                    </div>
                    <ChevronDown class="w-4 h-4 text-slate-400 shrink-0 ml-2 transition-transform duration-200" :class="isPelaksanaanDropdownOpen ? 'rotate-180' : ''" />
                  </button>

                  <!-- Dropdown Menu Options (12 Months Checkboxes) -->
                  <div 
                    v-if="isPelaksanaanDropdownOpen"
                    class="absolute z-50 mt-1.5 w-full bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl p-3 space-y-2 animate-in fade-in zoom-in-95 duration-150 min-w-[260px]"
                  >
                    <div class="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
                      <span class="text-[10px] font-black text-slate-500 uppercase tracking-wider">Bulan Pelaksanaan</span>
                      <div class="space-x-2">
                        <button 
                          type="button"
                          @click="selectAllPelaksanaanMonths"
                          class="text-[10px] font-bold text-[#308e87] dark:text-[#3aada4] hover:underline cursor-pointer"
                        >
                          Pilih Semua
                        </button>
                        <button 
                          type="button"
                          @click="clearAllPelaksanaanMonths"
                          class="text-[10px] font-bold text-rose-500 hover:underline cursor-pointer"
                        >
                          Hapus Semua
                        </button>
                      </div>
                    </div>

                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-1.5 max-h-48 overflow-y-auto p-1">
                      <label 
                        v-for="(mName, i) in monthNames" 
                        :key="'p-month-' + (i + 1)"
                        class="flex items-center space-x-2 p-1.5 rounded-lg border transition-colors cursor-pointer text-xs font-bold select-none"
                        :class="form.pelaksanaan_bulan && form.pelaksanaan_bulan.includes(i + 1) ? 'bg-[#308e87]/15 border-[#308e87]/40 text-[#308e87] dark:text-[#3aada4]' : 'bg-slate-50 dark:bg-slate-800/50 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'"
                      >
                        <input 
                          type="checkbox"
                          :value="i + 1"
                          v-model="form.pelaksanaan_bulan"
                          @change="syncPelaksanaanAwalAkhir"
                          class="rounded border-slate-300 text-[#308e87] focus:ring-[#308e87]"
                        />
                        <span>{{ mName }}</span>
                      </label>
                    </div>

                    <div class="pt-2 border-t border-slate-100 dark:border-slate-800 text-right">
                      <button 
                        type="button" 
                        @click="isPelaksanaanDropdownOpen = false"
                        class="px-3 py-1 bg-[#308e87] text-white text-[11px] font-bold rounded-lg hover:bg-[#25736d] transition-colors cursor-pointer"
                      >
                        Selesai
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Pemilihan Penyedia (Awal - Akhir) -->
              <div v-if="Number(form.jenis_paket) !== 2" class="p-3.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
                <span class="font-black text-xs text-blue-600 dark:text-blue-400 block">Pemilihan Penyedia</span>
                <div class="space-y-2">
                  <div>
                    <label class="text-[10px] font-bold text-slate-500 block">Bulan Awal</label>
                    <select v-model.number="form.awal_pemilihan" class="w-full py-1.5 px-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-bold">
                      <option :value="null">-- Bulan --</option>
                      <option v-for="(m, i) in monthNames" :key="'apem-' + i" :value="i + 1">{{ m }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="text-[10px] font-bold text-slate-500 block">Bulan Akhir</label>
                    <select v-model.number="form.akhir_pemilihan" class="w-full py-1.5 px-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-bold">
                      <option :value="null">-- Bulan --</option>
                      <option v-for="(m, i) in monthNames" :key="'akpem-' + i" :value="i + 1">{{ m }}</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Pelaksanaan Kontrak (Awal - Akhir) -->
              <div v-if="Number(form.jenis_paket) !== 2" class="p-3.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
                <span class="font-black text-xs text-purple-600 dark:text-purple-400 block">Pelaksanaan Kontrak</span>
                <div class="space-y-2">
                  <div>
                    <label class="text-[10px] font-bold text-slate-500 block">Bulan Awal</label>
                    <select v-model.number="form.awal_kontrak" class="w-full py-1.5 px-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-bold">
                      <option :value="null">-- Bulan --</option>
                      <option v-for="(m, i) in monthNames" :key="'akont-' + i" :value="i + 1">{{ m }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="text-[10px] font-bold text-slate-500 block">Bulan Akhir</label>
                    <select v-model.number="form.akhir_kontrak" class="w-full py-1.5 px-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-bold">
                      <option :value="null">-- Bulan --</option>
                      <option v-for="(m, i) in monthNames" :key="'akkont-' + i" :value="i + 1">{{ m }}</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Section 3: Tagging Combobox Multi-Select Dropdown -->
          <div class="space-y-3 pt-2">
            <h4 class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-[11px] pb-1 border-b border-slate-200 dark:border-slate-800 flex items-center space-x-1.5">
              <Tag class="w-4 h-4 text-purple-600" />
              <span>Tagging Program / Prioritas</span>
            </h4>

            <div class="relative space-y-2">
              <label class="font-bold text-slate-700 dark:text-slate-300 block">
                Tagging (Combobox Multi-Select Dropdown)
              </label>

              <!-- Custom Combobox Trigger Box -->
              <div 
                @click.stop="isTagDropdownOpen = !isTagDropdownOpen"
                class="min-h-[44px] w-full p-2 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl cursor-pointer flex items-center justify-between gap-2 focus:border-purple-600 transition-all shadow-xs"
                :class="isTagDropdownOpen ? 'border-purple-600 ring-2 ring-purple-500/20' : ''"
              >
                <!-- Badges or Placeholder -->
                <div class="flex flex-wrap gap-1.5 items-center flex-1">
                  <span 
                    v-for="(tName, tIdx) in form.tags" 
                    :key="tIdx"
                    class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-lg text-xs font-bold bg-purple-600 text-white shadow-xs"
                  >
                    <span>{{ tName }}</span>
                    <button 
                      type="button" 
                      @click.stop="removeTag(tIdx)" 
                      class="hover:text-purple-200 ml-0.5 cursor-pointer"
                    >
                      <X class="w-3 h-3" />
                    </button>
                  </span>
                  <span v-if="!form.tags || form.tags.length === 0" class="text-slate-400 font-medium text-xs px-1">
                    -- Pilih Tagging (Multi-select Combobox) --
                  </span>
                </div>

                <ChevronDown class="w-4 h-4 text-slate-400 shrink-0 transition-transform duration-200" :class="isTagDropdownOpen ? 'rotate-180 text-purple-600' : ''" />
              </div>

              <!-- Dropdown Popover Menu -->
              <div 
                v-if="isTagDropdownOpen"
                @click.stop
                class="absolute left-0 right-0 mt-1 bg-white dark:bg-[#1a263d] border-2 border-purple-500/30 rounded-2xl shadow-2xl z-50 p-3 space-y-2 animate-in fade-in zoom-in-95 duration-150 max-h-64 flex flex-col"
              >
                <!-- Search Filter & Quick Reset -->
                <div class="flex items-center justify-between gap-2 pb-2 border-b border-slate-100 dark:border-slate-800">
                  <div class="relative flex-1">
                    <Search class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2" />
                    <input 
                      v-model="tagSearchQuery" 
                      type="text" 
                      placeholder="Cari tagging..." 
                      class="w-full pl-8 pr-2 py-1.5 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-bold focus:outline-none focus:border-purple-500" 
                    />
                  </div>
                  <button 
                    type="button" 
                    @click="clearAllTags" 
                    class="text-[10px] font-black text-rose-500 hover:underline shrink-0 cursor-pointer"
                  >
                    Reset
                  </button>
                </div>

                <!-- Checkboxes Multi-Select List -->
                <div class="overflow-y-auto space-y-1 flex-1 pr-1">
                  <div 
                    v-for="t in filteredTaggingOptions" 
                    :key="t.id"
                    @click="toggleTagSelection(t.tag)"
                    class="flex items-center justify-between p-2 rounded-xl text-xs font-bold cursor-pointer transition-colors"
                    :class="form.tags && form.tags.includes(t.tag) ? 'bg-purple-500/10 text-purple-700 dark:text-purple-300' : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'"
                  >
                    <div class="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        :checked="form.tags && form.tags.includes(t.tag)" 
                        @click.stop="toggleTagSelection(t.tag)"
                        class="rounded text-purple-600 focus:ring-purple-500 cursor-pointer" 
                      />
                      <span>{{ t.tag }}</span>
                    </div>
                    <Check v-if="form.tags && form.tags.includes(t.tag)" class="w-3.5 h-3.5 text-purple-600" />
                  </div>

                  <div v-if="filteredTaggingOptions.length === 0" class="text-center py-4 text-slate-400 text-xs italic">
                    Tidak ada tagging ditemukan
                  </div>
                </div>
              </div>
            </div>
          </div>

          
          <!-- Section 4: Multi-Lokasi Pekerjaan & Map (PostGIS & Leaflet Geoman) -->
          <div class="space-y-4 pt-2">
            <h4 class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-[11px] pb-1 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <div class="flex items-center space-x-1.5">
                <MapPin class="w-4 h-4 text-emerald-600" />
                <span>Lokasi Pekerjaan </span>
              </div>
              <span class="text-[10px] text-slate-400 font-medium">Bisa memilih lebih dari 1 lokasi (Titik, Garis, Polygon, Kotak, Bundar)</span>
            </h4>

            <!-- Text Lokasi Pekerjaan -->
              <div class="sm:col-span-2 lg:col-span-3 space-y-1">
                <label class="font-bold text-slate-700 dark:text-slate-300">Lokasi Pekerjaan (Text Alamat / Kecamatan / Kelurahan)</label>
                <input v-model="form.lokasi" type="text" placeholder="Contoh: Kecamatan Tegal Barat, Kelurahan Debong Candi..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
              </div>

            <div class="space-y-3">
              <!-- Instruction Banner & Quick Add Text Button -->
              <div class="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl flex items-center justify-between gap-2 text-xs">
                <div class="flex items-center space-x-2 text-emerald-800 dark:text-emerald-300 font-bold">
                  <Map class="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Gunakan toolbar gambar di kiri peta (Titik 📍, Garis 📈, Polygon ⬡, Kotak 🔲, Bundar ⭕) atau tambah text lokasi manual.</span>
                </div>
                <div class="flex items-center space-x-2 shrink-0">
                  <button 
                    type="button" 
                    @click="addManualTextLocation" 
                    class="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[11px] flex items-center space-x-1 transition-colors cursor-pointer shadow-xs"
                  >
                    <Plus class="w-3.5 h-3.5" />
                    <span>Tambah Lokasi Text</span>
                  </button>
                  <span class="px-2.5 py-1 rounded-full font-black text-[10px] bg-slate-900 dark:bg-white dark:text-slate-900 text-white">
                    {{ form.lokasi_list?.length || 0 }} Lokasi
                  </span>
                </div>
              </div>

              <!-- Leaflet Map Container -->
              <div class="relative w-full h-80 rounded-2xl overflow-hidden border-2 border-slate-200 dark:border-slate-700 shadow-inner">
                <div id="rko-pekerjaan-map" class="w-full h-full z-10"></div>
              </div>

              <!-- Location Cards List -->
              <div v-if="form.lokasi_list && form.lokasi_list.length > 0" class="space-y-2">
                <label class="font-bold text-slate-700 dark:text-slate-300 text-xs block">Daftar Lokasi Terdaftar (PostGIS):</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <div 
                    v-for="(loc, lIdx) in form.lokasi_list" 
                    :key="lIdx"
                    class="p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col justify-between space-y-2 shadow-xs"
                  >
                    <div class="flex items-start justify-between gap-2">
                      <div class="space-y-1 flex-1">
                        <div class="flex items-center space-x-1.5">
                          <span class="px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-wider bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 shrink-0">
                            {{ loc.jenis_geometry || 'Point' }}
                          </span>
                          <input 
                            v-model="loc.nama_lokasi" 
                            type="text" 
                            placeholder="Nama Lokasi..." 
                            class="w-full font-bold text-slate-800 dark:text-slate-200 text-xs bg-transparent border-b border-dashed border-slate-300 dark:border-slate-700 focus:outline-none focus:border-emerald-500" 
                          />
                        </div>
                        <div class="text-[10px] font-mono text-slate-400">
                          Lat: {{ loc.lat ? Number(loc.lat).toFixed(5) : '-' }}, Lng: {{ loc.lng ? Number(loc.lng).toFixed(5) : '-' }}
                          <span v-if="loc.radius">| Radius: {{ loc.radius }}m</span>
                        </div>
                      </div>

                      <button 
                        type="button" 
                        @click="removeLocationItem(lIdx)" 
                        class="p-1 rounded-lg hover:bg-rose-500/20 text-rose-500 transition-colors cursor-pointer"
                        title="Hapus Lokasi Ini"
                      >
                        <Trash2 class="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Section 5: Target Fisik & Keuangan Bulanan -->
          <div class="space-y-4 pt-2">
            <h4 class="font-black text-slate-900 dark:text-white uppercase tracking-wider text-[11px] pb-1 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <span>Target Rencana Fisik (%) & Keuangan (%) Bulanan</span>
              <span class="text-[10px] text-slate-400 font-medium">Persentase Kumulatif (0 - 100%)</span>
            </h4>

            <!-- Grid 12 Bulan Target Fisik (%) -->
            <div class="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/20 space-y-2">
              <label class="font-black text-emerald-700 dark:text-emerald-400 flex items-center justify-between">
                <span>Target Fisik (%) Bulanan</span>
                <span class="text-[10px] text-emerald-600/80 font-semibold">Progresif Positif &amp; Maks 100%</span>
              </label>
              <div class="grid grid-cols-3 sm:grid-cols-6 gap-2">
                <div v-for="(m, idx) in monthShorts" :key="'f-' + idx" class="space-y-1">
                  <label class="text-[10px] font-bold text-slate-500 block text-center">{{ m }}</label>
                  <input 
                    v-model.number="form.target_fisik[idx]" 
                    @input="onTargetFisikChange(idx)"
                    type="number" 
                    step="any" 
                    min="0" 
                    max="100" 
                    class="w-full py-1.5 px-2 bg-white dark:bg-slate-900 border border-emerald-500/30 rounded-lg text-center font-bold text-emerald-700 dark:text-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-500" 
                  />
                </div>
              </div>
            </div>

            <!-- Grid 12 Bulan Target Keuangan (%) -->
            <div class="p-4 rounded-2xl bg-blue-500/5 border border-blue-500/20 space-y-2">
              <label class="font-black text-blue-700 dark:text-blue-400 flex items-center justify-between">
                <span>Target Keuangan (%) Bulanan</span>
                <span class="text-[10px] text-blue-600/80 font-semibold">Progresif Positif &amp; Maks 100%</span>
              </label>
              <div class="grid grid-cols-3 sm:grid-cols-6 gap-2">
                <div v-for="(m, idx) in monthShorts" :key="'k-' + idx" class="space-y-1">
                  <label class="text-[10px] font-bold text-slate-500 block text-center">{{ m }}</label>
                  <input 
                    v-model.number="form.target_keuangan[idx]" 
                    @input="onTargetKeuanganChange(idx)"
                    type="number" 
                    step="any" 
                    min="0" 
                    max="100" 
                    class="w-full py-1.5 px-2 bg-white dark:bg-slate-900 border border-blue-500/30 rounded-lg text-center font-bold text-blue-700 dark:text-blue-400 focus:outline-none focus:ring-1 focus:ring-blue-500" 
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end space-x-3">
            <button type="button" @click="showModal = false" class="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 font-bold transition-all cursor-pointer">
              Batal
            </button>
            <button type="submit" :disabled="saving" class="px-6 py-2.5 rounded-xl bg-[#308e87] hover:bg-[#256e69] text-white font-black transition-all flex items-center space-x-1.5 shadow-md shadow-[#308e87]/20 cursor-pointer">
              <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
              <Save v-else class="w-4 h-4" />
              <span>{{ isEditMode ? 'Simpan Perubahan' : 'Tambah Pekerjaan' }}</span>
            </button>
          </div>

        </form>

      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL CONFIRM DELETE -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-md space-y-4 shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        <div class="w-12 h-12 rounded-2xl bg-red-500/10 text-red-500 flex items-center justify-center mx-auto">
          <AlertTriangle class="w-6 h-6" />
        </div>
        <div class="text-center space-y-1">
          <h3 class="text-base font-black text-slate-900 dark:text-white">Hapus Paket Pekerjaan?</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Apakah Anda yakin ingin menghapus paket pekerjaan <strong class="text-slate-800 dark:text-slate-200">"{{ pekerjaanToDelete?.nama_pekerjaan }}"</strong>? Data yang dihapus tidak dapat dikembalikan.
          </p>
        </div>
        <div class="flex items-center justify-center space-x-3 pt-2">
          <button @click="showDeleteModal = false" class="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 font-bold text-xs cursor-pointer">
            Batal
          </button>
          <button @click="executeDeletePekerjaan" :disabled="deleting" class="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white font-black text-xs transition-all flex items-center space-x-1 shadow-md shadow-red-600/20 cursor-pointer">
            <Loader2 v-if="deleting" class="w-3.5 h-3.5 animate-spin" />
            <Trash2 v-else class="w-3.5 h-3.5" />
            <span>Ya, Hapus Paket</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL PROSEDUR SUBMIT RKO & CHECKLIST VALIDASI -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showSubmitModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl w-full max-w-2xl flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        <!-- Modal Header -->
        <div class="px-6 py-4 bg-gradient-to-r from-emerald-700 via-teal-700 to-[#308e87] text-white flex items-center justify-between">
          <div>
            <span class="text-[10px] font-black uppercase tracking-widest text-emerald-200">Prosedur Submission RKO</span>
            <h3 class="text-base font-black">Validasi &amp; Submit RKO {{ selectedOpdDetail?.opd?.nama_pd_singkat || selectedOpdDetail?.opd?.nama_pd }}</h3>
          </div>
          <button @click="showSubmitModal = false" class="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors cursor-pointer">
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Modal Body (Checklist) -->
        <div class="p-6 space-y-5 overflow-y-auto max-h-[75vh]">
          <p class="text-xs text-slate-600 dark:text-slate-300 font-medium leading-relaxed">
            Sebelum melakukan penyerahan RKO, sistem memverifikasi 3 aturan kelayakan utama:
          </p>

          <!-- Loading State -->
          <div v-if="loadingValidation" class="py-12 flex flex-col items-center justify-center space-y-3 text-slate-400">
            <Loader2 class="w-8 h-8 animate-spin text-emerald-600" />
            <span class="font-bold text-xs">Memverifikasi 3 kelayakan RKO...</span>
          </div>

          <!-- Validation Checklist Cards -->
          <div v-else-if="submitValidationData" class="space-y-3">
            
            <div 
              v-for="rule in submitValidationData.checklist" 
              :key="rule.id"
              class="p-4 rounded-2xl border transition-all space-y-2"
              :class="rule.passed ? 'bg-emerald-500/5 border-emerald-500/30' : 'bg-rose-500/5 border-rose-500/30'"
            >
              <div class="flex items-start justify-between gap-2">
                <div class="flex items-center space-x-2 font-black text-xs" :class="rule.passed ? 'text-emerald-700 dark:text-emerald-300' : 'text-rose-700 dark:text-rose-300'">
                  <CheckCircle2 v-if="rule.passed" class="w-4 h-4 text-emerald-600 shrink-0" />
                  <AlertTriangle v-else class="w-4 h-4 text-rose-600 shrink-0" />
                  <span>{{ rule.title }}</span>
                </div>
                <span 
                  class="px-2 py-0.5 rounded text-[10px] font-black uppercase"
                  :class="rule.passed ? 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-200' : 'bg-rose-500/20 text-rose-800 dark:text-rose-200'"
                >
                  {{ rule.passed ? 'MEMENUHI' : 'BELUM MEMENUHI' }}
                </span>
              </div>

              <p class="text-xs font-semibold text-slate-600 dark:text-slate-300 pl-6">
                {{ rule.message }}
              </p>

              <!-- Failing Details List -->
              <div v-if="!rule.passed && rule.items?.length > 0" class="mt-2 pl-6 space-y-1">
                <div 
                  v-for="(item, iIdx) in rule.items.slice(0, 5)" 
                  :key="iIdx"
                  class="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-rose-500/20 text-[11px] font-bold text-rose-800 dark:text-rose-300"
                >
                  <div v-if="rule.id === 'rule_1'">
                    ❌ Subkegiatan <span class="font-mono text-xs">{{ item.kode }}</span> - {{ item.nama }} (0 Pekerjaan)
                  </div>
                  <div v-else-if="rule.id === 'rule_2'">
                    ❌ Subkegiatan <span class="font-mono text-xs">{{ item.kode }}</span>: Pagu DPA {{ formatRupiah(item.pagu_renja) }} != Pagu Pekerjaan {{ formatRupiah(item.pagu_pekerjaan) }} (Selisih: {{ formatRupiah(item.selisih) }})
                  </div>
                  <div v-else-if="rule.id === 'rule_3'">
                    ❌ Pekerjaan "{{ item.nama_pekerjaan }}": Target Des Keuangan {{ item.target_keuangan_des }}% | Target Des Fisik {{ item.target_fisik_des }}%
                  </div>
                </div>
                <span v-if="rule.items.length > 5" class="text-[10px] italic text-rose-500 font-bold block pt-1">
                  +{{ rule.items.length - 5 }} item lainnya...
                </span>
              </div>
            </div>

          </div>

          <!-- Action Footer -->
          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3">
            <button 
              @click="showSubmitModal = false" 
              class="px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-bold text-xs hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
            >
              Tutup
            </button>

            <button 
              @click="doSubmitRko" 
              :disabled="!submitValidationData?.is_valid || submittingRko"
              class="px-5 py-2.5 rounded-xl font-black text-xs flex items-center space-x-2 transition-all cursor-pointer shadow-md"
              :class="submitValidationData?.is_valid ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-600/30' : 'bg-slate-300 dark:bg-slate-800 text-slate-400 cursor-not-allowed'"
            >
              <Loader2 v-if="submittingRko" class="w-4 h-4 animate-spin" />
              <Send v-else class="w-4 h-4" />
              <span>{{ submitValidationData?.is_valid ? 'Konfirmasi &amp; Submit RKO' : 'Belum Memenuhi Syarat Submit' }}</span>
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { notifySuccess, notifyError, notifyWarning, confirmDialog, promptDialog } from '@/utils/notify'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import '@geoman-io/leaflet-geoman-free'
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css'
import { 
  Building2, 
  Folder, 
  Layers, 
  Briefcase, 
  Search, 
  X, 
  ChevronRight, 
  ChevronDown,
  ArrowLeft, 
  Loader2, 
  FileX,
  AlertTriangle,
  Plus,
  Pencil,
  Trash2,
  Save,
  Calendar,
  Tag,
  Check,
  MapPin,
  Map,
  Send,
  CheckCircle2,
  Lock,
  Settings
} from 'lucide-vue-next'

const authStore = useAuthStore()
const isAdmin = computed(() => {
  if (!authStore.user) return true
  if (authStore.user.role_id !== undefined && authStore.user.role_id !== null) {
    return authStore.user.role_id <= 5
  }
  return true
})

const viewMode = ref('list')
const selectedTahun = ref(2026)
const searchQuery = ref('')
const loading = ref(false)
const loadingDetail = ref(false)
const saving = ref(false)
const deleting = ref(false)
const actionLoading = ref(false)
const opdList = ref([])
const selectedOpdDetail = ref(null)

const showSubmitModal = ref(false)
const loadingValidation = ref(false)
const submitValidationData = ref(null)
const submittingRko = ref(false)

const personelOptions = ref([])

const fetchPersonelOptions = async (idSubPd) => {
  if (!idSubPd) return
  try {
    const res = await axios.get(`/api/v1/rko/personel-options/${idSubPd}`)
    personelOptions.value = res.data
  } catch (err) {
    console.warn('Gagal memuat personel options:', err)
  }
}

const taggingOptions = ref([])
const isTagDropdownOpen = ref(false)
const tagSearchQuery = ref('')

const expandedNodes = ref({})
const activeMenuId = ref(null)

const filteredTaggingOptions = computed(() => {
  if (!tagSearchQuery.value.trim()) return taggingOptions.value
  const q = tagSearchQuery.value.toLowerCase().trim()
  return taggingOptions.value.filter(t => t.tag && t.tag.toLowerCase().includes(q))
})

const toggleTagSelection = (tagVal) => {
  if (!form.value.tags) form.value.tags = []
  const idx = form.value.tags.indexOf(tagVal)
  if (idx > -1) {
    form.value.tags.splice(idx, 1)
  } else {
    form.value.tags.push(tagVal)
  }
}

const clearAllTags = () => {
  form.value.tags = []
}

const isPelaksanaanDropdownOpen = ref(false)

const syncPelaksanaanAwalAkhir = () => {
  if (!form.value.pelaksanaan_bulan || form.value.pelaksanaan_bulan.length === 0) {
    form.value.awal_pelaksanaan = null
    form.value.akhir_pelaksanaan = null
  } else {
    const sorted = [...form.value.pelaksanaan_bulan].sort((a, b) => a - b)
    form.value.awal_pelaksanaan = sorted[0]
    form.value.akhir_pelaksanaan = sorted[sorted.length - 1]
  }
}

const selectAllPelaksanaanMonths = () => {
  form.value.pelaksanaan_bulan = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  syncPelaksanaanAwalAkhir()
}

const clearAllPelaksanaanMonths = () => {
  form.value.pelaksanaan_bulan = []
  syncPelaksanaanAwalAkhir()
}

const derivePelaksanaanBulan = (d) => {
  if (Array.isArray(d.pelaksanaan_bulan) && d.pelaksanaan_bulan.length > 0) {
    return d.pelaksanaan_bulan.map(Number)
  }
  const awal = Number(d.awal_pelaksanaan)
  const akhir = Number(d.akhir_pelaksanaan)
  if (awal > 0 && akhir >= awal) {
    const list = []
    for (let i = awal; i <= akhir; i++) list.push(i)
    return list
  }
  return []
}

const sumberDanaOptions = ref([])
const isSumberDanaDropdownOpen = ref(false)
const sumberDanaSearchQuery = ref('')

const fetchRefSumberDana = async () => {
  try {
    const res = await axios.get('/api/v1/rko/ref-sumberdana')
    sumberDanaOptions.value = res.data
  } catch (err) {
    console.warn('Gagal memuat ref_sumberdana:', err)
  }
}

const filteredSumberDanaOptions = computed(() => {
  if (!sumberDanaSearchQuery.value.trim()) return sumberDanaOptions.value
  const q = sumberDanaSearchQuery.value.toLowerCase().trim()
  return sumberDanaOptions.value.filter(sd => 
    (sd.kode_dana && sd.kode_dana.toLowerCase().includes(q)) ||
    (sd.nama_dana && sd.nama_dana.toLowerCase().includes(q)) ||
    (sd.sumber_dana && sd.sumber_dana.toLowerCase().includes(q))
  )
})

const selectedSumberDanaObj = computed(() => {
  if (!form.value.id_sumber_dana) return null
  return sumberDanaOptions.value.find(sd => sd.id_dana === form.value.id_sumber_dana) || null
})

const selectSumberDanaOption = (sdObj) => {
  if (!sdObj) {
    form.value.id_sumber_dana = null
    form.value.sumber_dana = ''
  } else {
    form.value.id_sumber_dana = sdObj.id_dana
    form.value.sumber_dana = sdObj.sumber_dana || sdObj.nama_dana
  }
  isSumberDanaDropdownOpen.value = false
  sumberDanaSearchQuery.value = ''
}

const monthNames = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
const monthShorts = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
const monthKeys = ['jan', 'feb', 'mar', 'apr', 'mei', 'jun', 'jul', 'agu', 'sep', 'okt', 'nov', 'des']

// Modal States
const showModal = ref(false)
const isEditMode = ref(false)
const editingPekerjaanId = ref(null)
const targetSubkegiatanName = ref('')
const showDeleteModal = ref(false)
const pekerjaanToDelete = ref(null)

const form = ref({
  id_sub_pd: null,
  id_subkegiatan: '',
  tahun: 2026,
  nomor_pekerjaan: null,
  nama_pekerjaan: '',
  ket_pekerjaan: '',
  pagu_anggaran: 0,
  volume: null,
  satuan: '',
  nomor_rup: '',
  jenis_paket: 1,
  jenis_pengadaan: 1,
  tipe_swa: null,
  penyelenggara_swa: '',
  metode: null,
  awal_pelaksanaan: null,
  akhir_pelaksanaan: null,
  pelaksanaan_bulan: [],
  awal_pemilihan: null,
  akhir_pemilihan: null,
  awal_kontrak: null,
  akhir_kontrak: null,
  nama_ppk: '',
  nama_pptk: '',
  id_sumber_dana: null,
  sumber_dana: '',
  tags: [],
  target_fisik: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  target_keuangan: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
})

const filteredOpdList = computed(() => {
  if (!searchQuery.value.trim()) return opdList.value
  const q = searchQuery.value.toLowerCase().trim()
  return opdList.value.filter(item => 
    (item.kode && item.kode.toLowerCase().includes(q)) ||
    (item.nama_pd && item.nama_pd.toLowerCase().includes(q)) ||
    (item.nama_pd_singkat && item.nama_pd_singkat.toLowerCase().includes(q))
  )
})

const formatRupiah = (val) => {
  if (!val || val === 0) return '0'
  return new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 }).format(val)
}

const formatPercent = (val) => {
  if (val === null || val === undefined) return '0'
  const num = Number(val)
  if (num === 0) return '-'
  return num % 1 === 0 ? `${num}` : `${num.toFixed(1)}`
}

const toggleMenu = (id) => {
  if (activeMenuId.value === id) {
    activeMenuId.value = null
  } else {
    activeMenuId.value = id
  }
}

const closeMenu = () => {
  activeMenuId.value = null
  isTagDropdownOpen.value = false
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/v1/rko/opd', { params: { tahun: selectedTahun.value } })
    opdList.value = res.data
  } catch (err) {
    console.warn('Gagal memuat data RKO OPD:', err)
  } finally {
    loading.value = false
  }
}

const fetchTaggingOptions = async () => {
  try {
    const res = await axios.get('/api/v1/pengaturan/tagging')
    taggingOptions.value = res.data
  } catch (err) {
    console.warn('Gagal memuat options tagging:', err)
  }
}

const onTagSelect = (event) => {
  const selectedTag = event.target.value
  if (selectedTag) {
    if (!form.value.tags) form.value.tags = []
    if (!form.value.tags.includes(selectedTag)) {
      form.value.tags.push(selectedTag)
    }
  }
  event.target.value = ''
}

const removeTag = (index) => {
  if (form.value.tags) {
    form.value.tags.splice(index, 1)
  }
}

const openOpdDetail = async (item) => {
  viewMode.value = 'detail'
  loadingDetail.value = true
  selectedOpdDetail.value = null
  expandedNodes.value = {}

  try {
    const res = await axios.get(`/api/v1/rko/detail/${item.id_sub_pd}`, { params: { tahun: selectedTahun.value } })
    selectedOpdDetail.value = res.data
    
    // Auto expand first branch
    if (res.data.programs?.length > 0) {
      const p1 = res.data.programs[0]
      expandedNodes.value['prog-' + p1.kode] = true
      if (p1.kegiatan?.length > 0) {
        const k1 = p1.kegiatan[0]
        expandedNodes.value['keg-' + k1.kode] = true
        if (k1.subkegiatan?.length > 0) {
          const s1 = k1.subkegiatan[0]
          expandedNodes.value['sub-' + s1.kode] = true
        }
      }
    }
  } catch (err) {
    console.warn('Gagal memuat detail RKO OPD:', err)
  } finally {
    loadingDetail.value = false
  }
}

const backToList = () => {
  viewMode.value = 'list'
  selectedOpdDetail.value = null
}

const onTahunChange = () => {
  if (viewMode.value === 'list') {
    fetchData()
  } else if (selectedOpdDetail.value?.opd) {
    openOpdDetail(selectedOpdDetail.value.opd)
  }
}

const toggleNode = (nodeKey) => {
  expandedNodes.value[nodeKey] = !expandedNodes.value[nodeKey]
}

const toggleAll = (expand) => {
  if (!selectedOpdDetail.value?.programs) return
  const newMap = {}
  if (expand) {
    selectedOpdDetail.value.programs.forEach(prog => {
      newMap['prog-' + prog.kode] = true
      if (prog.kegiatan) {
        prog.kegiatan.forEach(keg => {
          newMap['keg-' + keg.kode] = true
          if (keg.subkegiatan) {
            keg.subkegiatan.forEach(sub => {
              newMap['sub-' + sub.kode] = true
            })
          }
        })
      }
    })
  }
  expandedNodes.value = newMap
}

// ════════════════════════════════════════════════════════════════════
// TARGET PROGRESSIVE & AUTO-FILL 100% VALIDATION HANDLERS
// ════════════════════════════════════════════════════════════════════

const onTargetFisikChange = (idx) => {
  let val = Number(form.value.target_fisik[idx] || 0)
  if (val < 0) val = 0
  if (val > 100) val = 100
  form.value.target_fisik[idx] = val

  if (idx > 0 && val < form.value.target_fisik[idx - 1]) {
    form.value.target_fisik[idx] = form.value.target_fisik[idx - 1]
    val = form.value.target_fisik[idx]
  }

  for (let i = idx + 1; i < 12; i++) {
    if (val === 100 || form.value.target_fisik[i] < val) {
      form.value.target_fisik[i] = val
    }
  }
}

const onTargetKeuanganChange = (idx) => {
  let val = Number(form.value.target_keuangan[idx] || 0)
  if (val < 0) val = 0
  if (val > 100) val = 100
  form.value.target_keuangan[idx] = val

  if (idx > 0 && val < form.value.target_keuangan[idx - 1]) {
    form.value.target_keuangan[idx] = form.value.target_keuangan[idx - 1]
    val = form.value.target_keuangan[idx]
  }

  for (let i = idx + 1; i < 12; i++) {
    if (val === 100 || form.value.target_keuangan[i] < val) {
      form.value.target_keuangan[i] = val
    }
  }
}

// ════════════════════════════════════════════════════════════════════
// CRUD PEKERJAAN HANDLERS (FORM LENGKAP)
// ════════════════════════════════════════════════════════════════════

let rkoMap = null
let drawnItemsLayerGroup = null

const initRkoMap = () => {
  nextTick(() => {
    const mapEl = document.getElementById('rko-pekerjaan-map')
    if (!mapEl) return

    if (rkoMap) {
      rkoMap.remove()
      rkoMap = null
    }

    const defaultLat = form.value.lokasi_list?.[0]?.lat || -6.86942
    const defaultLng = form.value.lokasi_list?.[0]?.lng || 109.13824

    rkoMap = L.map('rko-pekerjaan-map').setView([defaultLat, defaultLng], 13)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap'
    }).addTo(rkoMap)

    drawnItemsLayerGroup = L.featureGroup().addTo(rkoMap)

    // Add Leaflet-Geoman Controls for Titik, Garis, Polygon, Kotak, Bundar
    rkoMap.pm.addControls({
      position: 'topleft',
      drawMarker: true,       // Titik (Point)
      drawPolyline: true,     // Garis (LineString)
      drawPolygon: true,      // Polygon
      drawRectangle: true,    // Kotak (Square)
      drawCircle: true,       // Bundar (Circle)
      drawCircleMarker: false,
      editMode: true,
      dragMode: true,
      removalMode: true
    })

    // Load existing locations on map
    if (form.value.lokasi_list && form.value.lokasi_list.length > 0) {
      form.value.lokasi_list.forEach((loc, idx) => {
        renderLocationOnMap(loc, idx)
      })
      if (drawnItemsLayerGroup.getLayers().length > 0) {
        try {
          rkoMap.fitBounds(drawnItemsLayerGroup.getBounds(), { padding: [30, 30] })
        } catch (e) {}
      }
    }

    // Event listener when shape is created
    rkoMap.on('pm:create', (e) => {
      const shapeType = e.shape
      const layer = e.layer
      const geojson = layer.toGeoJSON()

      let lat = null, lng = null, radius = null, jenisGeom = 'Point'

      if (shapeType === 'Marker') {
        jenisGeom = 'Point'
        lat = layer.getLatLng().lat
        lng = layer.getLatLng().lng
      } else if (shapeType === 'Line') {
        jenisGeom = 'LineString'
        const center = layer.getBounds().getCenter()
        lat = center.lat
        lng = center.lng
      } else if (shapeType === 'Polygon' || shapeType === 'Rectangle') {
        jenisGeom = shapeType === 'Rectangle' ? 'Square' : 'Polygon'
        const center = layer.getBounds().getCenter()
        lat = center.lat
        lng = center.lng
      } else if (shapeType === 'Circle') {
        jenisGeom = 'Circle'
        lat = layer.getLatLng().lat
        lng = layer.getLatLng().lng
        radius = layer.getRadius()
      }

      if (!form.value.lokasi_list) form.value.lokasi_list = []
      
      const newLocItem = {
        id: null,
        nama_lokasi: `Lokasi ${form.value.lokasi_list.length + 1} (${jenisGeom})`,
        jenis_geometry: jenisGeom,
        geojson: geojson.geometry || geojson,
        lat: lat,
        lng: lng,
        radius: radius
      }

      form.value.lokasi_list.push(newLocItem)
      drawnItemsLayerGroup.addLayer(layer)
      layer.bindPopup(`<b>${newLocItem.nama_lokasi}</b><br/>Tipe: ${jenisGeom}`).openPopup()
    })
  })
}

const renderLocationOnMap = (loc, idx) => {
  if (!rkoMap || !drawnItemsLayerGroup) return
  if (loc.geojson && loc.geojson.type) {
    const geoLayer = L.geoJSON(loc.geojson, {
      style: { color: '#308e87', weight: 3, opacity: 0.8, fillOpacity: 0.3 }
    })
    geoLayer.bindPopup(`<b>${loc.nama_lokasi || 'Lokasi ' + (idx + 1)}</b><br/>Tipe: ${loc.jenis_geometry}`)
    drawnItemsLayerGroup.addLayer(geoLayer)
  } else if (loc.lat && loc.lng) {
    const marker = L.marker([loc.lat, loc.lng])
    marker.bindPopup(`<b>${loc.nama_lokasi || 'Lokasi ' + (idx + 1)}</b>`)
    drawnItemsLayerGroup.addLayer(marker)
  }
}

const removeLocationItem = (index) => {
  form.value.lokasi_list.splice(index, 1)
  if (rkoMap && drawnItemsLayerGroup) {
    drawnItemsLayerGroup.clearLayers()
    if (form.value.lokasi_list) {
      form.value.lokasi_list.forEach((loc, idx) => {
        renderLocationOnMap(loc, idx)
      })
    }
  }
}

const addManualTextLocation = () => {
  if (!form.value.lokasi_list) form.value.lokasi_list = []
  form.value.lokasi_list.push({
    id: null,
    nama_lokasi: `Lokasi ${form.value.lokasi_list.length + 1}`,
    jenis_geometry: 'Text',
    geojson: null,
    lat: null,
    lng: null,
    radius: null
  })
}

const openCreateModal = (sub) => {
  isEditMode.value = false
  editingPekerjaanId.value = null
  targetSubkegiatanName.value = `${sub.kode} - ${sub.nama}`
  const targetOpdId = selectedOpdDetail.value?.opd?.id_sub_pd
  fetchPersonelOptions(targetOpdId)
  isPelaksanaanDropdownOpen.value = false
  isSumberDanaDropdownOpen.value = false
  sumberDanaSearchQuery.value = ''
  form.value = {
    id_sub_pd: targetOpdId,
    id_subkegiatan: sub.idsubkegiatan,
    tahun: selectedTahun.value,
    nomor_pekerjaan: null,
    nama_pekerjaan: '',
    ket_pekerjaan: '',
    lokasi: '',
    pagu_anggaran: 0,
    volume: null,
    satuan: '',
    nomor_rup: '',
    jenis_paket: 1,
    jenis_pengadaan: 1,
    tipe_swa: null,
    penyelenggara_swa: '',
    metode: null,
    awal_pelaksanaan: null,
    akhir_pelaksanaan: null,
    pelaksanaan_bulan: [],
    awal_pemilihan: null,
    akhir_pemilihan: null,
    awal_kontrak: null,
    akhir_kontrak: null,
    nama_ppk: '',
    nama_pptk: '',
    id_sumber_dana: null,
    sumber_dana: '',
    tags: [],
    lokasi_list: [],
    target_fisik: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    target_keuangan: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  }
  fetchTaggingOptions()
  showModal.value = true
  initRkoMap()
}

const openEditModal = async (pek, sub) => {
  isEditMode.value = true
  editingPekerjaanId.value = pek.id
  targetSubkegiatanName.value = sub ? `${sub.kode} - ${sub.nama}` : 'Subkegiatan Target'
  const targetOpdId = pek.id_sub_pd || selectedOpdDetail.value?.opd?.id_sub_pd
  fetchPersonelOptions(targetOpdId)
  fetchTaggingOptions()
  isPelaksanaanDropdownOpen.value = false
  isSumberDanaDropdownOpen.value = false
  sumberDanaSearchQuery.value = ''
  
  try {
    const res = await axios.get(`/api/v1/rko/pekerjaan/${pek.id}`)
    const d = res.data
    form.value = {
      id_sub_pd: d.id_sub_pd,
      id_subkegiatan: d.id_subkegiatan,
      tahun: d.tahun || selectedTahun.value,
      nomor_pekerjaan: d.nomor_pekerjaan || null,
      nama_pekerjaan: d.nama_pekerjaan || '',
      ket_pekerjaan: d.ket_pekerjaan || '',
      lokasi: d.lokasi || '',
      pagu_anggaran: d.pagu_anggaran || 0,
      volume: d.volume || null,
      satuan: d.satuan || '',
      nomor_rup: d.nomor_rup || '',
      jenis_paket: d.jenis_paket || 1,
      jenis_pengadaan: d.jenis_pengadaan || 1,
      tipe_swa: d.tipe_swa || null,
      penyelenggara_swa: d.penyelenggara_swa || '',
      metode: d.metode || null,
      awal_pelaksanaan: d.awal_pelaksanaan || null,
      akhir_pelaksanaan: d.akhir_pelaksanaan || null,
      pelaksanaan_bulan: derivePelaksanaanBulan(d),
      awal_pemilihan: d.awal_pemilihan || null,
      akhir_pemilihan: d.akhir_pemilihan || null,
      awal_kontrak: d.awal_kontrak || null,
      akhir_kontrak: d.akhir_kontrak || null,
      nama_ppk: d.nama_ppk || '',
      nama_pptk: d.nama_pptk || '',
      id_sumber_dana: d.id_sumber_dana || null,
      sumber_dana: d.sumber_dana || '',
      tags: d.tags || [],
      lokasi_list: d.lokasi_list || [],
      target_fisik: monthKeys.map(k => Number(d[k + '_f'] || 0)),
      target_keuangan: monthKeys.map(k => Number(d[k] || 0))
    }
  } catch (err) {
    form.value = {
      id_sub_pd: selectedOpdDetail.value?.opd?.id_sub_pd,
      id_subkegiatan: sub?.idsubkegiatan || '',
      tahun: selectedTahun.value,
      nomor_pekerjaan: pek.nomor_pekerjaan || null,
      nama_pekerjaan: pek.nama_pekerjaan || '',
      ket_pekerjaan: pek.ket_pekerjaan || '',
      lokasi: pek.lokasi || '',
      pagu_anggaran: pek.pagu_anggaran || 0,
      volume: pek.volume || null,
      satuan: pek.satuan || '',
      nomor_rup: pek.nomor_rup || '',
      jenis_paket: pek.jenis_paket || 1,
      jenis_pengadaan: pek.jenis_pengadaan || 1,
      tipe_swa: pek.tipe_swa || null,
      penyelenggara_swa: pek.penyelenggara_swa || '',
      metode: pek.metode || null,
      awal_pelaksanaan: pek.awal_pelaksanaan || null,
      akhir_pelaksanaan: pek.akhir_pelaksanaan || null,
      pelaksanaan_bulan: derivePelaksanaanBulan(pek),
      awal_pemilihan: pek.awal_pemilihan || null,
      akhir_pemilihan: pek.akhir_pemilihan || null,
      awal_kontrak: pek.awal_kontrak || null,
      akhir_kontrak: pek.akhir_kontrak || null,
      nama_ppk: pek.nama_ppk || '',
      nama_pptk: pek.nama_pptk || '',
      id_sumber_dana: pek.id_sumber_dana || null,
      sumber_dana: pek.sumber_dana || '',
      tags: pek.tags || [],
      lokasi_list: [],
      target_fisik: [...pek.target_fisik],
      target_keuangan: [...pek.target_keuangan]
    }
  }
  showModal.value = true
  initRkoMap()
}

const savePekerjaan = async () => {
  saving.value = true
  try {
    const payload = {
      id_sub_pd: form.value.id_sub_pd,
      id_subkegiatan: form.value.id_subkegiatan,
      tahun: form.value.tahun,
      nomor_pekerjaan: form.value.nomor_pekerjaan ? Number(form.value.nomor_pekerjaan) : null,
      nama_pekerjaan: form.value.nama_pekerjaan,
      ket_pekerjaan: form.value.ket_pekerjaan,
      lokasi: form.value.lokasi,
      pagu_anggaran: Number(form.value.pagu_anggaran),
      volume: form.value.volume ? Number(form.value.volume) : null,
      satuan: form.value.satuan,
      nomor_rup: form.value.nomor_rup,
      jenis_paket: Number(form.value.jenis_paket || 1),
      jenis_pengadaan: Number(form.value.jenis_pengadaan || 1),
      tipe_swa: form.value.tipe_swa ? Number(form.value.tipe_swa) : null,
      penyelenggara_swa: form.value.penyelenggara_swa,
      metode: form.value.metode ? Number(form.value.metode) : null,
      awal_pelaksanaan: form.value.awal_pelaksanaan ? Number(form.value.awal_pelaksanaan) : null,
      akhir_pelaksanaan: form.value.akhir_pelaksanaan ? Number(form.value.akhir_pelaksanaan) : null,
      pelaksanaan_bulan: form.value.pelaksanaan_bulan || [],
      awal_pemilihan: form.value.awal_pemilihan ? Number(form.value.awal_pemilihan) : null,
      akhir_pemilihan: form.value.akhir_pemilihan ? Number(form.value.akhir_pemilihan) : null,
      awal_kontrak: form.value.awal_kontrak ? Number(form.value.awal_kontrak) : null,
      akhir_kontrak: form.value.akhir_kontrak ? Number(form.value.akhir_kontrak) : null,
      nama_ppk: form.value.nama_ppk || null,
      nama_pptk: form.value.nama_pptk || null,
      id_sumber_dana: form.value.id_sumber_dana ? Number(form.value.id_sumber_dana) : null,
      sumber_dana: form.value.sumber_dana || null,
      tags: form.value.tags,
      lokasi_list: form.value.lokasi_list || []
    }

    monthKeys.forEach((k, idx) => {
      payload[k] = Number(form.value.target_keuangan[idx] || 0)
      payload[k + '_f'] = Number(form.value.target_fisik[idx] || 0)
    })

    if (isEditMode.value) {
      await axios.put(`/api/v1/rko/pekerjaan/${editingPekerjaanId.value}`, payload)
    } else {
      await axios.post('/api/v1/rko/pekerjaan', payload)
    }

    showModal.value = false
    notifySuccess(isEditMode.value ? 'Pekerjaan Berhasil Diperbarui!' : 'Paket Pekerjaan Berhasil Ditambah!')
    if (selectedOpdDetail.value?.opd) {
      openOpdDetail(selectedOpdDetail.value.opd)
    }
  } catch (err) {
    notifyError('Gagal Menyimpan Paket Pekerjaan', err.response?.data?.detail || err.message)
  } finally {
    saving.value = false
  }
}

const confirmDeletePekerjaan = (pek) => {
  pekerjaanToDelete.value = pek
  showDeleteModal.value = true
}

const executeDeletePekerjaan = async () => {
  if (!pekerjaanToDelete.value) return
  deleting.value = true
  try {
    await axios.delete(`/api/v1/rko/pekerjaan/${pekerjaanToDelete.value.id}`)
    showDeleteModal.value = false
    pekerjaanToDelete.value = null
    notifySuccess('Paket Pekerjaan Berhasil Dihapus!')
    if (selectedOpdDetail.value?.opd) {
      openOpdDetail(selectedOpdDetail.value.opd)
    }
  } catch (err) {
    notifyError('Gagal Menghapus Pekerjaan', err.response?.data?.detail || err.message)
  } finally {
    deleting.value = false
  }
}

const openSubmitModal = async () => {
  const idSubPd = selectedOpdDetail.value?.opd?.id_sub_pd
  if (!idSubPd) return
  
  showSubmitModal.value = true
  loadingValidation.value = true
  submitValidationData.value = null

  try {
    const res = await axios.get(`/api/v1/rko/validate-submit/${idSubPd}`, {
      params: { tahun: selectedTahun.value }
    })
    submitValidationData.value = res.data
  } catch (err) {
    console.warn('Gagal validasi submit RKO:', err)
  } finally {
    loadingValidation.value = false
  }
}

const doSubmitRko = async () => {
  const idSubPd = selectedOpdDetail.value?.opd?.id_sub_pd
  if (!idSubPd || !submitValidationData.value?.is_valid) return

  submittingRko.value = true
  try {
    await axios.post(`/api/v1/rko/submit/${idSubPd}`, null, {
      params: { tahun: selectedTahun.value }
    })
    showSubmitModal.value = false
    notifySuccess('RKO Berhasil Disubmit! 🎉', 'Data RKO OPD kini telah terkunci.')
    if (selectedOpdDetail.value?.opd) {
      openOpdDetail(selectedOpdDetail.value.opd)
    }
  } catch (err) {
    notifyError('Gagal Submit RKO', err.response?.data?.detail?.message || err.message)
  } finally {
    submittingRko.value = false
  }
}

const doApproveRko = async () => {
  const idSubPd = selectedOpdDetail.value?.opd?.id_sub_pd
  if (!idSubPd) return

  const isConfirmed = await confirmDialog({
    title: 'Setujui (Approve) RKO OPD?',
    text: 'Data RKO OPD ini akan disetujui resmi oleh Admin.',
    confirmButtonText: 'Ya, Setujui',
    icon: 'question'
  })
  if (!isConfirmed) return

  actionLoading.value = true
  try {
    await axios.post(`/api/v1/rko/approve/${idSubPd}`, null, {
      params: { tahun: selectedTahun.value }
    })
    notifySuccess('RKO Berhasil Disetujui (Approved)! 🎉')
    if (selectedOpdDetail.value?.opd) {
      openOpdDetail(selectedOpdDetail.value.opd)
    }
  } catch (err) {
    notifyError('Gagal Menyetujui RKO', err.response?.data?.detail || err.message)
  } finally {
    actionLoading.value = false
  }
}

const doRejectRko = async () => {
  const idSubPd = selectedOpdDetail.value?.opd?.id_sub_pd
  if (!idSubPd) return

  const notes = await promptDialog({
    title: 'Buka Kunci / Revisi RKO OPD',
    inputPlaceholder: 'Masukkan catatan pengembalian/revisi...',
    defaultValue: 'Dikembalikan oleh Admin untuk penyesuaian target/pagu.',
    confirmButtonText: 'Buka Kunci'
  })
  if (notes === null) return

  actionLoading.value = true
  try {
    await axios.post(`/api/v1/rko/reject/${idSubPd}`, { notes }, {
      params: { tahun: selectedTahun.value }
    })
    notifySuccess('Kuncian RKO Berhasil Dibuka! 🔓', 'Status dikembalikan ke DRAFT untuk revisi OPD.')
    if (selectedOpdDetail.value?.opd) {
      openOpdDetail(selectedOpdDetail.value.opd)
    }
  } catch (err) {
    notifyError('Gagal Membuka Kuncian RKO', err.response?.data?.detail || err.message)
  } finally {
    actionLoading.value = false
  }
}

onMounted(() => {
  fetchData()
  fetchTaggingOptions()
  fetchRefSumberDana()
})
</script>
