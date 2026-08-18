<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    
    <!-- Top Action & Info Bar -->
    <div class="bg-white dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-5 py-3.5 flex flex-wrap items-center justify-between gap-3 shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[#308e87] to-[#1e5955] text-white flex items-center justify-center shadow-md">
          <Compass class="w-5 h-5" />
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h2 class="text-sm font-black text-slate-900 dark:text-white">RPJPD Kota Tegal {{ visiData.idperiode || '2025–2045' }}</h2>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4]">20 Tahunan</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400">Rencana Pembangunan Jangka Panjang Daerah Kota Tegal (Kode Pemda: {{ visiData.kodepemda || '3376' }})</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center space-x-2">
        <button 
          @click="fetchRpjpdData"
          class="p-1.5 rounded-lg text-xs font-bold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors cursor-pointer"
          title="Segarkan Data"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
        </button>
        <button 
          @click="showSwal('Ekspor Data', 'Dokumen RPJPD berhasil diunduh (PDF / Excel).')"
          class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 flex items-center space-x-1.5 transition-colors cursor-pointer"
        >
          <Download class="w-3.5 h-3.5" />
          <span>Ekspor</span>
        </button>
      </div>
    </div>

    <!-- 5 Tab Buttons Bar -->
    <div class="bg-slate-100 dark:bg-[#111c2e] border-b border-slate-200 dark:border-slate-800 px-4 py-2 flex items-center space-x-1 overflow-x-auto no-scrollbar shrink-0">
      <button
        v-for="t in tabs"
        :key="t.id"
        @click="activeTab = t.id"
        class="px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center space-x-1.5 shrink-0 cursor-pointer"
        :class="activeTab === t.id 
          ? 'bg-white dark:bg-[#1e293b] text-[#308e87] dark:text-[#3aada4] shadow-sm font-black' 
          : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/60 dark:hover:bg-slate-800/60'"
      >
        <component :is="t.icon" class="w-3.5 h-3.5" />
        <span>{{ t.label }}</span>
        <span v-if="t.count !== undefined" class="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
          {{ t.count }}
        </span>
      </button>
    </div>

    <!-- Tab Content Area (Scrollable) -->
    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      
      <!-- TAB 1: VISI DAERAH & PENJELASAN VISI -->
      <div v-if="activeTab === 'visi'" class="space-y-4">
        
        <!-- Visi Card (Tabel: rpjpd_visi) -->
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <div class="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4]">
              <Compass class="w-3.5 h-3.5" />
              <span>Visi Daerah (Tabel: <code class="font-mono">rpjpd_visi</code>)</span>
            </div>
            <span class="text-xs font-bold text-slate-400">Kode Pemda: {{ visiData.kodepemda || '3376' }}</span>
          </div>
          <h3 class="text-lg font-black text-slate-900 dark:text-white leading-snug">
            “{{ visiData.uraivisi || 'Memuat Visi Daerah...' }}”
          </h3>
          <div class="flex items-center space-x-4 mt-3 text-xs text-slate-500 dark:text-slate-400 font-medium">
            <span>Periode: <strong>{{ visiData.idperiode || '20252045' }}</strong></span>
            <span>Status: <strong class="text-emerald-500">{{ visiData.status === 1 ? 'Aktif' : 'Draft' }}</strong></span>
            <span>Check Value: <strong>{{ visiData.check_value || '-' }}</strong></span>
          </div>
        </div>

        <!-- Penjelasan Visi Grid (Tabel: rpjpd_penjelasan_visi) -->
        <div class="space-y-2.5">
          <h4 class="text-xs font-black uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center space-x-1.5">
            <Sparkles class="w-3.5 h-3.5 text-[#308e87]" />
            <span>Penjelasan Pokok Visi (Tabel: <code class="font-mono text-[#308e87]">rpjpd_penjelasan_visi</code>)</span>
          </h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div 
              v-for="(p, i) in penjelasanVisiList" 
              :key="p.id || i" 
              class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm flex flex-col justify-between space-y-2 hover:border-[#308e87]/40 transition-colors"
            >
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black text-[#308e87] dark:text-[#3aada4]">#{{ p.no || (i+1) }}</span>
                  <span class="text-[10px] font-mono text-slate-400">Kode: {{ p.kodepenjelasan || '-' }}</span>
                </div>
                <h4 class="text-xs font-black text-slate-900 dark:text-white mt-1">{{ p.pokokvisi }}</h4>
                <p class="text-[11px] text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">{{ p.penjelasanvisi }}</p>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-slate-800 text-[10px] text-slate-400 flex justify-between">
                <span>Periode: {{ p.idperiode || '20252045' }}</span>
                <span>Pemda: {{ p.kodepemda || '3376' }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- TAB 2: SASARAN VISI & INDIKATOR (TREE TABLE) -->
      <div v-if="activeTab === 'sasaran_visi'" class="space-y-3">
        
        <!-- Tree Table Action header -->
        <div class="flex items-center justify-between text-xs pb-1">
          <div class="flex items-center space-x-2">
            <span class="font-bold text-slate-700 dark:text-slate-300">Tree Tabel Sasaran Visi</span>
            <span class="text-[11px] text-slate-400">({{ sasaranVisiList.length }} Sasaran, {{ totalIndikatorCount }} Indikator)</span>
          </div>
          <div class="flex items-center space-x-1.5 text-[11px]">
            <button @click="expandAll" class="font-bold text-[#308e87] hover:underline cursor-pointer">Buka Semua</button>
            <span class="text-slate-300">|</span>
            <button @click="collapseAll" class="font-bold text-slate-500 hover:underline cursor-pointer">Tutup Semua</button>
          </div>
        </div>

        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-slate-100 dark:bg-slate-800/90 text-slate-600 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase">
                <tr>
                  <th class="py-2.5 px-3 w-28">Kode</th>
                  <th class="py-2.5 px-3 min-w-[200px]">Sasaran Visi &amp; Indikator</th>
                  <th class="py-2.5 px-3 text-center w-20">Kondisi Awal</th>
                  <th class="py-2.5 px-3 text-center w-20">Baseline</th>
                  <th class="py-2.5 px-3 text-center w-20 bg-blue-50/50 dark:bg-blue-950/20 text-blue-600">Target 1</th>
                  <th class="py-2.5 px-3 text-center w-20 bg-teal-50/50 dark:bg-teal-950/20 text-teal-600">Target 2</th>
                  <th class="py-2.5 px-3 text-center w-20 bg-amber-50/50 dark:bg-amber-950/20 text-amber-600">Target 3</th>
                  <th class="py-2.5 px-3 text-center w-20 bg-emerald-50/50 dark:bg-emerald-950/20 text-emerald-600">Target 4</th>
                </tr>
              </thead>

              <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
                <template v-for="sv in sasaranVisiList" :key="sv.id || sv.kode">
                  
                  <!-- PARENT ROW -->
                  <tr 
                    @click="toggleExpand(sv.kode)"
                    class="bg-slate-50/90 dark:bg-slate-800/70 hover:bg-slate-100 font-bold transition-colors cursor-pointer border-t border-slate-200 dark:border-slate-700"
                  >
                    <td class="py-2 px-3">
                      <div class="flex items-center space-x-1.5">
                        <button class="p-0.5 text-slate-500">
                          <ChevronDown v-if="expandedMap[sv.kode]" class="w-3.5 h-3.5 text-[#308e87]" />
                          <ChevronRight v-else class="w-3.5 h-3.5 text-slate-400" />
                        </button>
                        <span class="px-2 py-0.5 rounded text-[10px] font-black bg-[#308e87] text-white">
                          {{ sv.kode }}
                        </span>
                      </div>
                    </td>
                    <td class="py-2 px-3 font-bold text-slate-900 dark:text-white leading-snug">
                      {{ sv.urai }}
                      <span class="ml-1 text-[10px] font-normal text-slate-400">({{ sv.indikator_list ? sv.indikator_list.length : 0 }} Indikator)</span>
                    </td>
                    <td class="py-2 px-3 text-center text-slate-400">-</td>
                    <td class="py-2 px-3 text-center text-slate-400">-</td>
                    <td class="py-2 px-3 text-center text-slate-400 bg-blue-50/20 dark:bg-blue-950/10">-</td>
                    <td class="py-2 px-3 text-center text-slate-400 bg-teal-50/20 dark:bg-teal-950/10">-</td>
                    <td class="py-2 px-3 text-center text-slate-400 bg-amber-50/20 dark:bg-amber-950/10">-</td>
                    <td class="py-2 px-3 text-center text-slate-400 bg-emerald-50/20 dark:bg-emerald-950/10">-</td>
                  </tr>

                  <!-- CHILD ROWS -->
                  <template v-if="expandedMap[sv.kode]">
                    <tr 
                      v-for="ind in sv.indikator_list" 
                      :key="ind.id || ind.kode_indikator" 
                      class="bg-white dark:bg-[#141d30] hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors"
                    >
                      <td class="py-2 px-3 pl-7 font-mono font-bold text-[#308e87]">
                        <div class="flex items-center space-x-1 text-slate-400">
                          <CornerDownRight class="w-3 h-3" />
                          <span class="text-[#308e87] font-mono">{{ ind.kode_indikator }}</span>
                        </div>
                      </td>
                      <td class="py-2 px-3 text-slate-800 dark:text-slate-200 font-semibold">{{ ind.urai_indikator }}</td>
                      <td class="py-2 px-3 text-center text-slate-600 dark:text-slate-300">{{ ind.kondisi_awal || '-' }}</td>
                      <td class="py-2 px-3 text-center text-slate-500">{{ ind.baseline || '-' }}</td>
                      <td class="py-2 px-3 text-center font-bold text-blue-600">{{ ind.target_1 || '-' }}</td>
                      <td class="py-2 px-3 text-center font-bold text-teal-600">{{ ind.target_2 || '-' }}</td>
                      <td class="py-2 px-3 text-center font-bold text-amber-600">{{ ind.target_3 || '-' }}</td>
                      <td class="py-2 px-3 text-center font-black text-emerald-600">{{ ind.target_4 || '-' }}</td>
                    </tr>
                  </template>

                </template>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- TAB 3: MISI DAERAH (Tabel: rpjpd_misi) -->
      <div v-if="activeTab === 'misi'" class="space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div 
            v-for="(m, i) in misiList" 
            :key="m.id || i" 
            class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm hover:border-indigo-500/40 transition-all flex flex-col justify-between space-y-2"
          >
            <div>
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 rounded text-[10px] font-black bg-indigo-500/15 text-indigo-600 dark:text-indigo-400">
                  Misi {{ m.idmisi || (i+1) }}
                </span>
                <span v-if="m.misi_pembangunan" class="text-[10px] font-mono text-teal-600 dark:text-teal-400 font-bold">
                  Tag: {{ m.misi_pembangunan }}
                </span>
              </div>
              <h4 class="text-xs font-bold text-slate-900 dark:text-white mt-2 leading-snug">
                {{ m.uraimisi }}
              </h4>
            </div>
            
            <div class="pt-2 border-t border-slate-100 dark:border-slate-800 text-[10px] text-slate-400 flex items-center justify-between">
              <span>Urut: {{ m.urut || m.no }}</span>
              <span v-if="m.misi_provinsi && m.misi_provinsi.length > 0">Prov: {{ m.misi_provinsi.join(', ') }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 4: ARAH KEBIJAKAN (Tabel: rpjpd_arah_kebijakan) -->
      <div v-if="activeTab === 'arah_kebijakan'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-slate-100 dark:bg-slate-800/90 text-slate-600 dark:text-slate-300 font-black border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase">
                <th rowspan="2" class="py-2.5 px-3 w-14 text-center border-r border-slate-200 dark:border-slate-700">No</th>
                <th rowspan="2" class="py-2.5 px-3 min-w-[180px] border-r border-slate-200 dark:border-slate-700">Sasaran Pembangunan</th>
                <th rowspan="2" class="py-2.5 px-3 min-w-[240px] border-r border-slate-200 dark:border-slate-700">Arah Kebijakan RPJPD</th>
                <th colspan="4" class="py-1.5 px-2 text-center border-b border-r border-slate-200 dark:border-slate-700 bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 font-bold">
                  Periode Pelaksanaan RPJMD
                </th>
              </tr>
              <tr class="bg-amber-50/40 dark:bg-amber-950/20 text-slate-600 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800 text-[9px]">
                <th class="py-1 px-2 w-14 text-center border-r border-slate-200 dark:border-slate-700 text-blue-600">1 (25-29)</th>
                <th class="py-1 px-2 w-14 text-center border-r border-slate-200 dark:border-slate-700 text-teal-600">2 (30-34)</th>
                <th class="py-1 px-2 w-14 text-center border-r border-slate-200 dark:border-slate-700 text-amber-600">3 (35-39)</th>
                <th class="py-1 px-2 w-14 text-center border-r border-slate-200 dark:border-slate-700 text-emerald-600">4 (40-45)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="ak in arahKebijakanList" :key="ak.id || ak.idarahkebijakan" class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
                <td class="py-2.5 px-3 text-center font-black text-amber-600 border-r border-slate-100 dark:border-slate-800">#{{ ak.idarahkebijakan }}</td>
                <td class="py-2.5 px-3 border-r border-slate-100 dark:border-slate-800">
                  <span class="text-[11px] font-semibold text-slate-800 dark:text-slate-200 line-clamp-2">
                    {{ ak.uraisasaran || '-' }}
                  </span>
                </td>
                <td class="py-2.5 px-3 font-bold text-slate-900 dark:text-white leading-relaxed border-r border-slate-100 dark:border-slate-800">{{ ak.arahkebijakan }}</td>
                
                <!-- 1 -->
                <td class="py-2.5 px-2 text-center border-r border-slate-100 dark:border-slate-800 bg-blue-50/20 dark:bg-blue-950/10">
                  <span v-if="isPeriodeActive(ak, '1')" class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-500 text-white font-black text-[10px]">✓</span>
                  <span v-else class="text-slate-300 dark:text-slate-600">-</span>
                </td>
                <!-- 2 -->
                <td class="py-2.5 px-2 text-center border-r border-slate-100 dark:border-slate-800 bg-teal-50/20 dark:bg-teal-950/10">
                  <span v-if="isPeriodeActive(ak, '2')" class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-teal-500 text-white font-black text-[10px]">✓</span>
                  <span v-else class="text-slate-300 dark:text-slate-600">-</span>
                </td>
                <!-- 3 -->
                <td class="py-2.5 px-2 text-center border-r border-slate-100 dark:border-slate-800 bg-amber-50/20 dark:bg-amber-950/10">
                  <span v-if="isPeriodeActive(ak, '3')" class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-amber-500 text-white font-black text-[10px]">✓</span>
                  <span v-else class="text-slate-300 dark:text-slate-600">-</span>
                </td>
                <!-- 4 -->
                <td class="py-2.5 px-2 text-center border-r border-slate-100 dark:border-slate-800 bg-emerald-50/20 dark:bg-emerald-950/10">
                  <span v-if="isPeriodeActive(ak, '4')" class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-emerald-500 text-white font-black text-[10px]">✓</span>
                  <span v-else class="text-slate-300 dark:text-slate-600">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 5: SASARAN POKOK (TREE TABLE) -->
      <div v-if="activeTab === 'sasaran_pokok'" class="space-y-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <button 
              @click="expandAllPokok"
              class="px-2.5 py-1 text-[10px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#f39159] bg-slate-100 dark:bg-slate-800 rounded-lg"
            >
              Buka Semua
            </button>
            <button 
              @click="collapseAllPokok"
              class="px-2.5 py-1 text-[10px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#f39159] bg-slate-100 dark:bg-slate-800 rounded-lg"
            >
              Tutup Semua
            </button>
          </div>
          <span class="text-[11px] font-bold text-slate-500">
            {{ sasaranPokokList.length }} Sasaran • {{ totalIndikatorPokokCount }} Indikator
          </span>
        </div>

        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-bold border-b border-slate-200 dark:border-slate-800 text-[11px]">
              <tr>
                <th class="py-2.5 px-3 w-20 text-center">Kode</th>
                <th class="py-2.5 px-2.5 w-18 text-center">Misi</th>
                <th class="py-2.5 px-3 min-w-[200px]">Sasaran Pokok / Indikator Kinerja</th>
                <th class="py-2.5 px-2 text-center w-16">Satuan</th>
                <th class="py-2.5 px-2 text-center w-14">Awal</th>
                <th class="py-2.5 px-2 text-center w-14 text-amber-600">Base</th>
                <th class="py-2.5 px-2 text-center w-14 text-blue-600">T1</th>
                <th class="py-2.5 px-2 text-center w-14 text-teal-600">T2</th>
                <th class="py-2.5 px-2 text-center w-14 text-amber-600">T3</th>
                <th class="py-2.5 px-2 text-center w-14 text-emerald-600 font-black">T4</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <template v-for="sp in sasaranPokokList" :key="sp.id || sp.idsasaran">
                <!-- Parent Row -->
                <tr 
                  @click="toggleExpandPokok(sp.idsasaran)"
                  class="bg-slate-50/80 dark:bg-slate-800/60 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer font-bold select-none border-t border-slate-200 dark:border-slate-700"
                >
                  <td class="py-2 px-3">
                    <div class="flex items-center space-x-1.5">
                      <button class="p-0.5 text-slate-400">
                        <ChevronDown v-if="expandedPokokMap[sp.idsasaran]" class="w-3.5 h-3.5 text-[#f39159]" />
                        <ChevronRight v-else class="w-3.5 h-3.5 text-slate-400" />
                      </button>
                      <span class="px-2 py-0.5 rounded text-[10px] font-black bg-[#f39159] text-white">
                        {{ sp.idsasaran }}
                      </span>
                    </div>
                  </td>
                  <td class="py-2 px-2 text-center">
                    <span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400">
                      Misi {{ sp.idmisi || '1' }}
                    </span>
                  </td>
                  <td class="py-2 px-3 text-slate-900 dark:text-white font-extrabold text-xs">
                    <div class="flex items-center space-x-1.5">
                      <span>{{ sp.uraisasaran }}</span>
                      <span class="text-[10px] text-[#f39159] font-bold">
                        ({{ sp.indikator_list ? sp.indikator_list.length : 0 }})
                      </span>
                    </div>
                  </td>
                  <td class="py-2 px-2 text-center text-slate-400">-</td>
                  <td class="py-2 px-2 text-center text-slate-400">-</td>
                  <td class="py-2 px-2 text-center text-slate-400">-</td>
                  <td class="py-2 px-2 text-center text-slate-400 bg-blue-50/10">-</td>
                  <td class="py-2 px-2 text-center text-slate-400 bg-teal-50/10">-</td>
                  <td class="py-2 px-2 text-center text-slate-400 bg-amber-50/10">-</td>
                  <td class="py-2 px-2 text-center text-slate-400 bg-emerald-50/10">-</td>
                </tr>

                <!-- Child Rows -->
                <template v-if="expandedPokokMap[sp.idsasaran]">
                  <tr 
                    v-for="ind in sp.indikator_list" 
                    :key="ind.id || ind.idsasaran_indikator"
                    class="bg-white dark:bg-[#141d30] hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors"
                  >
                    <td class="py-2 px-3 pl-6">
                      <div class="flex items-center space-x-1 font-mono text-[11px]">
                        <CornerDownRight class="w-3 h-3 text-slate-400" />
                        <span class="text-[#f39159] font-bold">#{{ ind.idsasaran_indikator }}</span>
                      </div>
                    </td>
                    <td class="py-2 px-2 text-center text-slate-400 text-[10px]">
                      M{{ ind.idmisi || sp.idmisi || '1' }}
                    </td>
                    <td class="py-2 px-3 text-slate-800 dark:text-slate-200 font-medium text-[11px] leading-snug">
                      {{ ind.uraisasaran_indikator }}
                    </td>
                    <td class="py-2 px-2 text-center text-slate-500 text-[10px]">{{ ind.satuan || '-' }}</td>
                    <td class="py-2 px-2 text-center text-slate-600 dark:text-slate-400 text-[11px]">{{ ind.kondisi_awal || '-' }}</td>
                    <td class="py-2 px-2 text-center text-amber-700 dark:text-amber-400 font-semibold text-[11px] bg-amber-50/20">{{ ind.baseline || '-' }}</td>
                    <td class="py-2 px-2 text-center text-blue-600 font-bold text-[11px] bg-blue-50/10">{{ ind.target_1 || '-' }}</td>
                    <td class="py-2 px-2 text-center text-teal-600 font-bold text-[11px] bg-teal-50/10">{{ ind.target_2 || '-' }}</td>
                    <td class="py-2 px-2 text-center text-amber-600 font-bold text-[11px] bg-amber-50/10">{{ ind.target_3 || '-' }}</td>
                    <td class="py-2 px-2 text-center text-emerald-600 font-black text-[11px] bg-emerald-50/20">{{ ind.target_4 || '-' }}</td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { Compass, Target, Flag, Milestone, CheckCircle2, Download, RotateCw, Sparkles, ChevronDown, ChevronRight, CornerDownRight } from 'lucide-vue-next'

const activeTab = ref('visi')
const loading = ref(false)
const expandedMap = ref({})
const expandedPokokMap = ref({})

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
const sasaranVisiList = ref([])
const misiList = ref([])
const arahKebijakanList = ref([])
const sasaranPokokList = ref([])

const totalIndikatorCount = computed(() => {
  return sasaranVisiList.value.reduce((acc, sv) => acc + (sv.indikator_list ? sv.indikator_list.length : 0), 0)
})

const totalIndikatorPokokCount = computed(() => {
  return sasaranPokokList.value.reduce((acc, sp) => acc + (sp.indikator_list ? sp.indikator_list.length : 0), 0)
})

const tabs = computed(() => [
  { id: 'visi', label: 'Visi Daerah', icon: Compass, count: penjelasanVisiList.value.length },
  { id: 'sasaran_visi', label: 'Sasaran Visi (Tree)', icon: Target, count: totalIndikatorCount.value },
  { id: 'misi', label: 'Misi Daerah', icon: Flag, count: misiList.value.length },
  { id: 'arah_kebijakan', label: 'Arah Kebijakan', icon: Milestone, count: arahKebijakanList.value.length },
  { id: 'sasaran_pokok', label: 'Sasaran Pokok (Tree)', icon: CheckCircle2, count: totalIndikatorPokokCount.value }
])

function toggleExpand(kode) {
  expandedMap.value[kode] = !expandedMap.value[kode]
}

function expandAll() {
  sasaranVisiList.value.forEach(sv => {
    expandedMap.value[sv.kode] = true
  })
}

function collapseAll() {
  sasaranVisiList.value.forEach(sv => {
    expandedMap.value[sv.kode] = false
  })
}

function toggleExpandPokok(idsasaran) {
  expandedPokokMap.value[idsasaran] = !expandedPokokMap.value[idsasaran]
}

function expandAllPokok() {
  sasaranPokokList.value.forEach(sp => {
    expandedPokokMap.value[sp.idsasaran] = true
  })
}

function collapseAllPokok() {
  sasaranPokokList.value.forEach(sp => {
    expandedPokokMap.value[sp.idsasaran] = false
  })
}

function isPeriodeActive(item, periodeKey) {
  if (!item || !item.periode_rpjmd_pelaksanaan) return false
  if (Array.isArray(item.periode_rpjmd_pelaksanaan)) {
    return item.periode_rpjmd_pelaksanaan.map(String).includes(String(periodeKey))
  }
  return String(item.periode_rpjmd_pelaksanaan) === String(periodeKey)
}

async function fetchRpjpdData() {
  loading.value = true
  try {
    const [resVisi, resSasaran, resMisi, resArah, resPokok] = await Promise.all([
      axios.get('/api/v1/rpjpd/visi-lengkap'),
      axios.get('/api/v1/rpjpd/sasaran-visi-lengkap'),
      axios.get('/api/v1/rpjpd/misi'),
      axios.get('/api/v1/rpjpd/arah-kebijakan'),
      axios.get('/api/v1/rpjpd/sasaran-pokok-lengkap')
    ])
    
    if (resVisi.data) {
      if (resVisi.data.visi_utama) {
        visiData.value = resVisi.data.visi_utama
      }
      if (resVisi.data.daftar_penjelasan) {
        penjelasanVisiList.value = resVisi.data.daftar_penjelasan
      }
    }

    if (resSasaran.data && resSasaran.data.daftar_sasaran_visi) {
      sasaranVisiList.value = resSasaran.data.daftar_sasaran_visi
      resSasaran.data.daftar_sasaran_visi.forEach(sv => {
        if (expandedMap.value[sv.kode] === undefined) {
          expandedMap.value[sv.kode] = true
        }
      })
    }

    if (Array.isArray(resMisi.data)) {
      misiList.value = resMisi.data
    }

    if (Array.isArray(resArah.data)) {
      arahKebijakanList.value = resArah.data
    }

    if (resPokok.data && resPokok.data.daftar_sasaran_pokok) {
      sasaranPokokList.value = resPokok.data.daftar_sasaran_pokok
      resPokok.data.daftar_sasaran_pokok.forEach(sp => {
        if (expandedPokokMap.value[sp.idsasaran] === undefined) {
          expandedPokokMap.value[sp.idsasaran] = true
        }
      })
    }
  } catch (err) {
    console.error('Error fetching RPJPD data in RpjpdApp:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRpjpdData()
})

const sasaranPokok = [
  { kode: 'SP.01', nama: 'Peningkatan Usia Harapan Hidup Warga', indikator: 'UHH (Tahun)', target: '78.5 Tahun', opd: 'Dinas Kesehatan' },
  { kode: 'SP.02', nama: 'Peningkatan Rata-rata Lama Sekolah', indikator: 'RLS (Tahun)', target: '12.8 Tahun', opd: 'Dinas Pendidikan' },
  { kode: 'SP.03', nama: 'Pertumbuhan Nilai Tambah Ekonomi Maritim', indikator: 'PDRB Maritim (Triliun)', target: 'Rp 14.2 T', opd: 'DKPPP Kota Tegal' },
  { kode: 'SP.04', nama: 'Pengendalian Kawasan Genangan Rob Pesisir', indikator: 'Luas Genangan Teratasi (%)', target: '100%', opd: 'DPUPR Kota Tegal' },
  { kode: 'SP.05', nama: 'Kepuasan Warga Terhadap Layanan Publik', indikator: 'Indeks IKM (Skor)', target: '92.0 Poin', opd: 'Bagian Organisasi' }
]

const showSwal = (title, text) => {
  Swal.fire({
    title,
    text,
    icon: 'info',
    confirmButtonColor: '#308e87',
    timer: 2000
  })
}
</script>
