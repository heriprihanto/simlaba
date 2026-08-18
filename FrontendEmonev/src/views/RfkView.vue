<template>
  <div class="min-h-screen bg-slate-50 dark:bg-[#0b132b] text-slate-800 dark:text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6 transition-colors duration-200">
    
    <!-- Floating Toast Notification (Top Right, z-[100]) -->
    <Transition
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="toastShow" 
        class="fixed top-5 right-5 z-[100] max-w-sm w-full bg-slate-900 text-white rounded-2xl shadow-2xl border border-emerald-500/50 p-4 flex items-center justify-between space-x-3 backdrop-blur-md animate-in slide-in-from-top-3 duration-200"
      >
        <div class="flex items-center space-x-3 min-w-0">
          <div class="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
            <CheckCircle2 class="w-5 h-5" />
          </div>
          <div class="min-w-0">
            <p class="font-extrabold text-[10px] text-emerald-400 uppercase tracking-widest">Sukses</p>
            <p class="font-bold text-xs text-slate-100 leading-snug truncate" :title="toastMessage">{{ toastMessage }}</p>
          </div>
        </div>
        <button 
          @click="toastShow = false" 
          class="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors shrink-0 cursor-pointer"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </Transition>

    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white dark:bg-[#141d30] p-6 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-xl shadow-slate-200/50 dark:shadow-none">
      <div class="space-y-1">
        <div class="flex items-center space-x-2.5">
          <div class="p-2.5 rounded-2xl bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4]">
            <TrendingUp class="w-6 h-6" />
          </div>
          <div>
            <h1 class="text-xl sm:text-2xl font-black tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
              Realisasi Fisik &amp; Keuangan (RFK)
              <span class="text-xs font-extrabold px-2.5 py-0.5 rounded-full bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]">
                Tahun {{ selectedTahun }}
              </span>
            </h1>
            <!-- 
            <p class="text-xs sm:text-sm font-semibold text-slate-500 dark:text-slate-400">
              Rekapitulasi status pengiriman laporan RFK bulanan seluruh Perangkat Daerah Kota Tegal
            </p>
            -->
          </div>
        </div>
      </div>

      <!-- Action Buttons & Year Picker -->
      <div class="flex items-center space-x-3">
        <div class="flex items-center bg-slate-100 dark:bg-slate-800/80 p-1.5 rounded-2xl border border-slate-200 dark:border-slate-700">
          <Calendar class="w-4 h-4 text-slate-400 ml-2 mr-1" />
          <select 
            v-model="selectedTahun" 
            @change="fetchRfkData"
            class="bg-transparent text-xs font-black text-slate-800 dark:text-slate-200 px-2 py-1 focus:outline-none cursor-pointer"
          >
            <option :value="2026">Tahun 2026</option>
            <option :value="2025">Tahun 2025</option>
          </select>
        </div>

        <button 
          @click="fetchRfkData" 
          :disabled="loading"
          class="p-2.5 rounded-2xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold transition-all cursor-pointer flex items-center space-x-1.5 text-xs shadow-xs"
          title="Refresh Data"
        >
          <RotateCw class="w-4 h-4" :class="loading ? 'animate-spin text-[#308e87]' : ''" />
          <span class="hidden sm:inline">Refresh</span>
        </button>
      </div>
    </div>

    <!-- Navigation Breadcrumb -->
    <div class="flex items-center space-x-2 text-xs font-bold text-slate-500 bg-white dark:bg-[#141d30] px-5 py-3 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-xs overflow-x-auto">
      <button 
        @click="navigateToView('opd_list')"
        class="flex items-center space-x-1.5 hover:text-[#308e87] cursor-pointer transition-colors shrink-0"
        :class="currentView === 'opd_list' ? 'text-[#308e87] font-black' : ''"
      >
        <Building2 class="w-4 h-4" />
        <span>Daftar OPD</span>
      </button>

      <template v-if="currentView === 'opd_months' || currentView === 'month_detail'">
        <ChevronRight class="w-4 h-4 text-slate-400 shrink-0" />
        <button 
          @click="navigateToView('opd_months')"
          class="flex items-center space-x-1.5 hover:text-[#308e87] cursor-pointer transition-colors shrink-0"
          :class="currentView === 'opd_months' ? 'text-[#308e87] font-black' : ''"
        >
          <span>{{ selectedOpdModal?.nama_pd || 'Perangkat Daerah' }}</span>
        </button>
      </template>

      <template v-if="currentView === 'month_detail'">
        <ChevronRight class="w-4 h-4 text-slate-400 shrink-0" />
        <span class="text-[#308e87] font-black flex items-center space-x-1 shrink-0">
          <Calendar class="w-3.5 h-3.5" />
          <span>Laporan Bulan {{ monthNames[(selectedMonthDetail?.bulan || 1) - 1] }} {{ selectedTahun }}</span>
        </span>
      </template>
    </div>

    <!-- ========================================================================= -->
    <!-- LEVEL 1: DAFTAR OPD MAIN TABLE VIEW -->
    <!-- ========================================================================= -->
    <template v-if="currentView === 'opd_list'">
      <!-- Summary KPI Cards -->
      <!--  
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white dark:bg-[#141d30] p-5 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-md space-y-1">
          <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span class="text-xs font-bold uppercase tracking-wider">Total Perangkat Daerah</span>
            <Building2 class="w-4 h-4 text-[#308e87]" />
          </div>
          <div class="text-2xl font-black text-slate-900 dark:text-white">
            {{ summary.total_opd || 0 }}
          </div>
          <p class="text-[11px] font-semibold text-slate-400">Perangkat Daerah terdaftar aktif</p>
        </div>

        <div class="bg-white dark:bg-[#141d30] p-5 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-md space-y-1">
          <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span class="text-xs font-bold uppercase tracking-wider">Total Laporan Terkirim</span>
            <Send class="w-4 h-4 text-emerald-500" />
          </div>
          <div class="text-2xl font-black text-emerald-600 dark:text-emerald-400">
            {{ summary.total_laporan_terkirim || 0 }}
          </div>
          <p class="text-[11px] font-semibold text-slate-400">Akumulasi seluruh bulan</p>
        </div>

        <div class="bg-white dark:bg-[#141d30] p-5 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-md space-y-1">
          <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span class="text-xs font-bold uppercase tracking-wider">Rata-rata Terkirim / Bulan</span>
            <CheckCircle2 class="w-4 h-4 text-cyan-500" />
          </div>
          <div class="text-2xl font-black text-cyan-600 dark:text-cyan-400">
            {{ formatAveragePerMonth }}
          </div>
          <p class="text-[11px] font-semibold text-slate-400">Laporan terkirim tiap bulan</p>
        </div>

        <div class="bg-white dark:bg-[#141d30] p-5 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-md space-y-1">
          <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">
            <span class="text-xs font-bold uppercase tracking-wider">Bulan Terbanyak Kirim</span>
            <CalendarCheck class="w-4 h-4 text-indigo-500" />
          </div>
          <div class="text-2xl font-black text-indigo-600 dark:text-indigo-400">
            {{ highestReportingMonth.name }}
          </div>
          <p class="text-[11px] font-semibold text-slate-400">{{ highestReportingMonth.count }} OPD telah mengirim</p>
        </div>
      </div>
      -->

      <!-- Filter & Search Toolbar -->
      <div class="bg-white dark:bg-[#141d30] p-4 sm:p-5 rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-xl space-y-4">
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <!-- Category Tabs -->
           <!--
          <div class="flex items-center p-1 bg-slate-100 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700/60">
            <button 
              @click="opdFilterCategory = 'all'"
              class="px-4 py-1.5 rounded-xl text-xs font-black transition-all cursor-pointer"
              :class="opdFilterCategory === 'all' ? 'bg-white dark:bg-[#308e87] text-[#308e87] dark:text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
            >
              Semua OPD ({{ opdList.length }})
            </button>
            <button 
              @click="opdFilterCategory = 'main'"
              class="px-4 py-1.5 rounded-xl text-xs font-black transition-all cursor-pointer"
              :class="opdFilterCategory === 'main' ? 'bg-white dark:bg-[#308e87] text-[#308e87] dark:text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
            >
              Dinas Utama ({{ countMainOpd }})
            </button>
            <button 
              @click="opdFilterCategory = 'sub'"
              class="px-4 py-1.5 rounded-xl text-xs font-black transition-all cursor-pointer"
              :class="opdFilterCategory === 'sub' ? 'bg-white dark:bg-[#308e87] text-[#308e87] dark:text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
            >
              Sub Unit / Puskesmas ({{ countSubOpd }})
            </button>
          </div>
          -->
          <!-- Search input -->
          <div class="relative flex-1 max-w-md">
            <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Cari kode atau nama Perangkat Daerah..." 
              class="w-full pl-10 pr-9 py-2 rounded-2xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-[#308e87] transition-all"
            />
            <button 
              v-if="searchQuery" 
              @click="searchQuery = ''"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 cursor-pointer"
            >
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      <!-- Main OPD Table -->
      <div class="bg-white dark:bg-[#141d30] rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <!-- Header Row 1 -->
              <tr class="bg-slate-100/90 dark:bg-[#18233a] text-slate-700 dark:text-slate-200 text-xs font-black uppercase tracking-wider border-b border-slate-200 dark:border-slate-800">
                <th rowspan="2" class="p-3.5 w-48 border-r border-slate-200 dark:border-slate-800/60 sticky left-0 bg-slate-100/95 dark:bg-[#18233a]/95 z-10 shadow-xs">
                  Kode OPD
                </th>
                <th rowspan="2" class="p-3.5 w-80 border-r border-slate-200 dark:border-slate-800/60 sticky left-48 bg-slate-100/95 dark:bg-[#18233a]/95 z-10 shadow-xs">
                  Nama OPD
                </th>
                <th colspan="12" class="p-2.5 text-center bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-extrabold border-b border-slate-200 dark:border-slate-800">
                  Laporan Bulanan
                </th>
              </tr>
              <!-- Header Row 2: Months -->
              <tr class="bg-slate-100/90 dark:bg-[#18233a] text-slate-700 dark:text-slate-300 text-[11px] font-black text-center border-b border-slate-200 dark:border-slate-800">
                <th v-for="(mName, idx) in monthShorts" :key="idx" class="p-2 w-20 border-r border-slate-200/60 dark:border-slate-800/60 last:border-r-0">
                  {{ mName }}
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-200 dark:divide-slate-800/60 text-xs">
              <template v-if="loading">
                <tr>
                  <td colspan="14" class="p-12 text-center text-slate-400">
                    <div class="flex flex-col items-center space-y-2">
                      <Loader2 class="w-8 h-8 animate-spin text-[#308e87]" />
                      <span class="font-bold text-xs">Memuat daftar laporan RFK OPD...</span>
                    </div>
                  </td>
                </tr>
              </template>

              <template v-else-if="filteredOpdList.length === 0">
                <tr>
                  <td colspan="14" class="p-12 text-center text-slate-400">
                    <FileX class="w-10 h-10 mx-auto text-slate-300 dark:text-slate-700 mb-2" />
                    <p class="font-bold text-xs">Tidak ada data Perangkat Daerah ditemukan.</p>
                  </td>
                </tr>
              </template>

              <template v-else>
                <tr 
                  v-for="opd in filteredOpdList" 
                  :key="opd.id_sub_pd"
                  class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group"
                >
                  <!-- Kode OPD Column (Sticky) -->
                  <td class="p-3 font-mono font-extrabold text-[#308e87] dark:text-[#3aada4] border-r border-slate-200 dark:border-slate-800/60 sticky left-0 bg-white dark:bg-[#141d30] group-hover:bg-slate-50 dark:group-hover:bg-[#1a263d] z-10">
                    {{ opd.kode }}
                  </td>

                  <!-- Nama OPD Column (Clickable -> Opens Level 2 OPD Months View) -->
                  <td 
                    @click="selectOpdAndShowMonths(opd)"
                    class="p-3 font-bold text-slate-900 dark:text-white border-r border-slate-200 dark:border-slate-800/60 sticky left-48 bg-white dark:bg-[#141d30] group-hover:bg-slate-50 dark:group-hover:bg-[#1a263d] z-10 cursor-pointer hover:text-[#308e87] dark:hover:text-[#3aada4] transition-colors"
                    title="Klik nama OPD untuk melihat daftar tabel bulan"
                  >
                    <div class="flex flex-col space-y-0.5">
                      <span class="leading-snug hover:underline flex items-center justify-between">
                        <span>{{ opd.nama_pd }}</span>
                      </span>
                      <span v-if="opd.nama_pd_singkat" class="text-[10px] font-semibold text-slate-400 dark:text-slate-500">
                        ({{ opd.nama_pd_singkat }})
                      </span>
                    </div>
                  </td>

                  <!-- 12 Month Columns -->
                  <td 
                    v-for="m in 12" 
                    :key="'m-' + m" 
                    class="p-1.5 text-center border-r border-slate-200/60 dark:border-slate-800/60 last:border-r-0 align-middle"
                  >
                    <template v-if="opd.laporan_bulanan[m]">
                      <div 
                        v-if="opd.laporan_bulanan[m].tgl_kirim_fmt"
                        @click="selectOpdAndShowMonths(opd)"
                        class="px-1.5 py-1 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-800 dark:text-emerald-300 font-bold border border-emerald-500/30 transition-all duration-200 cursor-pointer flex flex-col items-center justify-center space-y-0.5 shadow-xs hover:scale-105"
                        :title="`Klik untuk membuka tabel bulan OPD ${opd.nama_pd}`"
                      >
                        <div class="flex items-center space-x-1 font-mono text-[11px] leading-none">
                          <CheckCircle2 class="w-3 h-3 text-emerald-600 dark:text-emerald-400 shrink-0" />
                          <span class="whitespace-nowrap">{{ opd.laporan_bulanan[m].tgl_kirim_fmt }}</span>
                        </div>
                      </div>

                      <div 
                        v-else
                        @click="selectOpdAndShowMonths(opd)"
                        class="px-1.5 py-0.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-amber-300 font-semibold text-[10px] border border-amber-500/20 transition-all duration-200 cursor-pointer text-center hover:scale-105"
                        title="Draft (Belum Kirim). Klik untuk membuka tabel bulan OPD"
                      >
                        Draft
                      </div>
                    </template>

                    <span v-else class="text-slate-300 dark:text-slate-700 font-bold text-xs">-</span>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </template>


    <!-- ========================================================================= -->
    <!-- LEVEL 2: TABEL BULAN OPD VIEW (Embedded Page View, NOT a modal) -->
    <!-- ========================================================================= -->
    <template v-else-if="currentView === 'opd_months' && selectedOpdModal">
      <div class="bg-white dark:bg-[#141d30] rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-xl p-6 space-y-6">
        
        <!-- Header Bar Level 2 -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div class="space-y-1">
            <div class="flex items-center space-x-2">
              <span class="px-2.5 py-1 rounded-xl bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] font-mono font-black text-xs">
                Kode: {{ selectedOpdModal.kode }}
              </span>
              <span 
                v-if="selectedOpdModal.status_rko" 
                class="px-2.5 py-1 rounded-xl text-xs font-black uppercase tracking-wider"
                :class="selectedOpdModal.status_rko === 'APPROVED' ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30'"
              >
                RKO: {{ selectedOpdModal.status_rko }}
              </span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">
              {{ selectedOpdModal.nama_pd }}
            </h2>
            <p class="text-xs font-semibold text-slate-400">
              Daftar Laporan RFK Bulanan yang telah dibuat untuk Perangkat Daerah ini
            </p>
          </div>

          <div class="flex items-center space-x-3">
            <button 
              @click="navigateToView('opd_list')"
              class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold text-xs transition-colors cursor-pointer flex items-center space-x-1.5"
            >
              <ChevronLeft class="w-4 h-4" />
              <span>Kembali ke Daftar OPD</span>
            </button>

            <button 
              @click="handleBuatLaporan(selectedOpdModal)"
              :disabled="creatingLaporan"
              class="px-4 py-2 rounded-xl bg-[#308e87] hover:bg-[#25736d] text-white font-black text-xs transition-all cursor-pointer flex items-center space-x-1.5 shadow-md active:scale-95 disabled:opacity-50"
              :title="`Buat Draf Laporan RFK Bulan ${monthNames[(selectedOpdModal.max_created_bulan || 0)] || 'Januari'}`"
            >
              <Loader2 v-if="creatingLaporan" class="w-4 h-4 animate-spin" />
              <Plus v-else class="w-4 h-4" />
              <span>Buat Laporan RFK</span>
            </button>
          </div>
        </div>

        <!-- Alert Error Banner -->
        <div 
          v-if="errorMessage" 
          class="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-800 dark:text-rose-200 text-xs font-extrabold flex items-start space-x-2.5 shadow-xs animate-in fade-in"
        >
          <AlertCircle class="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
          <div class="flex-1 leading-relaxed">
            {{ errorMessage }}
          </div>
          <button @click="errorMessage = ''" class="text-rose-500 hover:text-rose-700">
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- Alert Success Banner -->
        <div 
          v-if="successMessage" 
          class="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-800 dark:text-emerald-200 text-xs font-extrabold flex items-start space-x-2.5 shadow-xs animate-in fade-in"
        >
          <CheckCircle2 class="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
          <div class="flex-1 leading-relaxed">
            {{ successMessage }}
          </div>
          <button @click="successMessage = ''" class="text-emerald-500 hover:text-emerald-700">
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- OPD Monthly Table (Limited to created months, DESC order) -->
        <div 
          v-if="selectedOpdModal.max_created_bulan > 0"
          class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-xs"
        >
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-100/90 dark:bg-[#18233a] text-slate-700 dark:text-slate-200 font-black uppercase text-[11px] border-b border-slate-200 dark:border-slate-800">
                <th class="py-3.5 px-3 w-12 text-center border-r border-slate-200 dark:border-slate-800">No</th>
                <th class="py-3.5 px-4 w-36 border-r border-slate-200 dark:border-slate-800">Bulan</th>
                <th class="py-3.5 px-4 border-r border-slate-200 dark:border-slate-800">Tanggal Buat</th>
                <th class="py-3.5 px-4 border-r border-slate-200 dark:border-slate-800">Tanggal Kirim</th>
                <th class="py-3.5 px-4 border-r border-slate-200 dark:border-slate-800">Tanggal Verifikasi</th>
                
                <!-- Aksi (Khusus Admin) -->
                <th v-if="isAdmin" class="py-3.5 px-3 text-center w-20">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 font-semibold">
              <tr 
                v-for="m in getCreatedMonthsDesc(selectedOpdModal.max_created_bulan)" 
                :key="'opd-modal-m-' + m"
                @click="selectMonthAndShowDetail(selectedOpdModal, m)"
                class="hover:bg-[#308e87]/10 dark:hover:bg-slate-800/80 transition-colors cursor-pointer group"
                title="Klik item bulan ini untuk melihat Data RFK rincian"
              >
                <!-- No -->
                <td class="py-3 px-3 text-center font-bold text-slate-400 border-r border-slate-100 dark:border-slate-800/60 group-hover:text-[#308e87]">
                  {{ m }}
                </td>

                <!-- Bulan -->
                <td class="py-3 px-4 font-black text-slate-900 dark:text-white border-r border-slate-100 dark:border-slate-800/60 group-hover:text-[#308e87]">
                  <div class="flex items-center space-x-2">
                    <Calendar class="w-4 h-4 text-[#308e87] shrink-0" />
                    <span>{{ monthNames[m - 1] }}</span>
                  </div>
                </td>
                
                <!-- Tanggal Buat -->
                <td class="py-3 px-4 font-mono text-slate-600 dark:text-slate-300 border-r border-slate-100 dark:border-slate-800/60">
                  <template v-if="selectedOpdModal.laporan_bulanan[m]?.tgl_buat_fmt">
                    <div class="flex flex-col space-y-0.5">
                      <span class="font-bold">{{ selectedOpdModal.laporan_bulanan[m].tgl_buat_fmt }}</span>
                      <span v-if="selectedOpdModal.laporan_bulanan[m].user_buat" class="text-[10px] font-sans font-bold text-slate-400 dark:text-slate-500">
                        Oleh: {{ selectedOpdModal.laporan_bulanan[m].user_buat }}
                      </span>
                    </div>
                  </template>
                  <span v-else class="text-slate-400 font-bold">-</span>
                </td>

                <!-- Tanggal Kirim -->
                <td class="py-3 px-4 font-mono border-r border-slate-100 dark:border-slate-800/60">
                  <template v-if="selectedOpdModal.laporan_bulanan[m]?.tgl_kirim_full">
                    <div class="flex flex-col space-y-0.5">
                      <span class="text-emerald-700 dark:text-emerald-400 font-bold flex items-center space-x-1">
                        <CheckCircle2 class="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                        <span>{{ selectedOpdModal.laporan_bulanan[m].tgl_kirim_full }}</span>
                      </span>
                      <span v-if="selectedOpdModal.laporan_bulanan[m].user_kirim" class="text-[10px] font-sans font-bold text-emerald-600/80 dark:text-emerald-400/80">
                        Oleh: {{ selectedOpdModal.laporan_bulanan[m].user_kirim }}
                      </span>
                    </div>
                  </template>
                  <span v-else-if="selectedOpdModal.laporan_bulanan[m]?.tgl_buat_fmt" class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-700 dark:text-amber-300 text-[10px] font-bold inline-block">
                    Draft (Belum Kirim)
                  </span>
                  <span v-else class="text-slate-400 font-bold">-</span>
                </td>

                <!-- Tanggal Verifikasi -->
                <td class="py-3 px-4 font-mono" :class="isAdmin ? 'border-r border-slate-100 dark:border-slate-800/60' : ''">
                  <template v-if="selectedOpdModal.laporan_bulanan[m]?.tgl_verify_fmt">
                    <div class="flex flex-col space-y-0.5">
                      <span class="text-cyan-700 dark:text-cyan-400 font-bold flex items-center space-x-1">
                        <CheckCircle2 class="w-3.5 h-3.5 text-cyan-500 shrink-0" />
                        <span>{{ selectedOpdModal.laporan_bulanan[m].tgl_verify_fmt }}</span>
                      </span>
                      <span v-if="selectedOpdModal.laporan_bulanan[m].user_verify" class="text-[10px] font-sans font-bold text-cyan-600/80 dark:text-cyan-400/80">
                        Oleh: {{ selectedOpdModal.laporan_bulanan[m].user_verify }}
                      </span>
                    </div>
                  </template>
                  <span v-else-if="selectedOpdModal.laporan_bulanan[m]?.tgl_kirim_full" class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-700 dark:text-amber-300 text-[10px] font-bold inline-block">
                    Belum Verifikasi
                  </span>
                  <span v-else class="text-slate-400 font-bold">-</span>
                </td>

                <!-- Tombol Hapus (Khusus Admin, hanya aktif untuk bulan terbaru) -->
                <td v-if="isAdmin" class="py-3 px-3 text-center" @click.stop>
                  <button 
                    v-if="m === selectedOpdModal.max_created_bulan"
                    @click.stop="confirmDeleteLaporan(selectedOpdModal, m)"
                    :disabled="deletingBulan === m"
                    class="p-1.5 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-600 dark:text-rose-400 font-bold transition-all cursor-pointer inline-flex items-center justify-center border border-rose-500/20 hover:scale-105 active:scale-95 disabled:opacity-50"
                    title="Hapus Laporan RFK bulan terbaru ini (Khusus Admin)"
                  >
                    <Loader2 v-if="deletingBulan === m" class="w-4 h-4 animate-spin text-rose-500" />
                    <Trash2 v-else class="w-4 h-4" />
                  </button>
                  <button 
                    v-else
                    disabled
                    class="p-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-300 dark:text-slate-600 font-bold cursor-not-allowed inline-flex items-center justify-center border border-slate-200 dark:border-slate-700 opacity-60"
                    :title="`Hanya Laporan RFK Bulan ${monthNames[selectedOpdModal.max_created_bulan - 1]} (bulan terbaru) yang dapat dihapus terlebih dahulu`"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State if no reports created yet -->
        <div v-else class="p-12 text-center bg-slate-50 dark:bg-slate-900/50 rounded-2xl border border-dashed border-slate-300 dark:border-slate-800 space-y-3">
          <FileX class="w-12 h-12 mx-auto text-slate-400" />
          <p class="font-bold text-xs text-slate-500">Belum ada Laporan RFK yang dibuat untuk Perangkat Daerah ini.</p>
          <button 
            @click="handleBuatLaporan(selectedOpdModal)"
            :disabled="creatingLaporan"
            class="px-4 py-2 rounded-xl bg-[#308e87] hover:bg-[#25736d] text-white font-black text-xs transition-all cursor-pointer inline-flex items-center space-x-1.5 shadow-md active:scale-95"
          >
            <Plus class="w-4 h-4" />
            <span>Buat Laporan RFK Pertama (Januari)</span>
          </button>
        </div>

      </div>
    </template>


    <!-- ========================================================================= -->
    <!-- LEVEL 3: DATA RFK BULAN TREEVIEW VIEW (Embedded Page View, NOT a modal) -->
    <!-- ========================================================================= -->
    <template v-else-if="currentView === 'month_detail' && selectedMonthDetail">
      <div class="bg-white dark:bg-[#141d30] rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-xl p-6 space-y-6">
        
        <!-- Header Bar Level 3 -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div class="space-y-1">
            <div class="flex items-center space-x-2 text-xs font-black text-[#308e87]">
              <Calendar class="w-4 h-4" />
              <span>Data RFK Bulan {{ monthNames[selectedMonthDetail.bulan - 1] }} {{ selectedTahun }}</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">
              {{ selectedMonthDetail.opd.nama_pd }}
            </h2>
            <p class="text-xs font-mono font-bold text-slate-400">Kode OPD: {{ selectedMonthDetail.opd.kode }}</p>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <button 
              @click="toggleAllMonthDetailNodes(true)"
              class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-xs cursor-pointer transition-colors"
            >
              + Expand Semua
            </button>
            <button 
              @click="toggleAllMonthDetailNodes(false)"
              class="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-xs cursor-pointer transition-colors"
            >
              - Collapse Semua
            </button>
            <button 
              @click="navigateToView('opd_months')"
              class="px-4 py-2 rounded-xl bg-[#308e87] hover:bg-[#25736d] text-white font-bold text-xs transition-colors cursor-pointer flex items-center space-x-1.5 shadow-xs"
            >
              <ChevronLeft class="w-4 h-4" />
              <span>Kembali ke Tabel Bulan</span>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loadingMonthDetail" class="py-24 text-center">
          <Loader2 class="w-10 h-10 animate-spin mx-auto mb-3 text-[#308e87]" />
          <span class="font-bold text-xs text-slate-400">Memuat rincian Data RFK Bulan {{ monthNames[selectedMonthDetail.bulan - 1] }}...</span>
        </div>

        <!-- Treeview Table Grid -->
        <div v-else-if="selectedMonthDetail.data?.programs?.length > 0" class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-xs">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse min-w-[1400px]">
              <thead>
                <!-- Header Row 1 -->
                <tr class="bg-[#308e87]/15 dark:bg-[#18233a] text-slate-800 dark:text-slate-200 font-black uppercase text-[11px] text-center border-b border-slate-200 dark:border-slate-800">
                  <th rowspan="2" class="py-3.5 px-4 text-left border-r border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-0 bg-[#308e87]/20 dark:bg-[#18233a] z-20 shadow-xs">
                    Program > Kegiatan > Sub kegiatan > Pekerjaan
                  </th>
                  <th rowspan="2" class="py-3.5 px-3 text-right border-r border-slate-200 dark:border-slate-800 min-w-[140px]">
                    Anggaran
                  </th>
                  <th rowspan="2" class="py-3.5 px-2 text-center border-r border-slate-200 dark:border-slate-800 min-w-[100px] bg-emerald-500/10 text-emerald-700 dark:text-emerald-300">
                    Realisasi Fisik
                  </th>
                  <th colspan="3" class="py-2.5 px-3 text-center border-r border-slate-200 dark:border-slate-800 bg-blue-500/10 text-blue-700 dark:text-blue-300">
                    Realisasi Keuangan
                  </th>
                  <th colspan="12" class="py-2.5 px-2 text-center bg-indigo-500/10 text-indigo-700 dark:text-indigo-300">
                    Realisasi Keuangan Per Bulan
                  </th>
                </tr>

                <!-- Header Row 2 -->
                <tr class="bg-slate-100/90 dark:bg-[#18233a] text-slate-700 dark:text-slate-300 font-black text-[10px] text-center border-b-2 border-slate-200 dark:border-slate-800">
                  <th class="py-2 px-2 border-r border-slate-200 dark:border-slate-800 min-w-[130px] bg-blue-500/5">Bulan Ini</th>
                  <th class="py-2 px-2 border-r border-slate-200 dark:border-slate-800 min-w-[130px] bg-blue-500/5">Total Sampai Bulan Ini</th>
                  <th class="py-2 px-2 border-r border-slate-200 dark:border-slate-800 min-w-[130px] bg-blue-500/5">Total (SIPD)</th>
                  
                  <th v-for="m in monthShorts" :key="'rk-bln-' + m" class="py-1.5 px-1 border-r border-slate-200 dark:border-slate-800/60 w-24 bg-indigo-500/5 last:border-r-0">
                    {{ m }}
                  </th>
                </tr>
              </thead>

              <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
                
                <!-- LOOP PROGRAM -->
                <template v-for="prog in selectedMonthDetail.data.programs" :key="'m-prog-' + prog.kode">
                  <tr 
                    @click="toggleMonthDetailNode('prog-' + prog.kode)"
                    class="bg-slate-100/80 dark:bg-slate-800/80 hover:bg-slate-200/60 dark:hover:bg-slate-800 transition-colors cursor-pointer group font-extrabold text-slate-900 dark:text-white"
                  >
                    <!-- Uraian Program (Sticky Left 0) -->
                    <td class="py-3 px-4 border-r border-b border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-0 bg-slate-100 dark:bg-[#141d30] z-20">
                      <div class="flex items-center space-x-2 min-w-0 max-w-[330px]">
                        <ChevronRight 
                          class="w-4 h-4 text-[#308e87] transition-transform duration-200 shrink-0" 
                          :class="monthDetailExpandedNodes['prog-' + prog.kode] ? 'rotate-90' : ''" 
                        />
                        <Folder class="w-4 h-4 text-[#308e87] shrink-0" />
                        <span class="px-1.5 py-0.5 rounded font-mono font-black text-[10px] bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] shrink-0">
                          {{ prog.kode }}
                        </span>
                        <span class="font-black text-xs leading-snug group-hover:text-[#308e87] transition-colors truncate">
                          {{ prog.nama }}
                        </span>
                      </div>
                    </td>

                    <td class="py-3 px-3 text-right font-black border-r border-b border-slate-200 dark:border-slate-800">
                      {{ formatRupiah(prog.anggaran) }}
                    </td>

                    <td class="py-3 px-2 text-center font-black text-emerald-700 dark:text-emerald-400 border-r border-b border-slate-200 dark:border-slate-800 bg-emerald-500/[0.03]">
                      {{ formatPercent(prog.realisasi_fisik) }}
                    </td>

                    <td class="py-3 px-2 text-right font-black text-blue-700 dark:text-blue-400 border-r border-b border-slate-200 dark:border-slate-800 bg-blue-500/[0.03]">
                      {{ formatRupiah(prog.keuangan_bulan_ini) }}
                    </td>

                    <td class="py-3 px-2 text-right font-black text-blue-800 dark:text-blue-300 border-r border-b border-slate-200 dark:border-slate-800 bg-blue-500/[0.03]">
                      {{ formatRupiah(prog.keuangan_total_sd_bulan_ini) }}
                    </td>

                    <td class="py-3 px-2 text-right font-black text-indigo-700 dark:text-indigo-400 border-r border-b border-slate-200 dark:border-slate-800 bg-indigo-500/[0.03]">
                      {{ formatRupiah(prog.keuangan_total_sipd) }}
                    </td>

                    <td v-for="(v, mIdx) in prog.keuangan_per_bulan" :key="'prog-rkb-' + mIdx" class="py-2 px-2 text-right font-bold text-[11px] border-r border-slate-150 dark:border-slate-800/50 bg-indigo-500/[0.02]">
                      {{ v > 0 ? formatRupiah(v) : '-' }}
                    </td>
                  </tr>

                  <!-- LOOP KEGIATAN -->
                  <template v-if="monthDetailExpandedNodes['prog-' + prog.kode]" v-for="keg in prog.kegiatan" :key="'m-keg-' + keg.kode">
                    <tr 
                      @click="toggleMonthDetailNode('keg-' + keg.kode)"
                      class="bg-blue-50/40 dark:bg-blue-950/20 hover:bg-blue-50/70 dark:hover:bg-blue-950/30 transition-colors cursor-pointer group"
                    >
                      <td class="py-2.5 px-4 pl-9 border-r border-b border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-0 bg-blue-50/40 dark:bg-[#141d30] z-20">
                        <div class="flex items-center space-x-2 min-w-0 max-w-[310px]">
                          <ChevronRight 
                            class="w-3.5 h-3.5 text-blue-500 transition-transform duration-200 shrink-0" 
                            :class="monthDetailExpandedNodes['keg-' + keg.kode] ? 'rotate-90' : ''" 
                          />
                          <Layers class="w-3.5 h-3.5 text-blue-500 shrink-0" />
                          <span class="px-1.5 py-0.5 rounded font-mono font-black text-[9px] bg-blue-500/10 text-blue-600 dark:text-blue-400 shrink-0">
                            {{ keg.kode }}
                          </span>
                          <span class="font-bold text-slate-800 dark:text-slate-200 text-xs leading-snug group-hover:text-blue-600 transition-colors truncate">
                            {{ keg.nama }}
                          </span>
                        </div>
                      </td>

                      <td class="py-2.5 px-3 text-right font-bold text-slate-800 dark:text-slate-200 border-r border-b border-slate-200 dark:border-slate-800">
                        {{ formatRupiah(keg.anggaran) }}
                      </td>

                      <td class="py-2.5 px-2 text-center font-bold text-emerald-600 dark:text-emerald-400 border-r border-b border-slate-200 dark:border-slate-800">
                        {{ formatPercent(keg.realisasi_fisik) }}
                      </td>

                      <td class="py-2.5 px-2 text-right font-bold text-blue-600 dark:text-blue-400 border-r border-b border-slate-200 dark:border-slate-800">
                        {{ formatRupiah(keg.keuangan_bulan_ini) }}
                      </td>

                      <td class="py-2.5 px-2 text-right font-bold text-blue-700 dark:text-blue-300 border-r border-b border-slate-200 dark:border-slate-800">
                        {{ formatRupiah(keg.keuangan_total_sd_bulan_ini) }}
                      </td>

                      <td class="py-2.5 px-2 text-right font-bold text-indigo-600 dark:text-indigo-400 border-r border-b border-slate-200 dark:border-slate-800">
                        {{ formatRupiah(keg.keuangan_total_sipd) }}
                      </td>

                      <td v-for="(v, mIdx) in keg.keuangan_per_bulan" :key="'keg-rkb-' + mIdx" class="py-2 px-2 text-right font-medium text-[10px] border-r border-slate-150 dark:border-slate-800/50">
                        {{ v > 0 ? formatRupiah(v) : '-' }}
                      </td>
                    </tr>

                    <!-- LOOP SUBKEGIATAN -->
                    <template v-if="monthDetailExpandedNodes['keg-' + keg.kode]" v-for="sub in keg.subkegiatan" :key="'m-sub-' + sub.kode">
                      <tr 
                        @click="toggleMonthDetailNode('sub-' + sub.kode)"
                        class="bg-emerald-50/40 dark:bg-emerald-950/20 hover:bg-emerald-50/60 dark:hover:bg-emerald-950/30 transition-colors cursor-pointer group"
                      >
                        <td class="py-2.5 px-4 pl-14 border-r border-b border-slate-200 dark:border-slate-800 w-[360px] max-w-[360px] sticky left-0 bg-emerald-50/40 dark:bg-[#141d30] z-20">
                          <div class="flex items-center space-x-2 min-w-0 max-w-[290px]">
                            <ChevronRight 
                              class="w-3.5 h-3.5 text-emerald-600 transition-transform duration-200 shrink-0" 
                              :class="monthDetailExpandedNodes['sub-' + sub.kode] ? 'rotate-90' : ''" 
                            />
                            <span class="px-1.5 py-0.5 rounded font-mono font-black text-[9px] bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 shrink-0">
                              {{ sub.kode }}
                            </span>
                            <span class="font-bold text-slate-800 dark:text-slate-200 text-xs leading-snug group-hover:text-emerald-600 transition-colors truncate">
                              {{ sub.nama }}
                            </span>
                          </div>
                        </td>

                        <td class="py-2.5 px-3 text-right font-black text-emerald-700 dark:text-emerald-400 border-r border-b border-slate-200 dark:border-slate-800">
                          {{ formatRupiah(sub.anggaran) }}
                        </td>

                        <td class="py-2.5 px-2 text-center font-bold text-emerald-700 dark:text-emerald-400 border-r border-b border-slate-200 dark:border-slate-800">
                          {{ formatPercent(sub.realisasi_fisik) }}
                        </td>

                        <td class="py-2.5 px-2 text-right font-bold text-blue-700 dark:text-blue-400 border-r border-b border-slate-200 dark:border-slate-800">
                          {{ formatRupiah(sub.keuangan_bulan_ini) }}
                        </td>

                        <td class="py-2.5 px-2 text-right font-bold text-blue-800 dark:text-blue-300 border-r border-b border-slate-200 dark:border-slate-800">
                          {{ formatRupiah(sub.keuangan_total_sd_bulan_ini) }}
                        </td>

                        <td class="py-2.5 px-2 text-right font-bold text-indigo-700 dark:text-indigo-400 border-r border-b border-slate-200 dark:border-slate-800">
                          {{ formatRupiah(sub.keuangan_total_sipd) }}
                        </td>

                        <td v-for="(v, mIdx) in sub.keuangan_per_bulan" :key="'sub-rkb-' + mIdx" class="py-2 px-2 text-right font-medium text-[10px] border-r border-slate-150 dark:border-slate-800/50">
                          {{ v > 0 ? formatRupiah(v) : '-' }}
                        </td>
                      </tr>

                      <!-- LOOP PEKERJAAN -->
                      <template v-if="monthDetailExpandedNodes['sub-' + sub.kode]" v-for="(pek, pIdx) in sub.pekerjaan" :key="'m-pek-' + pek.id">
                        <tr 
                          @click="openFormRealisasiModal(pek)"
                          class="hover:bg-[#308e87]/10 dark:hover:bg-[#308e87]/20 transition-colors cursor-pointer group"
                          title="Klik untuk mengisi / mengedit realisasi pekerjaan ini"
                        >
                          <td class="py-2 px-4 pl-20 border-r border-b border-slate-150 dark:border-slate-800/60 w-[360px] max-w-[360px] sticky left-0 bg-white dark:bg-[#141d30] group-hover:bg-[#f2fcfb] dark:group-hover:bg-[#182a3a] z-20">
                            <div class="flex items-center space-x-2 min-w-0 max-w-[270px]">
                              <Briefcase class="w-3.5 h-3.5 text-[#f39159] shrink-0" />
                              <span class="font-bold text-slate-800 dark:text-slate-200 text-xs leading-snug truncate group-hover:text-[#308e87]">
                                {{ pek.nomor_pekerjaan ? pek.nomor_pekerjaan + '.' : (pIdx + 1) + '.' }} {{ pek.nama_pekerjaan }}
                              </span>
                              <Edit3 class="w-3 h-3 text-[#308e87] opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                            </div>
                          </td>

                          <td class="py-2 px-3 text-right font-bold text-slate-900 dark:text-white border-r border-b border-slate-150 dark:border-slate-800/60">
                            {{ formatRupiah(pek.anggaran) }}
                          </td>

                          <td class="py-2 px-2 text-center font-medium text-slate-700 dark:text-slate-300 border-r border-b border-slate-150 dark:border-slate-800/60">
                            {{ formatPercent(pek.realisasi_fisik) }}
                          </td>

                          <td class="py-2 px-2 text-right font-semibold text-blue-600 dark:text-blue-400 border-r border-b border-slate-150 dark:border-slate-800/60">
                            {{ formatRupiah(pek.keuangan_bulan_ini) }}
                          </td>

                          <td class="py-2 px-2 text-right font-semibold text-blue-700 dark:text-blue-300 border-r border-b border-slate-150 dark:border-slate-800/60">
                            {{ formatRupiah(pek.keuangan_total_sd_bulan_ini) }}
                          </td>

                          <td class="py-2 px-2 text-right font-semibold text-indigo-600 dark:text-indigo-400 border-r border-b border-slate-150 dark:border-slate-800/60">
                            {{ formatRupiah(pek.keuangan_total_sipd) }}
                          </td>

                          <td v-for="(v, mIdx) in pek.keuangan_per_bulan" :key="'pek-rkb-' + mIdx" class="py-2 px-2 text-right font-medium text-[10px] text-slate-600 dark:text-slate-400 border-r border-slate-100 dark:border-slate-800/40">
                            {{ v > 0 ? formatRupiah(v) : '-' }}
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

        <div v-else class="py-16 text-center text-slate-400">
          <FileX class="w-12 h-12 mx-auto text-slate-300 dark:text-slate-700 mb-2" />
          <p class="font-bold text-xs">Tidak ada data rincian RFK ditemukan untuk bulan ini.</p>
        </div>

      </div>
    </template>

    <!-- DELETE CONFIRMATION MODAL (Admin Only) -->
    <div 
      v-if="showDeleteConfirm && monthToDelete" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-150"
    >
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-700 rounded-3xl shadow-2xl max-w-md w-full p-6 space-y-5 relative">
        <button 
          @click="showDeleteConfirm = false; monthToDelete = null" 
          class="absolute right-4 top-4 p-1.5 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <X class="w-5 h-5" />
        </button>

        <div class="space-y-2 pr-6">
          <div class="w-12 h-12 rounded-2xl bg-rose-500/10 text-rose-500 flex items-center justify-center mb-3">
            <Trash2 class="w-6 h-6" />
          </div>
          <h3 class="text-base font-extrabold text-slate-900 dark:text-white leading-tight">
            Konfirmasi Hapus Laporan RFK
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
            Apakah Anda yakin ingin menghapus Laporan RFK bulan <strong class="text-slate-800 dark:text-slate-200">{{ monthNames[monthToDelete.bulan - 1] }} {{ selectedTahun }}</strong> untuk <strong class="text-slate-800 dark:text-slate-200">{{ monthToDelete.opd.nama_pd }}</strong>?
          </p>
        </div>

        <div class="p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-800 dark:text-rose-300 text-xs font-bold space-y-1">
          <p class="flex items-center space-x-1.5">
            <AlertCircle class="w-4 h-4 text-rose-500 shrink-0" />
            <span>Tindakan ini tidak dapat dibatalkan!</span>
          </p>
        </div>

        <div class="flex items-center justify-end space-x-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          <button 
            @click="showDeleteConfirm = false; monthToDelete = null"
            class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 font-bold text-xs text-slate-700 dark:text-slate-200 transition-colors cursor-pointer"
          >
            Batal
          </button>
          <button 
            @click="handleDeleteLaporan"
            :disabled="deletingBulan !== null"
            class="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-black text-xs transition-all cursor-pointer flex items-center space-x-1.5 shadow-md active:scale-95 disabled:opacity-50"
          >
            <Loader2 v-if="deletingBulan !== null" class="w-4 h-4 animate-spin" />
            <Trash2 v-else class="w-4 h-4" />
            <span>Ya, Hapus Laporan</span>
          </button>
        </div>
      </div>
    </div>

    <!-- FORM ENTRI REALISASI PEKERJAAN MODAL (ta_pekerjaan_realisasi) -->
    <div 
      v-if="selectedPekerjaanForm" 
      :class="isFormModalMaximized ? 'p-0' : 'p-3 sm:p-5'"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-150 transition-all"
    >
      <div 
        :class="isFormModalMaximized ? 'w-screen h-screen max-w-none max-h-none rounded-none border-0' : 'w-full max-w-2xl max-h-[92vh] rounded-3xl border-2 border-slate-200 dark:border-slate-800'"
        class="bg-white dark:bg-[#141d30] shadow-2xl flex flex-col overflow-hidden relative transition-all duration-200"
      >
        
        <!-- Modal Header -->
        <div class="px-6 py-4 bg-gradient-to-r from-[#1b4e4a] via-[#308e87] to-[#25736d] text-white flex items-center justify-between shrink-0">
          <div>
            <div class="flex items-center space-x-2 text-xs font-black text-[#85e3db]">
              <Edit3 class="w-4 h-4" />
              <span>Form Entri Realisasi Pekerjaan</span>
            </div>
            <h3 class="text-base font-extrabold mt-0.5 leading-snug">
              {{ selectedPekerjaanForm.nama_pekerjaan }}
            </h3>
            <p class="text-xs font-mono font-bold text-slate-200">
              Pagu Anggaran: {{ formatRupiah(selectedPekerjaanForm.anggaran) }} | Bulan {{ monthNames[(selectedMonthDetail?.bulan || 1) - 1] }} {{ selectedTahun }}
            </p>

            <!-- Tagging Badges -->
            <div v-if="formRealisasiData.tagging?.length > 0" class="flex flex-wrap items-center gap-1.5 mt-2">
              <span 
                v-for="(tag, tIdx) in formRealisasiData.tagging" 
                :key="'mod-tag-' + tIdx"
                class="px-2 py-0.5 rounded-lg bg-amber-400/20 text-amber-200 border border-amber-300/30 text-[10px] font-black inline-flex items-center space-x-1"
              >
                <Tag class="w-3 h-3 text-amber-300 shrink-0" />
                <span>{{ tag }}</span>
              </span>
            </div>
          </div>

          <div class="flex items-center space-x-1.5 shrink-0">
            <!-- Navigation Previous / Next Controls -->
            <div v-if="allPekerjaanList.length > 0" class="flex items-center space-x-1.5 bg-black/20 p-1.5 rounded-2xl border border-white/20 mr-1">
              <button 
                type="button"
                @click="navigatePekerjaan('prev')"
                :disabled="!hasPrevPekerjaan"
                class="p-1 rounded-xl hover:bg-white/20 text-white transition-all cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed flex items-center space-x-1"
                title="Pekerjaan Sebelumnya"
              >
                <ChevronLeft class="w-4 h-4" />
                <span class="text-[10px] font-extrabold hidden sm:inline">Sebelumnya</span>
              </button>

              <span class="text-[10px] font-mono font-black text-amber-200 px-1.5">
                {{ currentPekerjaanIndex >= 0 ? currentPekerjaanIndex + 1 : 1 }} / {{ allPekerjaanList.length }}
              </span>

              <button 
                type="button"
                @click="navigatePekerjaan('next')"
                :disabled="!hasNextPekerjaan"
                class="p-1 rounded-xl hover:bg-white/20 text-white transition-all cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed flex items-center space-x-1"
                title="Pekerjaan Berikutnya"
              >
                <span class="text-[10px] font-extrabold hidden sm:inline">Berikutnya</span>
                <ChevronRight class="w-4 h-4" />
              </button>
            </div>

            <!-- Maximize / Restore Toggle Button -->
            <button 
              type="button"
              @click="isFormModalMaximized = !isFormModalMaximized" 
              class="p-2 rounded-full hover:bg-white/20 text-white transition-colors cursor-pointer"
              :title="isFormModalMaximized ? 'Kecilkan Tampilan (Restore)' : 'Perbesar Tampilan (Maximize)'"
            >
              <Minimize2 v-if="isFormModalMaximized" class="w-4 h-4" />
              <Maximize2 v-else class="w-4 h-4" />
            </button>

            <!-- Close Button -->
            <button 
              @click="selectedPekerjaanForm = null" 
              class="p-2 rounded-full hover:bg-white/20 text-white transition-colors cursor-pointer"
              title="Tutup Modal"
            >
              <X class="w-5 h-5" />
            </button>
          </div>
        </div>

        <!-- Modal Tabbed Navigation -->
        <div class="flex items-center space-x-1 px-6 pt-3 bg-slate-100/80 dark:bg-slate-900/60 border-b border-slate-200 dark:border-slate-800 shrink-0">
          <button 
            type="button"
            @click="activeFormTab = 'realisasi'"
            :class="activeFormTab === 'realisasi' ? 'bg-white dark:bg-[#141d30] text-[#308e87] border-t-2 border-t-[#308e87] font-black shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 font-bold'"
            class="px-4 py-2.5 rounded-t-xl text-xs transition-all cursor-pointer inline-flex items-center space-x-1.5"
          >
            <FileText class="w-4 h-4" />
            <span>1. Entri Realisasi</span>
          </button>
          
          <button 
            type="button"
            @click="activeFormTab = 'dokumen'"
            :class="activeFormTab === 'dokumen' ? 'bg-white dark:bg-[#141d30] text-[#308e87] border-t-2 border-t-[#308e87] font-black shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 font-bold'"
            class="px-4 py-2.5 rounded-t-xl text-xs transition-all cursor-pointer inline-flex items-center space-x-1.5"
          >
            <UploadCloud class="w-4 h-4" />
            <span>2. Data Dukung (Foto &amp; Dokumen)</span>
            <span 
              v-if="dokumenList.length > 0" 
              class="px-1.5 py-0.2 text-[10px] font-black rounded-full bg-[#308e87] text-white ml-1"
            >
              {{ dokumenList.length }}
            </span>
          </button>

          <button 
            type="button"
            @click="activeFormTab = 'lokasi'"
            :class="activeFormTab === 'lokasi' ? 'bg-white dark:bg-[#141d30] text-[#308e87] border-t-2 border-t-[#308e87] font-black shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 font-bold'"
            class="px-4 py-2.5 rounded-t-xl text-xs transition-all cursor-pointer inline-flex items-center space-x-1.5"
          >
            <MapPin class="w-4 h-4 text-emerald-500" />
            <span>3. Lokasi Pekerjaan</span>
            <span 
              v-if="formRealisasiData.lokasi_list?.length > 0" 
              class="px-1.5 py-0.2 text-[10px] font-black rounded-full bg-emerald-500 text-white ml-1"
            >
              {{ formRealisasiData.lokasi_list.length }}
            </span>
          </button>

          <button 
            type="button"
            @click="activeFormTab = 'kontrak'"
            :class="activeFormTab === 'kontrak' ? 'bg-white dark:bg-[#141d30] text-[#308e87] border-t-2 border-t-[#308e87] font-black shadow-xs' : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 font-bold'"
            class="px-4 py-2.5 rounded-t-xl text-xs transition-all cursor-pointer inline-flex items-center space-x-1.5"
          >
            <FileCheck class="w-4 h-4 text-indigo-500" />
            <span>4. Kontrak / SPK</span>
            <span 
              v-if="formKontrakData.nomor_kontrak" 
              class="px-1.5 py-0.2 text-[10px] font-black rounded-full bg-indigo-500 text-white ml-1"
            >
              ✓
            </span>
          </button>
        </div>

        <!-- Modal Body -->
        <div class="p-6 overflow-y-auto flex-1 space-y-5">
          
          <!-- Success Notification Banner inside Modal -->
          <div v-if="modalSaveSuccess" class="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-800 dark:text-emerald-300 flex items-center justify-between animate-in fade-in duration-200">
            <div class="flex items-center space-x-2">
              <CheckCircle2 class="w-4 h-4 text-emerald-500 shrink-0" />
              <span class="text-xs font-bold">{{ modalSaveSuccessMsg }}</span>
            </div>
            <button type="button" @click="modalSaveSuccess = false" class="p-1 rounded-lg hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 cursor-pointer">
              <X class="w-3.5 h-3.5" />
            </button>
          </div>

          <div v-if="loadingRealisasiForm" class="py-12 text-center">
            <Loader2 class="w-8 h-8 animate-spin mx-auto mb-2 text-[#308e87]" />
            <span class="font-bold text-xs text-slate-400">Memuat data realisasi pekerjaan...</span>
          </div>

          <!-- TAB 1: FORM ENTRI REALISASI -->
          <form v-else-if="activeFormTab === 'realisasi'" @submit.prevent="handleSaveRealisasi" class="space-y-4 text-xs font-bold">
            
            <!-- Physical Realization Info Cards (3 Columns) -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
              
              <!-- Card 1: Realisasi Fisik Bulan Lalu -->
              <div class="p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/20 space-y-1">
                <span class="block text-[11px] font-bold text-amber-800 dark:text-amber-300">
                  Realisasi Fisik Bulan Lalu
                </span>
                <div class="text-lg font-black text-amber-900 dark:text-amber-200 font-mono">
                  {{ formRealisasiData.fisik_lalu }}%
                </div>
                <p class="text-[9px] text-slate-400 font-medium">Capaian s/d bulan lalu</p>
              </div>

              <!-- Card 2: Target Fisik Bulan Ini -->
              <div class="p-3.5 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 space-y-1">
                <span class="block text-[11px] font-bold text-indigo-800 dark:text-indigo-300">
                  Target Fisik Bulan Ini
                </span>
                <div class="text-lg font-black text-indigo-900 dark:text-indigo-200 font-mono">
                  {{ formRealisasiData.target_fisik_bulan_ini }}%
                </div>
                <p class="text-[9px] text-slate-400 font-medium">Target bulan {{ monthNames[(selectedMonthDetail?.bulan || 1) - 1] }}</p>
              </div>

              <!-- Card 3: Input Realisasi Fisik Bulan Ini (%) -->
              <div class="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 space-y-1">
                <label class="block text-[11px] font-extrabold text-emerald-800 dark:text-emerald-300">
                  Realisasi Fisik Bulan Ini (%) <span class="text-rose-500">*</span>
                </label>
                <div class="relative">
                  <input 
                    v-model.number="formRealisasiData.fisik" 
                    type="number" 
                    step="0.01" 
                    min="0" 
                    max="100" 
                    required
                    class="w-full px-3 py-1.5 rounded-xl bg-white dark:bg-slate-900 border-2 border-emerald-500/40 text-slate-900 dark:text-white font-black text-sm focus:outline-none focus:border-emerald-500"
                    placeholder="0 - 100"
                  />
                  <span class="absolute right-2.5 top-1/2 -translate-y-1/2 font-black text-emerald-600 text-xs">%</span>
                </div>
              </div>

            </div>

            <!-- Financial Realization Input -->
            <div class="space-y-1.5 p-4 rounded-2xl bg-blue-500/5 border border-blue-500/20">
              <label class="block text-blue-800 dark:text-blue-300 font-extrabold">
                Realisasi Keuangan Bulan Ini (Rp) <span class="text-rose-500">*</span>
              </label>
              <div class="relative">
                <input 
                  v-model.number="formRealisasiData.keuangan" 
                  type="number" 
                  step="1" 
                  min="0" 
                  required
                  class="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-900 border-2 border-blue-500/30 text-slate-900 dark:text-white font-black text-sm focus:outline-none focus:border-blue-500"
                  placeholder="0"
                />
              </div>
              <p class="text-[10px] text-slate-400">Realisasi keuangan s/d bulan lalu: {{ formatRupiah(formRealisasiData.keuangan_lalu) }}</p>
            </div>

            <!-- Total Cumulative Summary Banner -->
            <div class="p-4 rounded-2xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 flex items-center justify-between">
              <div>
                <span class="text-slate-500 dark:text-slate-400 font-bold block text-[11px]">Total Realisasi Keuangan s/d Bulan Ini:</span>
                <span class="text-sm font-black text-slate-900 dark:text-white font-mono">
                  {{ formatRupiah(totalKeuanganSdBulanIni) }}
                </span>
              </div>
              <div class="text-right">
                <span class="text-slate-500 dark:text-slate-400 font-bold block text-[11px]">Persentase Keuangan s/d Bulan Ini:</span>
                <span class="text-sm font-black text-[#308e87] dark:text-[#3aada4]">
                  {{ formatPercent(selectedPekerjaanForm.anggaran > 0 ? (totalKeuanganSdBulanIni / selectedPekerjaanForm.anggaran * 100) : 0) }}
                </span>
              </div>
            </div>

            <!-- Permasalahan / Kendala -->
            <div class="space-y-1.5">
              <label class="block text-slate-700 dark:text-slate-300 font-bold">
                Permasalahan / Kendala (Opsional):
              </label>
              <textarea 
                v-model="formRealisasiData.masalah" 
                rows="2" 
                class="w-full p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-[#308e87]"
                placeholder="Tuliskan kendala atau permasalahan pelaksanaan pekerjaan..."
              ></textarea>
            </div>

            <!-- Upaya Penanganan -->
            <div class="space-y-1.5">
              <label class="block text-slate-700 dark:text-slate-300 font-bold">
                Solusi / Upaya Penanganan (Opsional):
              </label>
              <textarea 
                v-model="formRealisasiData.upaya" 
                rows="2" 
                class="w-full p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-[#308e87]"
                placeholder="Tuliskan solusi atau langkah penanganan yang telah dilakukan..."
              ></textarea>
            </div>

            <!-- Modal Footer Actions -->
            <div class="flex items-center justify-between pt-3 border-t border-slate-100 dark:border-slate-800">
              <!-- Previous / Next Footer Buttons -->
              <div v-if="allPekerjaanList.length > 0" class="flex items-center space-x-1.5">
                <button 
                  type="button"
                  @click="navigatePekerjaan('prev')"
                  :disabled="!hasPrevPekerjaan"
                  class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold text-xs transition-colors cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed inline-flex items-center space-x-1"
                >
                  <ChevronLeft class="w-4 h-4" />
                  <span>Sebelumnya</span>
                </button>
                <button 
                  type="button"
                  @click="navigatePekerjaan('next')"
                  :disabled="!hasNextPekerjaan"
                  class="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold text-xs transition-colors cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed inline-flex items-center space-x-1"
                >
                  <span>Berikutnya</span>
                  <ChevronRight class="w-4 h-4" />
                </button>
              </div>
              <div v-else></div>

              <div class="flex items-center space-x-2">
                <button 
                  type="button"
                  @click="selectedPekerjaanForm = null" 
                  class="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 font-bold text-xs text-slate-700 dark:text-slate-200 transition-colors cursor-pointer"
                >
                  Batal
                </button>
                <button 
                  type="submit"
                  :disabled="savingRealisasi"
                  class="px-5 py-2 rounded-xl bg-[#308e87] hover:bg-[#25736d] text-white font-black text-xs transition-all cursor-pointer flex items-center space-x-1.5 shadow-md active:scale-95 disabled:opacity-50"
                >
                  <Loader2 v-if="savingRealisasi" class="w-4 h-4 animate-spin" />
                  <Edit3 v-else class="w-4 h-4" />
                  <span>Simpan Realisasi</span>
                </button>
              </div>
            </div>

          </form>

          <!-- TAB 2: UPLOAD DATA DUKUNG (FOTO & DOKUMEN) -->
          <div v-else-if="activeFormTab === 'dokumen'" class="space-y-6 text-xs font-bold">
            
            <!-- Upload Form Box -->
            <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-4 shadow-xs">
              <div class="flex items-center space-x-2 font-black text-slate-800 dark:text-slate-200">
                <UploadCloud class="w-5 h-5 text-[#308e87]" />
                <h4 class="text-sm">Unggah Berkas Data Dukung</h4>
              </div>

              <form @submit.prevent="handleUploadDokumen" class="space-y-3">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  
                  <!-- Category Select -->
                  <div class="space-y-1">
                    <label class="block text-slate-600 dark:text-slate-300 font-bold">Kategori Berkas:</label>
                    <select 
                      v-model="uploadCategory" 
                      class="w-full px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold focus:outline-none focus:ring-2 focus:ring-[#308e87]"
                    >
                      <option value="foto">Foto Kegiatan (Gambar/Foto)</option>
                      <option value="dokumen">Dokumen Pendukung (PDF/Word/Excel)</option>
                    </select>
                  </div>

                  <!-- File Input -->
                  <div class="space-y-1">
                    <label class="block text-slate-600 dark:text-slate-300 font-bold">Pilih Berkas File: <span class="text-rose-500">*</span></label>
                    <input 
                      type="file" 
                      @change="handleFileSelect"
                      required
                      accept="image/*,.pdf,.doc,.docx,.xls,.xlsx"
                      class="w-full px-3 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-600 dark:text-slate-300 file:mr-3 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-[#308e87]/10 file:text-[#308e87] hover:file:bg-[#308e87]/20 cursor-pointer"
                    />
                  </div>

                </div>

                <!-- Keterangan / Deskripsi -->
                <div class="space-y-1">
                  <label class="block text-slate-600 dark:text-slate-300 font-bold">Keterangan / Deskripsi File (Opsional):</label>
                  <input 
                    v-model="uploadKeterangan" 
                    type="text" 
                    placeholder="Contoh: Foto Progres Fisik 50% atau Dokumen Kontrak Kerja"
                    class="w-full px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-[#308e87]"
                  />
                </div>

                <!-- Upload Button -->
                <div class="flex justify-end pt-1">
                  <button 
                    type="submit"
                    :disabled="uploadingFile || !selectedFile"
                    class="px-5 py-2 rounded-xl bg-[#308e87] hover:bg-[#25736d] text-white font-black text-xs transition-all cursor-pointer flex items-center space-x-1.5 shadow-md active:scale-95 disabled:opacity-50"
                  >
                    <Loader2 v-if="uploadingFile" class="w-4 h-4 animate-spin" />
                    <UploadCloud v-else class="w-4 h-4" />
                    <span>Mulai Unggah Berkas</span>
                  </button>
                </div>
              </form>
            </div>

            <!-- Loading State for Dokumen List -->
            <div v-if="loadingDokumenList" class="py-12 text-center">
              <Loader2 class="w-8 h-8 animate-spin mx-auto mb-2 text-[#308e87]" />
              <span class="font-bold text-xs text-slate-400">Memuat daftar data dukung...</span>
            </div>

            <div v-else class="space-y-6">
              
              <!-- SECTION 1: FOTO KEGIATAN GALLERY -->
              <div class="space-y-3">
                <div class="flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-2">
                  <Image class="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <h5 class="font-black text-slate-800 dark:text-slate-200 text-xs uppercase tracking-wide">
                    Foto Kegiatan ({{ fotoDokumenList.length }})
                  </h5>
                </div>

                <div v-if="fotoDokumenList.length > 0" class="grid grid-cols-2 sm:grid-cols-3 gap-3.5">
                  <div 
                    v-for="foto in fotoDokumenList" 
                    :key="'foto-' + foto.id"
                    class="group rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden bg-white dark:bg-slate-900 flex flex-col shadow-xs hover:shadow-md transition-all relative"
                  >
                    <!-- Thumbnail Image -->
                    <div class="h-32 bg-slate-100 dark:bg-slate-800 overflow-hidden relative">
                      <img 
                        :src="foto.file_path" 
                        :alt="foto.nama_file" 
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" 
                      />
                      <a 
                        :href="foto.file_path" 
                        target="_blank" 
                        class="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white transition-opacity font-bold text-xs gap-1"
                      >
                        <Eye class="w-4 h-4" />
                        <span>Lihat Foto</span>
                      </a>
                    </div>

                    <!-- Details -->
                    <div class="p-2.5 space-y-1 flex-1 flex flex-col justify-between">
                      <div>
                        <p class="font-extrabold text-slate-800 dark:text-slate-200 text-[11px] truncate" :title="foto.keterangan || foto.nama_file">
                          {{ foto.keterangan || foto.nama_file }}
                        </p>
                        <p class="text-[9px] font-mono font-semibold text-slate-400">
                          {{ foto.tgl_upload_fmt || '-' }}
                        </p>
                      </div>

                      <div class="flex items-center justify-between pt-1 border-t border-slate-100 dark:border-slate-800 mt-1">
                        <span class="text-[9px] font-bold text-slate-400 font-mono">
                          {{ formatFileSize(foto.ukuran_file) }}
                        </span>
                        <button 
                          @click="handleDeleteDokumen(foto.id)"
                          :disabled="deletingDokumenId === foto.id"
                          class="p-1 rounded-lg text-rose-500 hover:bg-rose-500/10 transition-colors cursor-pointer"
                          title="Hapus foto ini"
                        >
                          <Loader2 v-if="deletingDokumenId === foto.id" class="w-3.5 h-3.5 animate-spin" />
                          <Trash2 v-else class="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-else class="p-6 text-center bg-slate-50 dark:bg-slate-900/40 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 text-slate-400 font-bold text-xs">
                  Belum ada Foto Kegiatan yang diunggah untuk bulan ini.
                </div>
              </div>

              <!-- SECTION 2: DOKUMEN PENDUKUNG TABLE -->
              <div class="space-y-3">
                <div class="flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-2">
                  <Paperclip class="w-4 h-4 text-blue-600 dark:text-blue-400 shrink-0" />
                  <h5 class="font-black text-slate-800 dark:text-slate-200 text-xs uppercase tracking-wide">
                    Dokumen Pendukung ({{ berkasDokumenList.length }})
                  </h5>
                </div>

                <div v-if="berkasDokumenList.length > 0" class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-xs">
                  <table class="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr class="bg-slate-100/90 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-black uppercase text-[10px] border-b border-slate-200 dark:border-slate-800">
                        <th class="py-2.5 px-3">Nama Berkas / Keterangan</th>
                        <th class="py-2.5 px-3 w-28 text-center">Ukuran</th>
                        <th class="py-2.5 px-3 w-32">Tanggal Upload</th>
                        <th class="py-2.5 px-3 w-24 text-center">Aksi</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 font-semibold">
                      <tr 
                        v-for="doc in berkasDokumenList" 
                        :key="'doc-' + doc.id"
                        class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                      >
                        <td class="py-2.5 px-3">
                          <div class="flex items-center space-x-2.5">
                            <FileCheck class="w-4 h-4 text-blue-500 shrink-0" />
                            <div class="min-w-0">
                              <a 
                                :href="doc.file_path" 
                                target="_blank"
                                class="font-black text-slate-900 dark:text-white hover:text-[#308e87] truncate block"
                              >
                                {{ doc.nama_file }}
                              </a>
                              <p v-if="doc.keterangan" class="text-[10px] text-slate-400 font-medium truncate">
                                {{ doc.keterangan }}
                              </p>
                            </div>
                          </div>
                        </td>
                        <td class="py-2.5 px-3 text-center font-mono text-[10px] text-slate-500">
                          {{ formatFileSize(doc.ukuran_file) }}
                        </td>
                        <td class="py-2.5 px-3 font-mono text-[10px] text-slate-500">
                          {{ doc.tgl_upload_fmt || '-' }}
                        </td>
                        <td class="py-2.5 px-3 text-center">
                          <div class="flex items-center justify-center space-x-1">
                            <a 
                              :href="doc.file_path" 
                              target="_blank"
                              class="p-1.5 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 text-blue-600 dark:text-blue-400 transition-colors inline-flex items-center"
                              title="Buka / Download file"
                            >
                              <Download class="w-3.5 h-3.5" />
                            </a>
                            <button 
                              @click="handleDeleteDokumen(doc.id)"
                              :disabled="deletingDokumenId === doc.id"
                              class="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-600 dark:text-rose-400 transition-colors inline-flex items-center cursor-pointer"
                              title="Hapus file ini"
                            >
                              <Loader2 v-if="deletingDokumenId === doc.id" class="w-3.5 h-3.5 animate-spin" />
                              <Trash2 v-else class="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div v-else class="p-6 text-center bg-slate-50 dark:bg-slate-900/40 rounded-2xl border border-dashed border-slate-200 dark:border-slate-800 text-slate-400 font-bold text-xs">
                  Belum ada Dokumen Pendukung yang diunggah untuk bulan ini.
                </div>
              </div>

            </div>

          </div>

          <!-- TAB 3: LOKASI PEKERJAAN & MAP -->
          <div v-else-if="activeFormTab === 'lokasi'" class="space-y-4 text-xs font-bold animate-in fade-in duration-150">
            <div class="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-800 dark:text-emerald-300 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <MapPin class="w-4 h-4 text-emerald-500 shrink-0" />
                <span class="text-xs font-black">Pemetaan &amp; Koordinat GIS Lokasi Pekerjaan</span>
              </div>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-700 dark:text-emerald-300">
                {{ formRealisasiData.lokasi_list?.length || 0 }} Titik/Geometri Terdata
              </span>
            </div>

            <!-- Teks Deskripsi Lokasi -->
            <div>
              <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase text-[10px] tracking-wider">
                Nama / Alamat / Keterangan Lokasi Pekerjaan
              </label>
              <input 
                type="text" 
                v-model="formRealisasiData.lokasi" 
                placeholder="Contoh: Jl. Gajah Mada No. 12, Kel. Kudaile, Kec. Slawi"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-semibold focus:outline-none focus:border-[#308e87]"
              />
            </div>

            <!-- Interactive Map Container -->
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <label class="block font-black text-[#308e87] dark:text-[#3aada4] uppercase text-[10px] tracking-wider">
                  Peta GIS (Gunakan toolbar Leaflet-Geoman di kiri atas untuk menggambar Titik/Garis/Area)
                </label>
                <button 
                  type="button" 
                  @click="clearAllLocations" 
                  v-if="formRealisasiData.lokasi_list?.length > 0"
                  class="text-[10px] font-bold text-red-500 hover:text-red-600 dark:hover:text-red-400 flex items-center space-x-1 cursor-pointer"
                >
                  <Trash2 class="w-3 h-3" />
                  <span>Hapus Semua Titik</span>
                </button>
              </div>

              <!-- Map Container -->
              <div 
                id="rfk-pekerjaan-map" 
                class="w-full h-80 sm:h-[400px] rounded-2xl border-2 border-slate-200 dark:border-slate-700 shadow-inner z-10 overflow-hidden relative"
              ></div>
            </div>

            <!-- Daftar Titik GIS yang Terdaftar -->
            <div v-if="formRealisasiData.lokasi_list?.length > 0" class="space-y-2 pt-2 border-t border-slate-200 dark:border-slate-800">
              <span class="block text-[10px] font-black uppercase text-slate-500 tracking-wider">Daftar Koordinat &amp; Geometri GIS:</span>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div 
                  v-for="(loc, lIdx) in formRealisasiData.lokasi_list" 
                  :key="'rfk-loc-' + lIdx"
                  class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 flex items-center justify-between"
                >
                  <div class="min-w-0 pr-2">
                    <span class="font-extrabold text-slate-800 dark:text-slate-100 text-xs block truncate">
                      {{ loc.nama_lokasi || 'Lokasi Pekerjaan ' + (lIdx + 1) }}
                    </span>
                    <span class="font-mono text-[10px] text-slate-500 block truncate">
                      Jenis: {{ loc.jenis_geometry || 'Point' }} | Lat: {{ loc.lat ? loc.lat.toFixed(5) : '-' }}, Lng: {{ loc.lng ? loc.lng.toFixed(5) : '-' }}
                    </span>
                  </div>
                  <button 
                    type="button" 
                    @click="removeSingleLocation(lIdx)" 
                    class="p-1.5 rounded-lg hover:bg-red-500/20 text-red-500 cursor-pointer shrink-0"
                    title="Hapus lokasi ini"
                  >
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Action Save Lokasi Button -->
            <div class="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end">
              <button 
                type="button" 
                @click="handleSaveLokasi" 
                :disabled="savingLokasi"
                class="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-[#308e87] text-white font-black text-xs rounded-xl shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30 flex items-center space-x-2 cursor-pointer disabled:opacity-50 transition-all"
              >
                <Loader2 v-if="savingLokasi" class="w-4 h-4 animate-spin" />
                <Save v-else class="w-4 h-4" />
                <span>Simpan Lokasi Pekerjaan</span>
              </button>
            </div>
          </div>

          <!-- TAB 4: KONTRAK / SPK -->
          <form v-else-if="activeFormTab === 'kontrak'" @submit.prevent="handleSaveKontrak" class="space-y-5 text-xs font-bold animate-in fade-in duration-150">
            <div class="p-3.5 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-800 dark:text-indigo-300 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <FileCheck class="w-4 h-4 text-indigo-500 shrink-0" />
                <span class="text-xs font-black">Data Kontrak / Surat Perintah Kerja (SPK)</span>
              </div>
              <span 
                class="text-[10px] font-extrabold px-2.5 py-0.5 rounded-lg text-white"
                :class="{
                  'bg-emerald-500': formKontrakData.status_kontrak === 'Selesai',
                  'bg-amber-500': formKontrakData.status_kontrak === 'Dalam Proses',
                  'bg-rose-500': formKontrakData.status_kontrak === 'Dibatalkan'
                }"
              >
                Status: {{ formKontrakData.status_kontrak || 'Dalam Proses' }}
              </span>
            </div>

            <!-- GRID SECTION 1: PEJABAT & PENGELOLA -->
            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800/80 space-y-3">
              <span class="block text-[11px] font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                1. Pejabat &amp; Pengelola Pekerjaan
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nama PPK</label>
                  <input type="text" v-model="formKontrakData.nama_ppk" placeholder="Nama Pejabat Pembuat Komitmen" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nama PPTK</label>
                  <input type="text" v-model="formKontrakData.nama_pptk" placeholder="Nama Pejabat Pelaksana Teknis Kegiatan" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nama Ketua Pokja / Pejabat Pengadaan</label>
                  <input type="text" v-model="formKontrakData.nama_pokja" placeholder="Nama Ketua Pokja atau Pejabat Pengadaan" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nama Ketua PPHP</label>
                  <input type="text" v-model="formKontrakData.nama_pphp" placeholder="Nama Ketua Panitia Pemeriksa Hasil Pekerjaan" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
              </div>
            </div>

            <!-- GRID SECTION 2: NILAI ANGGARAN & KONTRAK -->
            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800/80 space-y-3">
              <span class="block text-[11px] font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                2. Nilai Anggaran &amp; Nilai Kontrak
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nilai HPS (Rp)</label>
                  <input type="number" step="any" v-model.number="formKontrakData.nilai_hps" placeholder="0" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                  <span class="text-[9px] text-slate-400 mt-0.5 block font-mono">{{ formatRupiah(formKontrakData.nilai_hps) }}</span>
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nilai Kontrak / SPK (Rp)</label>
                  <input type="number" step="any" v-model.number="formKontrakData.nilai_kontrak" placeholder="0" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                  <span class="text-[9px] text-slate-400 mt-0.5 block font-mono">{{ formatRupiah(formKontrakData.nilai_kontrak) }}</span>
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Sisa Anggaran (Pagu - Kontrak)</label>
                  <input type="number" step="any" v-model.number="formKontrakData.sisa_anggaran" placeholder="0" class="w-full px-3 py-2 bg-slate-100 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono font-bold" />
                  <span class="text-[9px] text-emerald-600 dark:text-emerald-400 mt-0.5 block font-mono font-bold">{{ formatRupiah(formKontrakData.sisa_anggaran) }}</span>
                </div>
              </div>
            </div>

            <!-- GRID SECTION 3: DATA PENYEDIA -->
            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800/80 space-y-3">
              <span class="block text-[11px] font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                3. Identitas Penyedia / Pelaksana Pekerjaan
              </span>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nama Penyedia / Badan Usaha</label>
                  <input type="text" v-model="formKontrakData.nama_penyedia" placeholder="Contoh: PT. Karya Utama Mandiri" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nama Pimpinan Penyedia</label>
                  <input type="text" v-model="formKontrakData.pimpinan_penyedia" placeholder="Nama Direktur / Pimpinan Penyedia" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">NPWP Penyedia</label>
                  <input type="text" v-model="formKontrakData.npwp_penyedia" placeholder="00.000.000.0-000.000" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Alamat Penyedia</label>
                  <input type="text" v-model="formKontrakData.alamat_penyedia" placeholder="Alamat lengkap badan usaha / penyedia" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white" />
                </div>
              </div>
            </div>

            <!-- GRID SECTION 4: LEGALITAS, SPMK & MASA KONTRAK -->
            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800/80 space-y-3">
              <span class="block text-[11px] font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                4. Nomor Kontrak, SPMK, Adendum &amp; Tanggal Pelaksanaan
              </span>
              
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
                <div class="sm:col-span-1">
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nomor Pengadaan / Kontrak / SPK</label>
                  <input type="text" v-model="formKontrakData.nomor_kontrak" placeholder="Nomor Kontrak / SPK" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Tanggal Kontrak (Mulai)</label>
                  <input type="date" v-model="formKontrakData.tgl_kontrak_awal" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Tanggal Kontrak (Selesai)</label>
                  <input type="date" v-model="formKontrakData.tgl_kontrak_akhir" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5 pt-2 border-t border-slate-200 dark:border-slate-800">
                <div class="sm:col-span-1">
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Nomor SPMK</label>
                  <input type="text" v-model="formKontrakData.nomor_spmk" placeholder="Nomor Surat Perintah Mulai Kerja" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Tanggal SPMK (Mulai)</label>
                  <input type="date" v-model="formKontrakData.tgl_spmk_awal" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Tanggal SPMK (Selesai)</label>
                  <input type="date" v-model="formKontrakData.tgl_spmk_akhir" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5 pt-2 border-t border-slate-200 dark:border-slate-800">
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Status Kontrak / Pekerjaan</label>
                  <select v-model="formKontrakData.status_kontrak" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-bold">
                    <option value="Dalam Proses">Dalam Proses</option>
                    <option value="Selesai">Selesai</option>
                    <option value="Dibatalkan">Dibatalkan</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Tanggal Adendum (Mulai)</label>
                  <input type="date" v-model="formKontrakData.tgl_adendum_awal" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
                <div>
                  <label class="block text-[10px] uppercase text-slate-500 mb-1">Tanggal Adendum (Selesai)</label>
                  <input type="date" v-model="formKontrakData.tgl_adendum_akhir" class="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white font-mono" />
                </div>
              </div>
            </div>

            <!-- Action Save Button -->
            <div class="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end">
              <button 
                type="submit" 
                :disabled="savingKontrak"
                class="px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-[#308e87] text-white font-black text-xs rounded-xl shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/30 flex items-center space-x-2 cursor-pointer disabled:opacity-50 transition-all"
              >
                <Loader2 v-if="savingKontrak" class="w-4 h-4 animate-spin" />
                <Save v-else class="w-4 h-4" />
                <span>Simpan Data Kontrak / SPK</span>
              </button>
            </div>
          </form>

        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import '@geoman-io/leaflet-geoman-free'
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css'
import { 
  TrendingUp, 
  Building2, 
  Send, 
  CheckCircle2, 
  CalendarCheck, 
  Calendar, 
  RotateCw, 
  Search, 
  X, 
  Loader2, 
  FileX,
  Plus,
  AlertCircle,
  Folder,
  Layers,
  Briefcase,
  ChevronRight,
  ChevronLeft,
  Trash2,
  Edit3,
  UploadCloud,
  FileText,
  Image,
  FileCheck,
  Paperclip,
  Download,
  Eye,
  Tag,
  Maximize2,
  Minimize2,
  MapPin,
  Map,
  Save
} from 'lucide-vue-next'

const authStore = useAuthStore()
const isAdmin = computed(() => {
  if (authStore.user?.role_id !== undefined && authStore.user?.role_id !== null) {
    return authStore.user.role_id <= 5
  }
  return true
})

const selectedTahun = ref(2026)
const loading = ref(false)
const searchQuery = ref('')
const opdFilterCategory = ref('all') // 'all', 'main', 'sub'

const currentView = ref('opd_list') // 'opd_list', 'opd_months', 'month_detail'

const summary = ref({
  total_opd: 0,
  total_laporan_terkirim: 0,
  bulan_terkirim: {}
})
const opdList = ref([])
const selectedOpdModal = ref(null)

const selectedMonthDetail = ref(null)
const loadingMonthDetail = ref(false)
const monthDetailExpandedNodes = ref({})

const selectedPekerjaanForm = ref(null)
const isFormModalMaximized = ref(false)
const loadingRealisasiForm = ref(false)
const savingRealisasi = ref(false)
const modalSaveSuccess = ref(false)
const modalSaveSuccessMsg = ref('')
const formRealisasiData = ref({
  id_pekerjaan: '',
  id_sub_pd: 0,
  bulan: 0,
  keuangan: 0,
  fisik: 0,
  masalah: '',
  upaya: '',
  keuangan_lalu: 0,
  fisik_lalu: 0,
  target_fisik_bulan_ini: 0,
  tagging: [],
  lokasi: '',
  lokasi_list: []
})

const activeFormTab = ref('realisasi') // 'realisasi', 'dokumen', 'lokasi', 'kontrak'
const savingKontrak = ref(false)
const formKontrakData = ref({
  nama_ppk: '',
  nama_pptk: '',
  nama_pokja: '',
  nama_pphp: '',
  nilai_hps: 0,
  nilai_kontrak: 0,
  sisa_anggaran: 0,
  nama_penyedia: '',
  alamat_penyedia: '',
  pimpinan_penyedia: '',
  npwp_penyedia: '',
  nomor_kontrak: '',
  tgl_kontrak_awal: '',
  tgl_kontrak_akhir: '',
  nomor_spmk: '',
  tgl_spmk_awal: '',
  tgl_spmk_akhir: '',
  tgl_adendum_awal: '',
  tgl_adendum_akhir: '',
  status_kontrak: 'Dalam Proses'
})

watch(() => formKontrakData.value.nilai_kontrak, (newVal) => {
  const pagu = selectedPekerjaanForm.value?.anggaran || 0
  const nilK = Number(newVal || 0)
  formKontrakData.value.sisa_anggaran = Math.max(0, pagu - nilK)
})
let rfkMap = null
let rfkDrawnGroup = null
const savingLokasi = ref(false)

const initRfkMap = () => {
  nextTick(() => {
    const mapEl = document.getElementById('rfk-pekerjaan-map')
    if (!mapEl) return

    if (rfkMap) {
      rfkMap.remove()
      rfkMap = null
    }

    const locs = formRealisasiData.value.lokasi_list || []
    const defaultLat = locs[0]?.lat || -6.86942
    const defaultLng = locs[0]?.lng || 109.13824

    rfkMap = L.map('rfk-pekerjaan-map').setView([defaultLat, defaultLng], 13)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap'
    }).addTo(rfkMap)

    rfkDrawnGroup = L.featureGroup().addTo(rfkMap)

    rfkMap.pm.addControls({
      position: 'topleft',
      drawMarker: true,
      drawPolyline: true,
      drawPolygon: true,
      drawRectangle: true,
      drawCircle: true,
      drawCircleMarker: false,
      editMode: true,
      dragMode: true,
      removalMode: true
    })

    if (locs.length > 0) {
      locs.forEach((loc, idx) => {
        renderRfkLocationOnMap(loc, idx)
      })
      if (rfkDrawnGroup.getLayers().length > 0) {
        try {
          rfkMap.fitBounds(rfkDrawnGroup.getBounds(), { padding: [30, 30] })
        } catch (e) {}
      }
    }

    rfkMap.on('pm:create', (e) => {
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

      const newLocItem = {
        id: null,
        nama_lokasi: selectedPekerjaanForm.value?.nama_pekerjaan || 'Lokasi Pekerjaan',
        jenis_geometry: jenisGeom,
        geojson: geojson,
        lat: lat,
        lng: lng,
        radius: radius
      }

      if (!formRealisasiData.value.lokasi_list) {
        formRealisasiData.value.lokasi_list = []
      }
      formRealisasiData.value.lokasi_list.push(newLocItem)
      rfkDrawnGroup.addLayer(layer)
    })
  })
}

const renderRfkLocationOnMap = (loc, idx) => {
  if (!rfkMap || !rfkDrawnGroup) return

  if (loc.geojson && loc.geojson.geometry) {
    try {
      const geoLayer = L.geoJSON(loc.geojson, {
        style: { color: '#308e87', weight: 3, opacity: 0.8, fillOpacity: 0.35 }
      })
      geoLayer.bindPopup(`<b>${loc.nama_lokasi || 'Lokasi Pekerjaan'}</b>`)
      rfkDrawnGroup.addLayer(geoLayer)
      return
    } catch (e) {}
  }

  if (loc.lat && loc.lng) {
    if (loc.jenis_geometry === 'Circle' && loc.radius) {
      const circleLayer = L.circle([loc.lat, loc.lng], {
        radius: loc.radius,
        color: '#308e87',
        fillColor: '#308e87',
        fillOpacity: 0.3
      }).bindPopup(`<b>${loc.nama_lokasi || 'Lokasi Pekerjaan'}</b>`)
      rfkDrawnGroup.addLayer(circleLayer)
    } else {
      const marker = L.marker([loc.lat, loc.lng])
        .bindPopup(`<b>${loc.nama_lokasi || 'Lokasi Pekerjaan'}</b>`)
      rfkDrawnGroup.addLayer(marker)
    }
  }
}

const clearAllLocations = () => {
  formRealisasiData.value.lokasi_list = []
  if (rfkDrawnGroup) {
    rfkDrawnGroup.clearLayers()
  }
}

const removeSingleLocation = (index) => {
  formRealisasiData.value.lokasi_list.splice(index, 1)
  initRfkMap()
}

const handleSaveLokasi = async () => {
  if (!selectedPekerjaanForm.value) return
  savingLokasi.value = true
  modalSaveSuccess.value = false
  try {
    const pekId = selectedPekerjaanForm.value.id
    await axios.put(`/api/rko/pekerjaan/${pekId}`, {
      lokasi: formRealisasiData.value.lokasi || null,
      lokasi_list: formRealisasiData.value.lokasi_list || []
    })
    const msg = 'Berhasil menyimpan lokasi pekerjaan dan data peta GIS!'
    modalSaveSuccessMsg.value = msg
    modalSaveSuccess.value = true
    triggerToast(msg)
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal menyimpan lokasi pekerjaan'
    triggerToast(msg)
  } finally {
    savingLokasi.value = false
  }
}

const handleSaveKontrak = async () => {
  if (!selectedPekerjaanForm.value) return
  savingKontrak.value = true
  modalSaveSuccess.value = false
  try {
    const res = await axios.post('/api/v1/rfk/kontrak/simpan', {
      id_pekerjaan: selectedPekerjaanForm.value.id,
      ...formKontrakData.value
    })
    const msg = res.data.message || 'Berhasil menyimpan data kontrak / SPK pekerjaan'
    modalSaveSuccessMsg.value = msg
    modalSaveSuccess.value = true
    triggerToast(msg)
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal menyimpan data kontrak'
    triggerToast(msg)
  } finally {
    savingKontrak.value = false
  }
}

watch(activeFormTab, (newTab) => {
  if (newTab === 'lokasi') {
    initRfkMap()
  }
})

watch(isFormModalMaximized, () => {
  if (activeFormTab.value === 'lokasi' && rfkMap) {
    nextTick(() => {
      rfkMap.invalidateSize()
    })
  }
})

const allPekerjaanList = computed(() => {
  if (!selectedMonthDetail.value?.data?.programs) return []
  const list = []
  for (const prog of selectedMonthDetail.value.data.programs) {
    for (const keg of (prog.kegiatan || [])) {
      const subList = keg.subkegiatan || keg.sub_kegiatan || []
      for (const sub of subList) {
        for (const pek of (sub.pekerjaan || [])) {
          list.push(pek)
        }
      }
    }
  }
  return list
})

const currentPekerjaanIndex = computed(() => {
  if (!selectedPekerjaanForm.value || allPekerjaanList.value.length === 0) return -1
  return allPekerjaanList.value.findIndex(p => p.id === selectedPekerjaanForm.value.id)
})

const hasPrevPekerjaan = computed(() => {
  return currentPekerjaanIndex.value > 0
})

const hasNextPekerjaan = computed(() => {
  return currentPekerjaanIndex.value >= 0 && currentPekerjaanIndex.value < allPekerjaanList.value.length - 1
})

const navigatePekerjaan = (direction) => {
  const idx = currentPekerjaanIndex.value
  if (idx < 0) return
  if (direction === 'prev' && hasPrevPekerjaan.value) {
    const targetPek = allPekerjaanList.value[idx - 1]
    openFormRealisasiModal(targetPek)
  } else if (direction === 'next' && hasNextPekerjaan.value) {
    const targetPek = allPekerjaanList.value[idx + 1]
    openFormRealisasiModal(targetPek)
  }
}
const dokumenList = ref([])
const loadingDokumenList = ref(false)
const uploadingFile = ref(false)
const uploadCategory = ref('foto') // 'foto', 'dokumen'
const uploadKeterangan = ref('')
const selectedFile = ref(null)
const deletingDokumenId = ref(null)

const fotoDokumenList = computed(() => {
  return dokumenList.value.filter(d => d.tipe_file === 'foto' || (d.nama_file && d.nama_file.match(/\.(jpg|jpeg|png|webp|gif)$/i)))
})

const berkasDokumenList = computed(() => {
  return dokumenList.value.filter(d => d.tipe_file !== 'foto' && (!d.nama_file || !d.nama_file.match(/\.(jpg|jpeg|png|webp|gif)$/i)))
})

const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const fetchDokumenList = async (id_pekerjaan, bulan) => {
  if (!id_pekerjaan || !bulan) return
  loadingDokumenList.value = true
  try {
    const res = await axios.get(`/api/v1/rfk/realisasi-dokumen/${id_pekerjaan}/${bulan}`)
    dokumenList.value = res.data.dokumen_list || []
  } catch (err) {
    console.error('Gagal memuat dokumen data dukung:', err)
  } finally {
    loadingDokumenList.value = false
  }
}

const handleFileSelect = (event) => {
  const files = event.target.files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
  } else {
    selectedFile.value = null
  }
}

