<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    
    <!-- Top Bar -->
    <div class="bg-white dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-5 py-3.5 flex flex-wrap items-center justify-between gap-3 shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-800 text-white flex items-center justify-center shadow-md">
          <Target class="w-5 h-5" />
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h2 class="text-sm font-black text-slate-900 dark:text-white">RPJMD Kota Tegal 2025–2029</h2>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400">5 Tahunan</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400">Rencana Pembangunan Jangka Menengah Daerah Kota Tegal</p>
        </div>
      </div>

      <div class="flex items-center space-x-2">
        <button 
          @click="showSwal('Ekspor Data', 'Dokumen RPJMD berhasil diunduh.')"
          class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-700 dark:text-slate-300 flex items-center space-x-1.5"
        >
          <Download class="w-3.5 h-3.5" />
          <span>Ekspor</span>
        </button>
        <button 
          @click="showSwal('Tambah Data', 'Modal form penambahan data RPJMD dibuka.')"
          class="px-3 py-1.5 rounded-lg text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white flex items-center space-x-1.5 shadow-sm"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Data</span>
        </button>
      </div>
    </div>

    <!-- 8 Tab Navigation Buttons -->
    <div class="bg-slate-100 dark:bg-[#111c2e] border-b border-slate-200 dark:border-slate-800 px-4 py-2 flex items-center space-x-1 overflow-x-auto no-scrollbar shrink-0">
      <button
        v-for="t in tabs"
        :key="t.id"
        @click="activeTab = t.id"
        class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center space-x-1.5 shrink-0"
        :class="activeTab === t.id 
          ? 'bg-white dark:bg-[#1e293b] text-indigo-600 dark:text-indigo-400 shadow-sm font-black' 
          : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 hover:bg-slate-200/60 dark:hover:bg-slate-800/60'"
      >
        <component :is="t.icon" class="w-3.5 h-3.5" />
        <span>{{ t.label }}</span>
        <span v-if="t.count" class="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
          {{ t.count }}
        </span>
      </button>
    </div>

    <!-- Content Area (Scrollable) -->
    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      
      <!-- TAB 1: VISI -->
      <div v-if="activeTab === 'visi'" class="space-y-4">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
          <div class="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-[11px] font-bold bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 mb-3">
            <Compass class="w-3.5 h-3.5" />
            <span>Visi Kepala Daerah {{ visiData.idperiode || '2025–2029' }}</span>
          </div>
          <h3 class="text-lg font-black text-slate-900 dark:text-white leading-snug">
            “{{ visiData.uraivisi || 'Tegal Berdikari Dan Sejahtera, Menjadi Kota Idaman' }}”
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 leading-relaxed">
            Pagu Indikatif: {{ visiData.tahunpagu || '2026 - 2030' }} • Sumber Database: <code class="font-mono">public.rpjmd_visi</code>
          </p>
        </div>
      </div>

      <!-- TAB 2: MISI -->
      <div v-if="activeTab === 'misi'" class="space-y-3">
        <div v-for="m in misiList" :key="m.idmisi || m.urut" class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm flex items-start space-x-3.5">
          <div class="w-8 h-8 rounded-lg bg-indigo-600 text-white font-black text-xs flex items-center justify-center shrink-0">
            {{ m.urut }}
          </div>
          <div>
            <h4 class="text-xs font-black text-slate-900 dark:text-white">{{ m.uraimisi }}</h4>
            <p class="text-[11px] text-slate-400 mt-1 font-mono">UUID: {{ (m.idmisi || '').substring(0, 13) }}...</p>
          </div>
        </div>
      </div>

      <!-- TAB 3: TUJUAN (TREE TABLE) -->
      <div v-if="activeTab === 'tujuan'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <div class="p-3 bg-slate-50 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span class="text-xs font-black text-slate-800 dark:text-white">Tree Tabel Tujuan &amp; Indikator RPJMD</span>
            <span class="text-[10px] text-slate-500 font-semibold">{{ tujuanList.length }} Tujuan • {{ totalIndikatorCount }} Indikator</span>
          </div>
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100/90 dark:bg-slate-800/60 text-slate-600 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase">
              <tr>
                <th class="py-2.5 px-3 w-14 text-center">No</th>
                <th class="py-2.5 px-3 w-48 text-center text-indigo-600">Misi RPJMD</th>
                <th class="py-2.5 px-4">Tujuan / Indikator Kinerja</th>
                <th class="py-2.5 px-3 text-center w-20">Satuan</th>
                <th class="py-2.5 px-3 text-center w-20">Baseline</th>
                <th class="py-2.5 px-2 text-center w-16">2025</th>
                <th class="py-2.5 px-2 text-center w-16">2026</th>
                <th class="py-2.5 px-2 text-center w-16">2027</th>
                <th class="py-2.5 px-2 text-center w-16">2028</th>
                <th class="py-2.5 px-2 text-center w-16">2029</th>
                <th class="py-2.5 px-2 text-center w-16 text-emerald-600 font-black">2030</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <template v-for="t in tujuanList" :key="t.idtujuan">
                <!-- Parent: Tujuan -->
                <tr class="bg-slate-50/80 dark:bg-slate-800/70 font-bold align-top">
                  <td class="py-2.5 px-3 text-center text-[#308e87] font-black">T-{{ t.urut }}</td>
                  <td class="py-2.5 px-3">
                    <div v-if="t.uraimisi || t.urut_misi" class="space-y-1">
                      <span class="inline-block px-1.5 py-0.5 rounded text-[10px] font-black bg-indigo-50 dark:bg-indigo-950 text-indigo-600 border border-indigo-200 dark:border-indigo-800">
                        Misi {{ t.urut_misi }}
                      </span>
                      <p class="text-[11px] text-slate-600 dark:text-slate-300 font-medium leading-tight">
                        {{ t.uraimisi }}
                      </p>
                    </div>
                    <span v-else class="text-slate-400 text-[10px]">-</span>
                  </td>
                  <td class="py-2.5 px-4 text-slate-900 dark:text-white font-extrabold" colspan="9">
                    {{ t.uraitujuan }}
                    <span class="ml-2 text-[10px] font-normal px-2 py-0.5 rounded-full bg-[#308e87]/10 text-[#308e87]">
                      {{ t.indikator_list ? t.indikator_list.length : 0 }} Indikator
                    </span>
                  </td>
                </tr>
                <!-- Children: Indikator Tujuan -->
                <tr v-for="ind in t.indikator_list" :key="ind.idtujuan_indikator" class="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                  <td class="py-2 px-3 text-center text-slate-400 font-mono text-[11px]">↳ #{{ ind.urut }}</td>
                  <td class="py-2 px-3 text-center text-slate-300 dark:text-slate-600 text-[11px]">-</td>
                  <td class="py-2 px-4 text-slate-700 dark:text-slate-300 font-medium pl-6">
                    {{ ind.uraitujuan_indikator }}
                    <span v-if="ind.iku" class="ml-1 text-[9px] px-1 py-0.2 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-600 font-black">IKU</span>
                    <span v-if="ind.ikd" class="ml-1 text-[9px] px-1 py-0.2 rounded bg-amber-100 dark:bg-amber-950 text-amber-600 font-black">IKD</span>
                  </td>
                  <td class="py-2 px-3 text-center text-slate-500 text-[11px]">{{ ind.satuan || '-' }}</td>
                  <td class="py-2 px-3 text-center font-bold text-amber-700 dark:text-amber-400 text-[11px]">{{ ind.baseline || '-' }}</td>
                  <td class="py-2 px-2 text-center text-blue-600 text-[11px]">{{ ind.target0 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-cyan-600 text-[11px]">{{ ind.target1 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-teal-600 text-[11px]">{{ ind.target2 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-indigo-600 text-[11px]">{{ ind.target3 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-amber-600 text-[11px]">{{ ind.target4 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-emerald-600 font-black text-[11px]">{{ ind.target5 || '-' }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 4: SASARAN (LIVE TREE TABLE) -->
      <div v-if="activeTab === 'sasaran'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <div class="p-3 bg-slate-50 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span class="text-xs font-black text-slate-800 dark:text-white">Tree Tabel Sasaran &amp; Indikator Sasaran RPJMD</span>
            <span class="text-[10px] text-slate-500 font-semibold">{{ sasaranListLive.length }} Sasaran • {{ totalIndikatorSasaranCount }} Indikator</span>
          </div>
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-100/90 dark:bg-slate-800/60 text-slate-600 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase">
              <tr>
                <th class="py-2.5 px-3 w-14 text-center">No</th>
                <th class="py-2.5 px-3 w-44 text-center text-indigo-600">Misi</th>
                <th class="py-2.5 px-3 w-48 text-center text-[#308e87]">Tujuan</th>
                <th class="py-2.5 px-4">Sasaran / Indikator Sasaran</th>
                <th class="py-2.5 px-3 text-center w-20">Satuan</th>
                <th class="py-2.5 px-3 text-center w-20">Baseline</th>
                <th class="py-2.5 px-2 text-center w-16">2025</th>
                <th class="py-2.5 px-2 text-center w-16">2026</th>
                <th class="py-2.5 px-2 text-center w-16">2027</th>
                <th class="py-2.5 px-2 text-center w-16">2028</th>
                <th class="py-2.5 px-2 text-center w-16">2029</th>
                <th class="py-2.5 px-2 text-center w-16 text-emerald-600 font-black">2030</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <template v-for="s in sasaranListLive" :key="s.idsasaran">
                <!-- Parent: Sasaran -->
                <tr class="bg-slate-50/80 dark:bg-slate-800/70 font-bold align-top">
                  <td class="py-2.5 px-3 text-center text-[#f39159] font-black">S-{{ s.urut }}</td>
                  <td class="py-2.5 px-3">
                    <div v-if="s.uraimisi || s.urut_misi" class="space-y-0.5">
                      <span class="inline-block px-1.5 py-0.2 rounded text-[9px] font-black bg-indigo-50 dark:bg-indigo-950 text-indigo-600 border border-indigo-200 dark:border-indigo-800">
                        Misi {{ s.urut_misi }}
                      </span>
                      <p class="text-[10px] text-slate-600 dark:text-slate-300 font-medium leading-tight">
                        {{ s.uraimisi }}
                      </p>
                    </div>
                    <span v-else class="text-slate-400 text-[10px]">-</span>
                  </td>
                  <td class="py-2.5 px-3">
                    <div v-if="s.uraitujuan || s.urut_tujuan" class="space-y-0.5">
                      <span class="inline-block px-1.5 py-0.2 rounded text-[9px] font-black bg-[#308e87]/15 text-[#308e87] border border-[#308e87]/30">
                        T-{{ s.urut_tujuan }}
                      </span>
                      <p class="text-[10px] text-slate-600 dark:text-slate-300 font-medium leading-tight">
                        {{ s.uraitujuan }}
                      </p>
                    </div>
                    <span v-else class="text-slate-400 text-[10px]">-</span>
                  </td>
                  <td class="py-2.5 px-4 text-slate-900 dark:text-white font-extrabold" colspan="9">
                    {{ s.uraisasaran }}
                    <span class="ml-2 text-[10px] font-normal px-2 py-0.5 rounded-full bg-[#f39159]/10 text-[#f39159]">
                      {{ s.indikator_list ? s.indikator_list.length : 0 }} Indikator
                    </span>
                  </td>
                </tr>
                <!-- Children: Indikator Sasaran -->
                <tr v-for="ind in s.indikator_list" :key="ind.idsasaran_indikator" class="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                  <td class="py-2 px-3 text-center text-slate-400 font-mono text-[11px]">↳ #{{ ind.urut }}</td>
                  <td class="py-2 px-3 text-center text-slate-300 dark:text-slate-600 text-[11px]">-</td>
                  <td class="py-2 px-3 text-center text-slate-300 dark:text-slate-600 text-[11px]">-</td>
                  <td class="py-2 px-4 text-slate-700 dark:text-slate-300 font-medium pl-6">
                    {{ ind.uraisasaran_indikator }}
                    <span v-if="ind.iku === '1' || ind.iku === true" class="ml-1 text-[9px] px-1 py-0.2 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-600 font-black">IKU</span>
                    <span v-if="ind.ikd === '1' || ind.ikd === true" class="ml-1 text-[9px] px-1 py-0.2 rounded bg-amber-100 dark:bg-amber-950 text-amber-600 font-black">IKD</span>
                  </td>
                  <td class="py-2 px-3 text-center text-slate-500 text-[11px]">{{ ind.satuan || '-' }}</td>
                  <td class="py-2 px-3 text-center font-bold text-amber-700 dark:text-amber-400 text-[11px]">{{ ind.baseline || '-' }}</td>
                  <td class="py-2 px-2 text-center text-blue-600 text-[11px]">{{ ind.target0 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-cyan-600 text-[11px]">{{ ind.target1 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-teal-600 text-[11px]">{{ ind.target2 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-indigo-600 text-[11px]">{{ ind.target3 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-amber-600 text-[11px]">{{ ind.target4 || '-' }}</td>
                  <td class="py-2 px-2 text-center text-emerald-600 font-black text-[11px]">{{ ind.target5 || '-' }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 5: PROGRAM -->
      <div v-if="activeTab === 'program'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-bold border-b border-slate-200 dark:border-slate-800 text-[11px]">
              <tr>
                <th class="py-2.5 px-4 w-28 text-center">Kode</th>
                <th class="py-2.5 px-4">Program Pembangunan</th>
                <th class="py-2.5 px-4 w-44">OPD Pengampu</th>
                <th class="py-2.5 px-4 text-right w-36">Pagu 5 Tahun</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="p in programList" :key="p.kode" class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
                <td class="py-2.5 px-4 text-center font-bold text-indigo-600">{{ p.kode }}</td>
                <td class="py-2.5 px-4 font-bold text-slate-900 dark:text-white">{{ p.nama }}</td>
                <td class="py-2.5 px-4 text-slate-600 dark:text-slate-300">{{ p.opd }}</td>
                <td class="py-2.5 px-4 text-right font-black text-emerald-600">{{ p.pagu }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 6: IKU -->
      <div v-if="activeTab === 'iku'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-bold border-b border-slate-200 dark:border-slate-800 text-[11px]">
              <tr>
                <th class="py-2.5 px-4">Indikator Kinerja Utama (IKU)</th>
                <th class="py-2.5 px-4 text-center w-20">Satuan</th>
                <th class="py-2.5 px-4 text-center w-20">2025</th>
                <th class="py-2.5 px-4 text-center w-20">2027</th>
                <th class="py-2.5 px-4 text-center w-24">Target 2029</th>
                <th class="py-2.5 px-4 w-40">Pengampu</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="i in ikuList" :key="i.nama" class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
                <td class="py-2.5 px-4 font-bold text-slate-900 dark:text-white">{{ i.nama }}</td>
                <td class="py-2.5 px-4 text-center text-slate-500">{{ i.satuan }}</td>
                <td class="py-2.5 px-4 text-center text-slate-600 dark:text-slate-400">{{ i.t25 }}</td>
                <td class="py-2.5 px-4 text-center text-slate-600 dark:text-slate-400">{{ i.t27 }}</td>
                <td class="py-2.5 px-4 text-center font-black text-emerald-600">{{ i.target }}</td>
                <td class="py-2.5 px-4 text-slate-700 dark:text-slate-300 font-medium">{{ i.opd }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 7: IKD -->
      <div v-if="activeTab === 'ikd'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-bold border-b border-slate-200 dark:border-slate-800 text-[11px]">
              <tr>
                <th class="py-2.5 px-4 w-16 text-center">Kode</th>
                <th class="py-2.5 px-4">Indikator Kinerja Daerah (IKD)</th>
                <th class="py-2.5 px-4 w-36">Aspek</th>
                <th class="py-2.5 px-4 text-center w-24">Target 2029</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="d in ikdList" :key="d.kode" class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
                <td class="py-2.5 px-4 text-center font-bold text-[#f39159]">{{ d.kode }}</td>
                <td class="py-2.5 px-4 font-bold text-slate-900 dark:text-white">{{ d.nama }}</td>
                <td class="py-2.5 px-4"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-[#308e87]/10 text-[#308e87]">{{ d.aspek }}</span></td>
                <td class="py-2.5 px-4 text-center font-black text-indigo-600">{{ d.target }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 8: PENDANAAN -->
      <div v-if="activeTab === 'pendanaan'" class="space-y-3">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm overflow-hidden">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-bold border-b border-slate-200 dark:border-slate-800 text-[11px]">
              <tr>
                <th class="py-2.5 px-4">Komponen Anggaran</th>
                <th class="py-2.5 px-4 text-right">2025</th>
                <th class="py-2.5 px-4 text-right">2027</th>
                <th class="py-2.5 px-4 text-right">2029</th>
                <th class="py-2.5 px-4 text-right">Total 5 Tahun</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="p in pendanaanList" :key="p.komponen" class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
                <td class="py-2.5 px-4 font-bold text-slate-900 dark:text-white">{{ p.komponen }}</td>
                <td class="py-2.5 px-4 text-right">{{ p.y25 }}</td>
                <td class="py-2.5 px-4 text-right">{{ p.y27 }}</td>
                <td class="py-2.5 px-4 text-right">{{ p.y29 }}</td>
                <td class="py-2.5 px-4 text-right font-black text-emerald-600">{{ p.total }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { Compass, Flag, Target, CheckCircle2, Layers, BarChart3, Award, Coins, Download, Plus } from 'lucide-vue-next'

const activeTab = ref('visi')

const visiData = ref({
  uraivisi: 'Tegal Berdikari Dan Sejahtera, Menjadi Kota Idaman',
  idperiode: '2025 - 2029',
  tahunpagu: '2026 - 2030'
})

const misiList = ref([])
const tujuanList = ref([])
const sasaranListLive = ref([])

const totalIndikatorCount = computed(() => {
  return tujuanList.value.reduce((acc, t) => acc + (t.indikator_list ? t.indikator_list.length : 0), 0)
})

const totalIndikatorSasaranCount = computed(() => {
  return sasaranListLive.value.reduce((acc, s) => acc + (s.indikator_list ? s.indikator_list.length : 0), 0)
})

const tabs = ref([
  { id: 'visi', label: 'Visi', icon: Compass, count: 1 },
  { id: 'misi', label: 'Misi', icon: Flag, count: 7 },
  { id: 'tujuan', label: 'Tujuan', icon: Target, count: 9 },
  { id: 'sasaran', label: 'Sasaran', icon: CheckCircle2, count: 24 },
  { id: 'program', label: 'Program', icon: Layers, count: 5 },
  { id: 'iku', label: 'IKU', icon: BarChart3, count: 5 },
  { id: 'ikd', label: 'IKD', icon: Award, count: 4 },
  { id: 'pendanaan', label: 'Proyeksi Pendanaan', icon: Coins, count: 4 }
])

async function fetchRpjmdData() {
  try {
    const resVisi = await axios.get('/api/v1/rpjmd/visi')
    if (resVisi.data) {
      visiData.value = resVisi.data
    }
  } catch (err) {
    console.error('Error fetching Visi RPJMD:', err)
  }

  try {
    const resMisi = await axios.get('/api/v1/rpjmd/misi')
    if (Array.isArray(resMisi.data)) {
      misiList.value = resMisi.data
      const misiTab = tabs.value.find(t => t.id === 'misi')
      if (misiTab) misiTab.count = resMisi.data.length
    }
  } catch (err) {
    console.error('Error fetching Misi RPJMD:', err)
  }

  try {
    const resTujuan = await axios.get('/api/v1/rpjmd/tujuan-lengkap')
    if (resTujuan.data && resTujuan.data.daftar_tujuan) {
      tujuanList.value = resTujuan.data.daftar_tujuan
      const tujuanTab = tabs.value.find(t => t.id === 'tujuan')
      if (tujuanTab) tujuanTab.count = resTujuan.data.daftar_tujuan.length
    }
  } catch (err) {
    console.error('Error fetching Tujuan RPJMD:', err)
  }

  try {
    const resSasaran = await axios.get('/api/v1/rpjmd/sasaran-lengkap')
    if (resSasaran.data && resSasaran.data.daftar_sasaran) {
      sasaranListLive.value = resSasaran.data.daftar_sasaran
      const sasaranTab = tabs.value.find(t => t.id === 'sasaran')
      if (sasaranTab) sasaranTab.count = resSasaran.data.daftar_sasaran.length
    }
  } catch (err) {
    console.error('Error fetching Sasaran RPJMD:', err)
  }
}

onMounted(() => {
  fetchRpjmdData()
})

const sasaranList = [
  { kode: 'S.01', uraian: 'Meningkatnya Mutu Layanan Pendidikan Usia Dini hingga Menengah', indikator: 'HLS (Tahun)', target: '14.2 Tahun' },
  { kode: 'S.02', uraian: 'Meningkatnya Derajat Kesehatan Ibu, Anak, dan Bebas Stunting', indikator: 'Prevalensi Stunting', target: '8.50%' },
  { kode: 'S.03', uraian: 'Meningkatnya Produksi Perikanan Tangkap dan Logistik Maritim', indikator: 'Nilai Produksi Ikan', target: 'Rp 850 M' },
  { kode: 'S.04', uraian: 'Menurunnya Luas Wilayah Terdampak Banjir Rob Pasang', indikator: 'Penurunan Genangan', target: '185 Ha' }
]

const programList = [
  { kode: 'PRG.01', nama: 'Program Pengelolaan Pendidikan dan Bantuan Siswa', opd: 'Dinas Pendidikan', pagu: 'Rp 425 Miliar' },
  { kode: 'PRG.02', nama: 'Program Pemenuhan Upaya Kesehatan Terpadu', opd: 'Dinas Kesehatan', pagu: 'Rp 580 Miliar' },
  { kode: 'PRG.03', nama: 'Program Daya Saing Perikanan Tangkap & Maritim', opd: 'DKPPP Kota Tegal', pagu: 'Rp 120 Miliar' },
  { kode: 'PRG.04', nama: 'Program Pengendalian Banjir Rob & Polder', opd: 'DPUPR Kota Tegal', pagu: 'Rp 340 Miliar' },
  { kode: 'PRG.05', nama: 'Program Penyelenggaraan SPBE Terpadu', opd: 'Diskominfo Kota Tegal', pagu: 'Rp 65 Miliar' }
]

const ikuList = [
  { nama: 'Indeks Pembangunan Manusia (IPM)', satuan: 'Poin', t25: '76.80', t27: '78.25', target: '79.80', opd: 'Bapperida' },
  { nama: 'Laju Pertumbuhan Ekonomi (LPE)', satuan: '%', t25: '5.20%', t27: '5.55%', target: '5.85%', opd: 'Dinas Koperasi UKM' },
  { nama: 'Tingkat Kemiskinan', satuan: '%', t25: '7.40%', t27: '6.80%', target: '6.20%', opd: 'Dinas Sosial' },
  { nama: 'Tingkat Pengangguran Terbuka (TPT)', satuan: '%', t25: '6.80%', t27: '6.00%', target: '5.20%', opd: 'Disnakerin' },
  { nama: 'Indeks Kualitas Lingkungan Hidup (IKLH)', satuan: 'Skor', t25: '69.00', t27: '72.00', target: '75.00', opd: 'DLH' }
]

const ikdList = [
  { kode: 'IKD.01', nama: 'Rasio Kemantapan Jalan Kota', aspek: 'Infrastruktur', target: '96.50%' },
  { kode: 'IKD.02', nama: 'Rumah Tangga Bersanitasi Layak', aspek: 'Permukiman', target: '98.00%' },
  { kode: 'IKD.03', nama: 'Cakupan Air Minum Perpipaan', aspek: 'Layanan Dasar', target: '88.00%' },
  { kode: 'IKD.04', nama: 'Indeks Kepuasan Masyarakat (IKM)', aspek: 'Tata Kelola', target: '90.50 Skor' }
]

const pendanaanList = [
  { komponen: 'Pendapatan Asli Daerah (PAD)', y25: 'Rp 380,5 M', y27: 'Rp 435,0 M', y29: 'Rp 475,0 M', total: 'Rp 2.156,2 M' },
  { komponen: 'Pendapatan Transfer (DAU/DAK)', y25: 'Rp 810,0 M', y27: 'Rp 860,0 M', y29: 'Rp 910,0 M', total: 'Rp 4.300,0 M' },
  { komponen: 'Belanja Operasi (Pegawai & Barang)', y25: 'Rp 750,0 M', y27: 'Rp 800,0 M', y29: 'Rp 840,0 M', total: 'Rp 3.985,0 M' },
  { komponen: 'Belanja Modal & Program Prioritas', y25: 'Rp 460,0 M', y27: 'Rp 520,0 M', y29: 'Rp 580,0 M', total: 'Rp 2.605,0 M' }
]

const showSwal = (title, text) => {
  Swal.fire({
    title,
    text,
    icon: 'info',
    confirmButtonColor: '#4f46e5',
    timer: 2000
  })
}
</script>
