<template>
  <div class="space-y-6 pb-16">

    <!-- Header Banner -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] dark:from-[#0f1729] dark:via-[#162032] dark:to-[#1a2940] p-6 sm:p-8 text-white shadow-xl shadow-[#308e87]/10">
      <div class="absolute inset-0 opacity-[0.04]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;40&quot; height=&quot;40&quot; viewBox=&quot;0 0 40 40&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot; fill-rule=&quot;evenodd&quot;%3E%3Cpath d=&quot;M0 40L40 0H20L0 20M40 40V20L20 40&quot;/%3E%3C/g%3E%3C/svg%3E')"></div>
      
      <div class="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div>
          <div class="flex flex-wrap items-center gap-2 mb-3">
            <span class="px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider bg-[#3aada4] text-white shadow-md shadow-[#3aada4]/30">
              Dokumen Perencanaan
            </span>
            <span class="px-2.5 py-0.5 rounded-lg text-xs font-bold bg-white/10 text-white/90 border border-white/15">
              Periode 2025 – 2029 (5 Tahunan)
            </span>
            <span class="text-xs text-white/60 font-semibold">• Kota Tegal</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-black tracking-tight text-white">
            RPJMD Kota Tegal
          </h1>
          <p class="text-xs sm:text-sm text-[#a7ded9] dark:text-[#a0c5e8] mt-1.5 font-medium max-w-2xl leading-relaxed">
            Rencana Pembangunan Jangka Menengah Daerah — Penjabaran visi, misi, dan program Kepala Daerah 5 tahunan yang memuat tujuan, sasaran, strategi, IKU, IKD, serta proyeksi kerangka pendanaan.
          </p>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-wrap items-center gap-2.5 shrink-0">
          <button 
            @click="handleExport"
            class="px-4 py-2.5 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/20 text-white border border-white/20 transition-all flex items-center space-x-2 active:scale-95 shadow-sm"
          >
            <Download class="w-4 h-4" />
            <span>Ekspor RPJMD</span>
          </button>
          <button 
            @click="openAddModal"
            class="px-4 py-2.5 rounded-xl text-xs font-black bg-[#f39159] hover:bg-[#e27b41] text-white transition-all flex items-center space-x-2 active:scale-95 shadow-lg shadow-[#f39159]/30"
          >
            <Plus class="w-4 h-4" />
            <span>Tambah Data {{ currentTabTitle }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Summary KPI Cards -->
    <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
      <div 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        class="bg-white dark:bg-[#141d30] border rounded-2xl p-3 transition-all cursor-pointer hover:shadow-md"
        :class="activeTab === tab.id ? 'border-[#308e87] ring-2 ring-[#308e87]/20 dark:ring-[#308e87]/40 shadow-sm bg-[#308e87]/5' : 'border-slate-200/80 dark:border-slate-800'"
      >
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[10px] font-bold text-slate-500 dark:text-slate-400 truncate">{{ tab.shortLabel }}</span>
          <component :is="tab.icon" class="w-3.5 h-3.5 text-[#308e87] dark:text-[#3aada4]" />
        </div>
        <p class="text-xl font-black text-slate-900 dark:text-white">{{ tab.count }}</p>
        <p class="text-[9px] text-slate-400 dark:text-slate-500 font-semibold truncate">{{ tab.subtitle }}</p>
      </div>
    </div>

    <!-- 8 Tab Header Navigation -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-1.5 shadow-sm">
      <div class="flex items-center overflow-x-auto no-scrollbar gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-3.5 py-2.5 rounded-xl font-bold text-xs whitespace-nowrap transition-all flex items-center space-x-2 shrink-0 cursor-pointer"
          :class="activeTab === tab.id 
            ? 'bg-[#308e87] text-white shadow-md shadow-[#308e87]/25' 
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/80'"
        >
          <component :is="tab.icon" class="w-3.5 h-3.5" />
          <span>{{ tab.label }}</span>
          <span 
            class="px-1.5 py-0.5 rounded-full text-[10px] font-black"
            :class="activeTab === tab.id ? 'bg-white/20 text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'"
          >
            {{ tab.count }}
          </span>
        </button>
      </div>
    </div>

    <!-- ==================== TAB 1: VISI (MODULAR COMPONENT) ==================== -->
    <RpjmdVisiTab v-if="activeTab === 'visi'" ref="visiTabRef" />

    <!-- ==================== TAB 2: MISI (MODULAR COMPONENT) ==================== -->
    <RpjmdMisiTab v-else-if="activeTab === 'misi'" ref="misiTabRef" />

    <!-- ==================== TAB 3: TUJUAN (MODULAR COMPONENT - TREE TABLE) ==================== -->
    <RpjmdTujuanTab v-else-if="activeTab === 'tujuan'" ref="tujuanTabRef" />

    <!-- ==================== TAB 4: SASARAN (MODULAR COMPONENT - TREE TABLE) ==================== -->
    <RpjmdSasaranTab v-else-if="activeTab === 'sasaran'" ref="sasaranTabRef" />

    <!-- ==================== TAB 5: PROGRAM ==================== -->
    <div v-if="activeTab === 'program'" class="space-y-4">
      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-sm">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Cari program atau Perangkat Daerah..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>
        <div class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          Menampilkan <strong>{{ filteredProgram.length }} Program RPJMD</strong>
        </div>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th class="py-3.5 px-4 w-28 text-center">Kode Program</th>
                <th class="py-3.5 px-4">Nama Program Pembangunan</th>
                <th class="py-3.5 px-4">Indikator Kinerja Program</th>
                <th class="py-3.5 px-4 w-48">Perangkat Daerah Pengampu</th>
                <th class="py-3.5 px-4 text-right w-36">Pagu Indikatif 5 Thn</th>
                <th class="py-3.5 px-4 text-center w-24">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 text-xs">
              <tr v-for="item in filteredProgram" :key="item.id" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
                <td class="py-3.5 px-4 text-center font-black text-indigo-600 dark:text-indigo-400">{{ item.kode }}</td>
                <td class="py-3.5 px-4 font-bold text-slate-900 dark:text-white">{{ item.nama }}</td>
                <td class="py-3.5 px-4 text-slate-600 dark:text-slate-300 font-medium">{{ item.indikator }}</td>
                <td class="py-3.5 px-4 font-semibold text-slate-700 dark:text-slate-300">{{ item.opd }}</td>
                <td class="py-3.5 px-4 text-right font-black text-emerald-600 dark:text-emerald-400">{{ formatRupiah(item.pagu5Tahun) }}</td>
                <td class="py-3.5 px-4 text-center">
                  <div class="flex items-center justify-center space-x-1">
                    <button @click="handleAction('edit', 'Program', item)" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"><Edit3 class="w-3.5 h-3.5" /></button>
                    <button @click="handleAction('delete', 'Program', item)" class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30"><Trash2 class="w-3.5 h-3.5" /></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ==================== TAB 6: IKU ==================== -->
    <div v-if="activeTab === 'iku'" class="space-y-4">
      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-sm">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Cari indikator kinerja utama (IKU)..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>
        <div class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          Total <strong>{{ filteredIku.length }} Indikator Kinerja Utama (IKU)</strong>
        </div>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th class="py-3.5 px-4 w-16 text-center">No</th>
                <th class="py-3.5 px-4">Indikator Kinerja Utama (IKU)</th>
                <th class="py-3.5 px-4 text-center w-20">Satuan</th>
                <th class="py-3.5 px-4 text-center w-20">2025</th>
                <th class="py-3.5 px-4 text-center w-20">2026</th>
                <th class="py-3.5 px-4 text-center w-20">2027</th>
                <th class="py-3.5 px-4 text-center w-20">2028</th>
                <th class="py-3.5 px-4 text-center w-24">Target 2029</th>
                <th class="py-3.5 px-4 w-40">Penanggung Jawab</th>
                <th class="py-3.5 px-4 text-center w-20">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 text-xs">
              <tr v-for="(item, idx) in filteredIku" :key="item.id" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
                <td class="py-3.5 px-4 text-center font-bold text-slate-400">{{ idx + 1 }}</td>
                <td class="py-3.5 px-4 font-bold text-slate-900 dark:text-white">{{ item.indikator }}</td>
                <td class="py-3.5 px-4 text-center text-slate-500 font-medium">{{ item.satuan }}</td>
                <td class="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400">{{ item.t2025 }}</td>
                <td class="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400">{{ item.t2026 }}</td>
                <td class="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400">{{ item.t2027 }}</td>
                <td class="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400">{{ item.t2028 }}</td>
                <td class="py-3.5 px-4 text-center">
                  <span class="px-2.5 py-1 rounded-lg font-black text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800">
                    {{ item.targetAkhir }}
                  </span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 dark:text-slate-300 font-medium">{{ item.opd }}</td>
                <td class="py-3.5 px-4 text-center">
                  <button @click="handleAction('edit', 'IKU', item)" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"><Edit3 class="w-3.5 h-3.5" /></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ==================== TAB 7: IKD ==================== -->
    <div v-if="activeTab === 'ikd'" class="space-y-4">
      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-sm">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Cari indikator kinerja daerah (IKD)..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>
        <div class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          Total <strong>{{ filteredIkd.length }} Indikator Kinerja Daerah (IKD)</strong>
        </div>
      </div>

      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th class="py-3.5 px-4 w-16 text-center">Kode</th>
                <th class="py-3.5 px-4">Aspek &amp; Indikator Kinerja Daerah (IKD)</th>
                <th class="py-3.5 px-4 w-36">Kategori Aspek</th>
                <th class="py-3.5 px-4 text-center w-20">Satuan</th>
                <th class="py-3.5 px-4 text-center w-24">Baseline 2024</th>
                <th class="py-3.5 px-4 text-center w-24">Target 2029</th>
                <th class="py-3.5 px-4 w-40">Perangkat Daerah</th>
                <th class="py-3.5 px-4 text-center w-20">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 text-xs">
              <tr v-for="item in filteredIkd" :key="item.id" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
                <td class="py-3.5 px-4 text-center font-black text-[#f39159]">{{ item.kode }}</td>
                <td class="py-3.5 px-4 font-bold text-slate-900 dark:text-white">{{ item.indikator }}</td>
                <td class="py-3.5 px-4">
                  <span class="px-2.5 py-0.5 rounded-md text-[10px] font-bold bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4]">
                    {{ item.kategori }}
                  </span>
                </td>
                <td class="py-3.5 px-4 text-center text-slate-500 font-medium">{{ item.satuan }}</td>
                <td class="py-3.5 px-4 text-center text-slate-600 dark:text-slate-400 font-semibold">{{ item.baseline }}</td>
                <td class="py-3.5 px-4 text-center">
                  <span class="px-2 py-0.5 rounded-lg font-black text-indigo-700 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800">
                    {{ item.target2029 }}
                  </span>
                </td>
                <td class="py-3.5 px-4 text-slate-700 dark:text-slate-300 font-medium">{{ item.opd }}</td>
                <td class="py-3.5 px-4 text-center">
                  <button @click="handleAction('edit', 'IKD', item)" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"><Edit3 class="w-3.5 h-3.5" /></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ==================== TAB 8: PROYEKSI KERANGKA PENDANAAN ==================== -->
    <div v-if="activeTab === 'pendanaan'" class="space-y-6">
      
      <!-- Pendanaan Top Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-gradient-to-br from-[#1a4845] to-[#308e87] text-white rounded-2xl p-5 shadow-lg">
          <span class="text-xs text-white/75 font-semibold">Total Proyeksi Pendanaan 5 Tahun</span>
          <p class="text-2xl font-black mt-1">Rp 6,45 Triliun</p>
          <span class="text-[10px] text-white/60 mt-1 block">Rata-rata Rp 1,29 Triliun / Tahun</span>
        </div>
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm">
          <span class="text-xs text-slate-500 font-semibold">Proyeksi Pendapatan Asli Daerah (PAD)</span>
          <p class="text-2xl font-black text-slate-900 dark:text-white mt-1">Rp 2,15 Triliun</p>
          <span class="text-[10px] text-emerald-600 font-bold mt-1 block">Kontribusi 33.3% dari Total APBD</span>
        </div>
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm">
          <span class="text-xs text-slate-500 font-semibold">Alokasi Belanja Modal &amp; Program Prioritas</span>
          <p class="text-2xl font-black text-[#f39159] mt-1">Rp 2,80 Triliun</p>
          <span class="text-[10px] text-slate-400 font-semibold mt-1 block">Infrastruktur, Pendidikan &amp; Kesehatan</span>
        </div>
      </div>

      <!-- Pendanaan Table Per Tahun -->
      <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <h4 class="text-sm font-black text-slate-900 dark:text-white">Proyeksi Kerangka Pendanaan RPJMD Per Tahun (2025–2029)</h4>
          <span class="text-xs text-slate-400 font-medium">Satuan: Miliar Rupiah</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 text-[11px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th class="py-3.5 px-4">Komponen Anggaran / Pendanaan</th>
                <th class="py-3.5 px-4 text-right">2025</th>
                <th class="py-3.5 px-4 text-right">2026</th>
                <th class="py-3.5 px-4 text-right">2027</th>
                <th class="py-3.5 px-4 text-right">2028</th>
                <th class="py-3.5 px-4 text-right">2029</th>
                <th class="py-3.5 px-4 text-right">Total 5 Tahun</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60 text-xs">
              <tr v-for="item in pendanaanList" :key="item.id" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors">
                <td class="py-3.5 px-4 font-bold text-slate-900 dark:text-white">{{ item.komponen }}</td>
                <td class="py-3.5 px-4 text-right font-medium text-slate-600 dark:text-slate-300">{{ item.y2025 }}</td>
                <td class="py-3.5 px-4 text-right font-medium text-slate-600 dark:text-slate-300">{{ item.y2026 }}</td>
                <td class="py-3.5 px-4 text-right font-medium text-slate-600 dark:text-slate-300">{{ item.y2027 }}</td>
                <td class="py-3.5 px-4 text-right font-medium text-slate-600 dark:text-slate-300">{{ item.y2028 }}</td>
                <td class="py-3.5 px-4 text-right font-medium text-slate-600 dark:text-slate-300">{{ item.y2029 }}</td>
                <td class="py-3.5 px-4 text-right font-black text-emerald-600 dark:text-emerald-400">{{ item.total }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Form (Tambah / Edit Mock) -->
    <div 
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-lg shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Plus class="w-4 h-4" />
            </div>
            <h3 class="text-base font-black text-slate-900 dark:text-white">
              {{ modalTitle }}
            </h3>
          </div>
          <button 
            @click="showModal = false"
            class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            ✕
          </button>
        </div>

        <div class="space-y-3.5 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kode / Nomor</label>
            <input 
              v-model="formModel.kode"
              type="text" 
              placeholder="Contoh: T-01 / S-01" 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
            />
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian / Deskripsi</label>
            <textarea 
              v-model="formModel.uraian"
              rows="3" 
              placeholder="Masukkan uraian detail..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Indikator Kinerja</label>
              <input 
                v-model="formModel.indikator"
                type="text" 
                placeholder="Indikator..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Target Akhir (2029)</label>
              <input 
                v-model="formModel.target"
                type="text" 
                placeholder="Target..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
              />
            </div>
          </div>
        </div>

        <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
          <button 
            @click="showModal = false"
            class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200"
          >
            Batal
          </button>
          <button 
            @click="saveFormData"
            class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25"
          >
            Simpan Data
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Swal from 'sweetalert2'
import { 
  Compass, Flag, Target, CheckCircle2, Layers, 
  BarChart3, Award, Coins, Plus, Download, Search, 
  Edit3, Trash2, FileCheck, Calendar, Sparkles 
} from 'lucide-vue-next'

// Modular Components per Menu Tab
import RpjmdVisiTab from '@/components/rpjmd/RpjmdVisiTab.vue'
import RpjmdMisiTab from '@/components/rpjmd/RpjmdMisiTab.vue'
import RpjmdTujuanTab from '@/components/rpjmd/RpjmdTujuanTab.vue'
import RpjmdSasaranTab from '@/components/rpjmd/RpjmdSasaranTab.vue'

const activeTab = ref('visi')
const searchQuery = ref('')
const showModal = ref(false)
const modalTitle = ref('')
const formModel = ref({ kode: '', uraian: '', indikator: '', target: '' })

const visiTabRef = ref(null)
const misiTabRef = ref(null)
const tujuanTabRef = ref(null)
const sasaranTabRef = ref(null)

// 8 Tab Navigation
const tabs = computed(() => [
  { id: 'visi', label: 'Visi', shortLabel: 'Visi', subtitle: 'Visi 5 Thn', icon: Compass, count: 1 },
  { id: 'misi', label: 'Misi', shortLabel: 'Misi', subtitle: 'Misi Daerah', icon: Flag, count: misiTabRef.value?.misiList?.length || 7 },
  { id: 'tujuan', label: 'Tujuan', shortLabel: 'Tujuan', subtitle: 'Tree Tabel', icon: Target, count: tujuanTabRef.value?.tujuanList?.length || 9 },
  { id: 'sasaran', label: 'Sasaran', shortLabel: 'Sasaran', subtitle: 'Tree Tabel', icon: CheckCircle2, count: sasaranTabRef.value?.sasaranList?.length || 24 },
  { id: 'program', label: 'Program', shortLabel: 'Program', subtitle: 'Program Pembangunan', icon: Layers, count: programList.value.length },
  { id: 'iku', label: 'IKU', shortLabel: 'IKU', subtitle: 'Indikator Utama', icon: BarChart3, count: ikuList.value.length },
  { id: 'ikd', label: 'IKD', shortLabel: 'IKD', subtitle: 'Indikator Daerah', icon: Award, count: ikdList.value.length },
  { id: 'pendanaan', label: 'Proyeksi Kerangka Pendanaan', shortLabel: 'Pendanaan', subtitle: 'Proyeksi APBD', icon: Coins, count: pendanaanList.value.length }
])

const currentTabTitle = computed(() => {
  const match = tabs.value.find(t => t.id === activeTab.value)
  return match ? match.label : 'Data'
})

// 3. DATA TUJUAN
const tujuanList = ref([
  { id: 1, kode: 'T.01', kodeMisi: '1', uraian: 'Meningkatkan Derajat Kesehatan dan Kualitas Pendidikan Masyarakat Kota Tegal', indikator: 'Indeks Pembangunan Manusia (IPM)', satuan: 'Poin', targetAkhir: '79.80' },
  { id: 2, kode: 'T.02', kodeMisi: '1', uraian: 'Menurunkan Angka Kemiskinan dan Kemiskinan Ekstrem', indikator: 'Persentase Penduduk Miskin', satuan: '%', targetAkhir: '6.20' },
  { id: 3, kode: 'T.03', kodeMisi: '2', uraian: 'Meningkatkan Pertumbuhan Ekonomi Daerah dan Serapan Tenaga Kerja', indikator: 'Laju Pertumbuhan Ekonomi (LPE)', satuan: '%', targetAkhir: '5.85' },
  { id: 4, kode: 'T.04', kodeMisi: '3', uraian: 'Meningkatkan Kualitas dan Ketahanan Infrastruktur Wilayah Pesisir dan Perkotaan', indikator: 'Indeks Infrastruktur Daerah', satuan: 'Skor', targetAkhir: '84.50' },
  { id: 5, kode: 'T.05', kodeMisi: '4', uraian: 'Mewujudkan Akuntabilitas Birokrasi dan Kualitas Layanan Publik yang Prima', indikator: 'Nilai SAKIP & Indeks SPBE', satuan: 'Skor', targetAkhir: 'A (85.00)' }
])

// 4. DATA SASARAN
const sasaranList = ref([
  { id: 1, kode: 'S.01', kodeTujuan: 'T.01', uraian: 'Meningkatnya Akses dan Mutu Layanan Pendidikan Usia Dini hingga Menengah', indikator: 'Harapan Lama Sekolah (HLS)', satuan: 'Tahun', target2029: '14.20' },
  { id: 2, kode: 'S.02', kodeTujuan: 'T.01', uraian: 'Meningkatnya Status Kesehatan Ibu, Anak, dan Bebas Stunting', indikator: 'Prevalensi Stunting Balita', satuan: '%', target2029: '8.50' },
  { id: 3, kode: 'S.03', kodeTujuan: 'T.03', uraian: 'Meningkatnya Produksi dan Nilai Tambah Hasil Tangkapan Perikanan Maritim', indikator: 'Nilai Produksi Perikanan', satuan: 'Miliar Rp', target2029: '850.00' },
  { id: 4, kode: 'S.04', kodeTujuan: 'T.04', uraian: 'Menurunnya Luas Wilayah Terdampak Banjir Rob dan Genangan Pasang', indikator: 'Penurunan Luas Wilayah Genangan', satuan: 'Hektar', target2029: '185.00' }
])

// 5. DATA PROGRAM
const programList = ref([
  { id: 1, kode: 'PRG.01.01', nama: 'Program Pengelolaan Pendidikan dan Bantuan Siswa Miskin', indikator: 'Persentase Kelulusan dan Angka Partisipasi Murni', opd: 'Dinas Pendidikan dan Kebudayaan', pagu5Tahun: 425000000000 },
  { id: 2, kode: 'PRG.01.02', nama: 'Program Pemenuhan Upaya Kesehatan Perorangan dan Masyarakat', indikator: 'Cakupan Layanan Kesehatan Dasar & Rujukan', opd: 'Dinas Kesehatan', pagu5Tahun: 580000000000 },
  { id: 3, kode: 'PRG.02.01', nama: 'Program Pengembangan Kapasitas Daya Saing Perikanan Tangkap', indikator: 'Volume Produksi Perikanan Tangkap', opd: 'DKPPP Kota Tegal', pagu5Tahun: 120000000000 },
  { id: 4, kode: 'PRG.03.01', nama: 'Program Pengendalian Banjir, Rob, dan Polder Perkotaan', indikator: 'Panjang Tanggul & Pompa Polder Beroperasi', opd: 'DPUPR Kota Tegal', pagu5Tahun: 340000000000 },
  { id: 5, kode: 'PRG.04.01', nama: 'Program Penyelenggaraan Sistem Pemerintahan Berbasis Elektronik', indikator: 'Indeks Kematangan SPBE', opd: 'Diskominfo Kota Tegal', pagu5Tahun: 65000000000 }
])

// 6. DATA IKU
const ikuList = ref([
  { id: 1, indikator: 'Indeks Pembangunan Manusia (IPM)', satuan: 'Poin', t2025: '76.80', t2026: '77.50', t2027: '78.25', t2028: '79.00', targetAkhir: '79.80', opd: 'Bapperida & OPD Terkait' },
  { id: 2, indikator: 'Laju Pertumbuhan Ekonomi (LPE)', satuan: '%', t2025: '5.20', t2026: '5.40', t2027: '5.55', t2028: '5.70', targetAkhir: '5.85', opd: 'Bapperida & Dinas Koperasi UKM' },
  { id: 3, indikator: 'Tingkat Kemiskinan', satuan: '%', t2025: '7.40', t2026: '7.10', t2027: '6.80', t2028: '6.50', targetAkhir: '6.20', opd: 'Dinas Sosial & Bapperida' },
  { id: 4, indikator: 'Tingkat Pengangguran Terbuka (TPT)', satuan: '%', t2025: '6.80', t2026: '6.40', t2027: '6.00', t2028: '5.60', targetAkhir: '5.20', opd: 'Disnakerin Kota Tegal' },
  { id: 5, indikator: 'Indeks Kualitas Lingkungan Hidup (IKLH)', satuan: 'Skor', t2025: '69.00', t2026: '70.50', t2027: '72.00', t2028: '73.50', targetAkhir: '75.00', opd: 'DLH Kota Tegal' }
])

// 7. DATA IKD
const ikdList = ref([
  { id: 1, kode: 'IKD.01', indikator: 'Rasio Kemantapan Jalan Kota', kategori: 'Infrastruktur', satuan: '%', baseline: '88.20', target2029: '96.50', opd: 'DPUPR Kota Tegal' },
  { id: 2, kode: 'IKD.02', indikator: 'Persentase Rumah Tangga Bersanitasi Layak', kategori: 'Perumahan & Permukiman', satuan: '%', baseline: '89.40', target2029: '98.00', opd: 'Disperkim Kota Tegal' },
  { id: 3, kode: 'IKD.03', indikator: 'Cakupan Pelayanan Air Minum Perpipaan', kategori: 'Layanan Dasar', satuan: '%', baseline: '74.50', target2029: '88.00', opd: 'Perumda Tirta Bahari / DPUPR' },
  { id: 4, kode: 'IKD.04', indikator: 'Indeks Kepuasan Masyarakat (IKM)', kategori: 'Tata Kelola', satuan: 'Skor', baseline: '84.20', target2029: '90.50', opd: 'Bagian Organisasi Setda' }
])

// 8. DATA PROYEKSI KERANGKA PENDANAAN
const pendanaanList = ref([
  { id: 1, komponen: 'Pendapatan Asli Daerah (PAD)', y2025: '380.5', y2026: '410.2', y2027: '435.0', y2028: '455.5', y2029: '475.0', total: '2.156,2' },
  { id: 2, komponen: 'Pendapatan Transfer (DAU/DAK/DBH)', y2025: '810.0', y2026: '835.0', y2027: '860.0', y2028: '885.0', y2029: '910.0', total: '4.300,0' },
  { id: 3, komponen: 'Lain-lain Pendapatan Daerah yang Sah', y2025: '35.0', y2026: '38.0', y2027: '40.0', y2028: '42.0', y2029: '45.0', total: '200,0' },
  { id: 4, komponen: 'Total Pendapatan Daerah', y2025: '1.225,5', y2026: '1.283,2', y2027: '1.335,0', y2028: '1.382,5', y2029: '1.430,0', total: '6.656,2' },
  { id: 5, komponen: 'Belanja Operasi (Pegawai & Barang)', y2025: '750.0', y2026: '775.0', y2027: '800.0', y2028: '820.0', y2029: '840.0', total: '3.985,0' },
  { id: 6, komponen: 'Belanja Modal & Program Pembangunan', y2025: '460.0', y2026: '495.0', y2027: '520.0', y2028: '550.0', y2029: '580.0', total: '2.605,0' }
])

// Filtered Lists
const filteredMisi = computed(() => {
  if (!searchQuery.value) return misiList.value
  const q = searchQuery.value.toLowerCase()
  return misiList.value.filter(m => m.uraian.toLowerCase().includes(q) || m.fokus.toLowerCase().includes(q))
})

const filteredTujuan = computed(() => {
  if (!searchQuery.value) return tujuanList.value
  const q = searchQuery.value.toLowerCase()
  return tujuanList.value.filter(t => t.uraian.toLowerCase().includes(q) || t.indikator.toLowerCase().includes(q) || t.kode.toLowerCase().includes(q))
})

const filteredSasaran = computed(() => {
  if (!searchQuery.value) return sasaranList.value
  const q = searchQuery.value.toLowerCase()
  return sasaranList.value.filter(s => s.uraian.toLowerCase().includes(q) || s.indikator.toLowerCase().includes(q) || s.kode.toLowerCase().includes(q))
})

const filteredProgram = computed(() => {
  if (!searchQuery.value) return programList.value
  const q = searchQuery.value.toLowerCase()
  return programList.value.filter(p => p.nama.toLowerCase().includes(q) || p.opd.toLowerCase().includes(q) || p.kode.toLowerCase().includes(q))
})

const filteredIku = computed(() => {
  if (!searchQuery.value) return ikuList.value
  const q = searchQuery.value.toLowerCase()
  return ikuList.value.filter(i => i.indikator.toLowerCase().includes(q) || i.opd.toLowerCase().includes(q))
})

const filteredIkd = computed(() => {
  if (!searchQuery.value) return ikdList.value
  const q = searchQuery.value.toLowerCase()
  return ikdList.value.filter(i => i.indikator.toLowerCase().includes(q) || i.opd.toLowerCase().includes(q) || i.kategori.toLowerCase().includes(q))
})

// Helpers
const formatRupiah = (value) => {
  if (!value) return 'Rp 0'
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(value)
// Modal & Actions
const openAddModal = () => {
  if (activeTab.value === 'visi') {
    visiTabRef.value?.openEditVisiModal?.()
    return
  }
  if (activeTab.value === 'misi') {
    misiTabRef.value?.openAddMisiModal?.()
    return
  }
  if (activeTab.value === 'tujuan') {
    tujuanTabRef.value?.openAddTujuanModal?.()
    return
  }
  if (activeTab.value === 'sasaran') {
    sasaranTabRef.value?.openAddSasaranModal?.()
    return
  }

  modalTitle.value = `Tambah Data ${currentTabTitle.value}`
  formModel.value = { kode: '', uraian: '', indikator: '', target: '' }
  showModal.value = true
}

const handleEditVisi = () => {
  modalTitle.value = 'Edit Visi RPJMD Kota Tegal'
  formModel.value = { kode: 'V-RPJMD', uraian: visiData.value.teks, indikator: 'Dasar Hukum', target: visiData.value.dasarHukum }
  showModal.value = true
}

const saveFormData = () => {
  showModal.value = false
  Swal.fire({
    icon: 'success',
    title: 'Data Tersimpan',
    text: `Data ${currentTabTitle.value} berhasil disimpan ke dokumen RPJMD.`,
    timer: 2000,
    showConfirmButton: false
  })
}

const handleAction = (type, moduleName, item) => {
  if (type === 'delete') {
    Swal.fire({
      title: 'Hapus Data?',
      text: `Apakah Anda yakin ingin menghapus data [${item.kode || item.indikator}] dari ${moduleName}?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ef4444',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Ya, Hapus',
      cancelButtonText: 'Batal'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire('Terhapus', 'Data telah berhasil dihapus.', 'success')
      }
    })
  } else {
    modalTitle.value = `Edit ${moduleName} [${item.kode || item.indikator}]`
    formModel.value = {
      kode: item.kode || '',
      uraian: item.uraian || item.nama || item.indikator || '',
      indikator: item.indikator || '',
      target: item.targetAkhir || item.target2029 || ''
    }
    showModal.value = true
  }
}

const handleExport = () => {
  Swal.fire({
    title: 'Ekspor Dokumen RPJMD',
    text: 'Pilih format ekspor data RPJMD:',
    icon: 'info',
    showDenyButton: true,
    showCancelButton: true,
    confirmButtonText: 'PDF Dokumen',
    denyButtonText: 'Excel (XLSX)',
    cancelButtonText: 'Batal',
    confirmButtonColor: '#308e87',
    denyButtonColor: '#f39159'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire('Mengunduh PDF', 'Dokumen RPJMD format PDF sedang diunduh.', 'success')
    } else if (result.isDenied) {
      Swal.fire('Mengunduh Excel', 'Data tabulasi RPJMD format Excel sedang diunduh.', 'success')
    }
  })
}
</script>