const handleUploadDokumen = async () => {
  if (!selectedFile.value || !selectedPekerjaanForm.value || !selectedMonthDetail.value) return
  uploadingFile.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('id_pekerjaan', selectedPekerjaanForm.value.id)
    formData.append('id_sub_pd', selectedOpdModal.value?.id_sub_pd || 0)
    formData.append('bulan', selectedMonthDetail.value.bulan)
    formData.append('tipe_file', uploadCategory.value)
    if (uploadKeterangan.value) {
      formData.append('keterangan', uploadKeterangan.value)
    }

    const res = await axios.post('/api/v1/rfk/realisasi-dokumen/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    const msg = res.data.message || 'Berhasil mengunggah data dukung'
    successMessage.value = msg
    triggerToast(msg)
    uploadKeterangan.value = ''
    selectedFile.value = null

    await fetchDokumenList(selectedPekerjaanForm.value.id, selectedMonthDetail.value.bulan)
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal mengunggah file data dukung'
    errorMessage.value = msg
  } finally {
    uploadingFile.value = false
  }
}

const handleDeleteDokumen = async (dokId) => {
  if (!dokId) return
  deletingDokumenId.value = dokId
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const res = await axios.delete(`/api/v1/rfk/realisasi-dokumen/${dokId}`)
    const msg = res.data.message || 'Berhasil menghapus dokumen data dukung'
    successMessage.value = msg
    triggerToast(msg)
    await fetchDokumenList(selectedPekerjaanForm.value.id, selectedMonthDetail.value.bulan)
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal menghapus dokumen data dukung'
    errorMessage.value = msg
  } finally {
    deletingDokumenId.value = null
  }
}

const openFormRealisasiModal = async (pek) => {
  if (!pek || !selectedMonthDetail.value) return
  const bulan = selectedMonthDetail.value.bulan
  selectedPekerjaanForm.value = pek
  activeFormTab.value = 'realisasi'
  dokumenList.value = []
  selectedFile.value = null
  uploadKeterangan.value = ''
  modalSaveSuccess.value = false
  modalSaveSuccessMsg.value = ''
  loadingRealisasiForm.value = true

  fetchDokumenList(pek.id, bulan)

  formRealisasiData.value = {
    id_pekerjaan: pek.id,
    id_sub_pd: selectedOpdModal.value?.id_sub_pd || 0,
    bulan: bulan,
    keuangan: pek.keuangan_bulan_ini || 0,
    fisik: pek.realisasi_fisik || 0,
    masalah: '',
    upaya: '',
    keuangan_lalu: 0,
    fisik_lalu: 0,
    target_fisik_bulan_ini: 0,
    tagging: [],
    lokasi: '',
    lokasi_list: []
  }

  formKontrakData.value = {
    nama_ppk: '',
    nama_pptk: '',
    nama_pokja: '',
    nama_pphp: '',
    nilai_hps: 0,
    nilai_kontrak: 0,
    sisa_anggaran: pek.anggaran || 0,
    nama_penyedia: '',
    alamat_penyedia: '',
    pimpinan_penyedia: '',
    npwp_penyedia: '',
    nomor_kontrak: '',
    tgl_kontrak_awal: '',
    tgl_kontrak_akhir: '',
    nomor_spmk: '',
    tgl_spmk_awal: '',
    tgl_spmk_akhir: '',
    tgl_adendum_awal: '',
    tgl_adendum_akhir: '',
    status_kontrak: 'Dalam Proses'
  }

  try {
    const res = await axios.get(`/api/v1/rfk/realisasi/${pek.id}/${bulan}`)
    const data = res.data
    if (data) {
      formRealisasiData.value.keuangan_lalu = data.keuangan_lalu || 0
      formRealisasiData.value.fisik_lalu = data.fisik_lalu || 0
      formRealisasiData.value.target_fisik_bulan_ini = data.target_fisik_bulan_ini || 0
      formRealisasiData.value.tagging = data.tagging || []
      formRealisasiData.value.lokasi = data.lokasi || ''
      formRealisasiData.value.lokasi_list = data.lokasi_list || []

      if (data.kontrak) {
        formKontrakData.value = {
          nama_ppk: data.kontrak.nama_ppk || '',
          nama_pptk: data.kontrak.nama_pptk || '',
          nama_pokja: data.kontrak.nama_pokja || '',
          nama_pphp: data.kontrak.nama_pphp || '',
          nilai_hps: data.kontrak.nilai_hps || 0,
          nilai_kontrak: data.kontrak.nilai_kontrak || 0,
          sisa_anggaran: data.kontrak.sisa_anggaran || Math.max(0, (pek.anggaran || 0) - (data.kontrak.nilai_kontrak || 0)),
          nama_penyedia: data.kontrak.nama_penyedia || '',
          alamat_penyedia: data.kontrak.alamat_penyedia || '',
          pimpinan_penyedia: data.kontrak.pimpinan_penyedia || '',
          npwp_penyedia: data.kontrak.npwp_penyedia || '',
          nomor_kontrak: data.kontrak.nomor_kontrak || '',
          tgl_kontrak_awal: data.kontrak.tgl_kontrak_awal || '',
          tgl_kontrak_akhir: data.kontrak.tgl_kontrak_akhir || '',
          nomor_spmk: data.kontrak.nomor_spmk || '',
          tgl_spmk_awal: data.kontrak.tgl_spmk_awal || '',
          tgl_spmk_akhir: data.kontrak.tgl_spmk_akhir || '',
          tgl_adendum_awal: data.kontrak.tgl_adendum_awal || '',
          tgl_adendum_akhir: data.kontrak.tgl_adendum_akhir || '',
          status_kontrak: data.kontrak.status_kontrak || 'Dalam Proses'
        }
      }

      if (data.realisasi) {
        formRealisasiData.value.keuangan = data.realisasi.keuangan || 0
        formRealisasiData.value.fisik = data.realisasi.fisik || 0
        formRealisasiData.value.masalah = data.realisasi.masalah || ''
        formRealisasiData.value.upaya = data.realisasi.upaya || ''
      } else {
        formRealisasiData.value.fisik = data.fisik_lalu || 0
      }
    }
  } catch (err) {
    console.error('Gagal mengambil rincian realisasi pekerjaan:', err)
  } finally {
    loadingRealisasiForm.value = false
  }
}

const totalKeuanganSdBulanIni = computed(() => {
  return (formRealisasiData.value.keuangan_lalu || 0) + (formRealisasiData.value.keuangan || 0)
})

const toastShow = ref(false)
const toastMessage = ref('')
let toastTimer = null

const triggerToast = (message, duration = 3500) => {
  toastMessage.value = message
  toastShow.value = true
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastShow.value = false
  }, duration)
}

const handleSaveRealisasi = async () => {
  if (!selectedPekerjaanForm.value || !selectedMonthDetail.value) return
  savingRealisasi.value = true
  errorMessage.value = ''
  successMessage.value = ''
  modalSaveSuccess.value = false

  try {
    const res = await axios.post('/api/v1/rfk/realisasi/simpan', {
      id_pekerjaan: formRealisasiData.value.id_pekerjaan,
      id_sub_pd: formRealisasiData.value.id_sub_pd,
      bulan: formRealisasiData.value.bulan,
      keuangan: Number(formRealisasiData.value.keuangan || 0),
      fisik: Number(formRealisasiData.value.fisik || 0),
      masalah: formRealisasiData.value.masalah || null,
      upaya: formRealisasiData.value.upaya || null
    })

    const msg = res.data.message || 'Berhasil menyimpan realisasi pekerjaan'
    modalSaveSuccessMsg.value = msg
    modalSaveSuccess.value = true
    triggerToast(msg)

    // Keep window open as requested & refresh background month detail treeview
    await selectMonthAndShowDetail(selectedOpdModal.value, selectedMonthDetail.value.bulan)
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal menyimpan realisasi pekerjaan'
    errorMessage.value = msg
  } finally {
    savingRealisasi.value = false
  }
}

const showDeleteConfirm = ref(false)
const monthToDelete = ref(null)
const deletingBulan = ref(null)

const confirmDeleteLaporan = (opd, bulan) => {
  monthToDelete.value = { opd, bulan }
  showDeleteConfirm.value = true
}

const handleDeleteLaporan = async () => {
  if (!monthToDelete.value) return
  const { opd, bulan } = monthToDelete.value
  deletingBulan.value = bulan
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const res = await axios.delete(`/api/v1/rfk/laporan/${opd.id_sub_pd}/${bulan}`, {
      params: { tahun: selectedTahun.value }
    })
    successMessage.value = res.data.message || `Berhasil menghapus Laporan RFK bulan ${monthNames[bulan - 1]}`
    showDeleteConfirm.value = false
    monthToDelete.value = null

    await fetchRfkData()

    if (selectedOpdModal.value) {
      const updatedOpd = opdList.value.find(o => o.id_sub_pd === selectedOpdModal.value.id_sub_pd)
      if (updatedOpd) {
        selectedOpdModal.value = updatedOpd
      }
    }
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal menghapus Laporan RFK'
    errorMessage.value = msg
  } finally {
    deletingBulan.value = null
  }
}

const creatingLaporan = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const monthShorts = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
const monthNames = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

const getCreatedMonthsDesc = (maxMonth) => {
  if (!maxMonth || maxMonth <= 0) return []
  const months = []
  for (let m = maxMonth; m >= 1; m--) {
    months.push(m)
  }
  return months
}

const navigateToView = (viewName) => {
  currentView.value = viewName
}

const selectOpdAndShowMonths = (opd) => {
  errorMessage.value = ''
  successMessage.value = ''
  selectedOpdModal.value = opd
  currentView.value = 'opd_months'
}

const selectMonthAndShowDetail = async (opd, bulan) => {
  if (!opd || !bulan) return
  loadingMonthDetail.value = true
  selectedOpdModal.value = opd
  selectedMonthDetail.value = {
    opd,
    bulan,
    data: null
  }
  monthDetailExpandedNodes.value = {}
  currentView.value = 'month_detail'

  try {
    const res = await axios.get(`/api/v1/rfk/laporan-detail/${opd.id_sub_pd}/${bulan}`, {
      params: { tahun: selectedTahun.value }
    })
    selectedMonthDetail.value.data = res.data
    
    if (res.data?.programs) {
      res.data.programs.forEach(prog => {
        monthDetailExpandedNodes.value['prog-' + prog.kode] = true
        if (prog.kegiatan) {
          prog.kegiatan.forEach(keg => {
            monthDetailExpandedNodes.value['keg-' + keg.kode] = true
            if (keg.subkegiatan) {
              keg.subkegiatan.forEach(sub => {
                monthDetailExpandedNodes.value['sub-' + sub.kode] = true
              })
            }
          })
        }
      })
    }
  } catch (err) {
    console.error('Gagal memuat detail laporan RFK bulanan:', err)
  } finally {
    loadingMonthDetail.value = false
  }
}

const toggleMonthDetailNode = (nodeId) => {
  monthDetailExpandedNodes.value[nodeId] = !monthDetailExpandedNodes.value[nodeId]
}

const toggleAllMonthDetailNodes = (expand) => {
  if (!selectedMonthDetail.value?.data?.programs) return
  const newState = {}
  if (expand) {
    selectedMonthDetail.value.data.programs.forEach(prog => {
      newState['prog-' + prog.kode] = true
      if (prog.kegiatan) {
        prog.kegiatan.forEach(keg => {
          newState['keg-' + keg.kode] = true
          if (keg.subkegiatan) {
            keg.subkegiatan.forEach(sub => {
              newState['sub-' + sub.kode] = true
            })
          }
        })
      }
    })
  }
  monthDetailExpandedNodes.value = newState
}

const formatRupiah = (val) => {
  if (!val || isNaN(val)) return 'Rp 0'
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val)
}

const formatPercent = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0%'
  return `${Number(val).toFixed(2)}%`
}

const handleBuatLaporan = async (opd) => {
  if (!opd) return
  creatingLaporan.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const res = await axios.post('/api/v1/rfk/laporan/buat', {
      id_sub_pd: opd.id_sub_pd,
      tahun: selectedTahun.value
    })
    successMessage.value = res.data.message || 'Berhasil membuat Draf Laporan RFK'
    await fetchRfkData()

    if (selectedOpdModal.value) {
      const updatedOpd = opdList.value.find(o => o.id_sub_pd === selectedOpdModal.value.id_sub_pd)
      if (updatedOpd) {
        selectedOpdModal.value = updatedOpd
      }
    }
  } catch (err) {
    const msg = err.response?.data?.detail || 'Gagal membuat Laporan RFK'
    errorMessage.value = msg
  } finally {
    creatingLaporan.value = false
  }
}

const fetchRfkData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/v1/rfk/opd-laporan', {
      params: { tahun: selectedTahun.value }
    })
    summary.value = res.data.summary || {}
    opdList.value = res.data.opd_list || []
  } catch (err) {
    console.error('Gagal memuat data laporan RFK OPD:', err)
  } finally {
    loading.value = false
  }
}

const countMainOpd = computed(() => {
  return opdList.value.filter(o => o.is_pd === 1).length
})

const countSubOpd = computed(() => {
  return opdList.value.filter(o => o.is_pd === 0 || o.is_pd === null).length
})

const filteredOpdList = computed(() => {
  let list = opdList.value

  if (opdFilterCategory.value === 'main') {
    list = list.filter(o => o.is_pd === 1)
  } else if (opdFilterCategory.value === 'sub') {
    list = list.filter(o => o.is_pd === 0 || o.is_pd === null)
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(o => 
      (o.kode && o.kode.toLowerCase().includes(q)) || 
      (o.nama_pd && o.nama_pd.toLowerCase().includes(q)) ||
      (o.nama_pd_singkat && o.nama_pd_singkat.toLowerCase().includes(q))
    )
  }

  return list
})

const formatAveragePerMonth = computed(() => {
  if (!summary.value.total_laporan_terkirim) return '0.0'
  return (summary.value.total_laporan_terkirim / 12).toFixed(1)
})

const highestReportingMonth = computed(() => {
  const counts = summary.value.bulan_terkirim || {}
  let maxMonth = 1
  let maxVal = 0

  for (let m = 1; m <= 12; m++) {
    const cnt = counts[m] || 0
    if (cnt > maxVal) {
      maxVal = cnt
      maxMonth = m
    }
  }

  return {
    name: monthNames[maxMonth - 1] || 'Januari',
    count: maxVal
  }
})

onMounted(() => {
  fetchRfkData()
})
</script>
