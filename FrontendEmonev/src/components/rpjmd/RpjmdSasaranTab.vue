<template>
  <div class="space-y-4">

    <!-- Top Action Bar & Search -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <div class="relative flex-1 md:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQuerySasaran"
            type="text" 
            placeholder="Cari sasaran, indikator, tujuan, atau misi..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>
        <button 
          @click="expandAllSasaran"
          class="px-3 py-2 text-[11px] font-bold rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 shrink-0 cursor-pointer"
          title="Buka semua node tree"
        >
          Buka Semua
        </button>
        <button 
          @click="collapseAllSasaran"
          class="px-3 py-2 text-[11px] font-bold rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 shrink-0 cursor-pointer"
          title="Tutup semua node tree"
        >
          Tutup Semua
        </button>
      </div>

      <div class="flex items-center space-x-2 w-full md:w-auto justify-end">
        <button 
          @click="fetchSasaranData"
          :disabled="loadingSasaran"
          class="p-2 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 cursor-pointer disabled:opacity-50"
          title="Segarkan Data"
        >
          <RotateCw class="w-4 h-4" :class="loadingSasaran ? 'animate-spin' : ''" />
        </button>
        <button 
          @click="openAddSasaranModal"
          class="px-4 py-2 text-xs font-black rounded-xl bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 transition-all active:scale-95 cursor-pointer"
        >
          <Plus class="w-4 h-4" />
          <span>Tambah Sasaran RPJMD</span>
        </button>
      </div>
    </div>

    <!-- Data Summary Badge -->
    <div class="flex flex-wrap items-center justify-between gap-2 px-1 text-xs text-slate-500 dark:text-slate-400 font-semibold">
      <div class="flex items-center space-x-2">
        <span class="inline-flex items-center px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-[11px] font-black">
          {{ filteredSasaranList.length }} Sasaran Daerah
        </span>
        <span class="inline-flex items-center px-2.5 py-1 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 text-[11px] font-black">
          {{ totalIndikatorSasaranCount }} Indikator Kinerja
        </span>
      </div>
      <div class="text-[11px] text-slate-400">
        Database: <code class="text-slate-600 dark:text-slate-300 font-mono">rpjmd_sasaran</code> &amp; <code class="text-slate-600 dark:text-slate-300 font-mono">rpjmd_indikator_sasaran</code>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingSasaran" class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-12 text-center shadow-sm">
      <Loader2 class="w-8 h-8 animate-spin mx-auto text-[#308e87] mb-3" />
      <p class="text-xs font-bold text-slate-600 dark:text-slate-400">Memuat Tree Tabel Sasaran RPJMD...</p>
    </div>

    <!-- ==================== UNIFIED TREE TABLE: SASARAN RPJMD ==================== -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-100/90 dark:bg-slate-800/90 text-[10px] font-black uppercase tracking-wider text-slate-600 dark:text-slate-300 select-none">
              <th rowspan="2" class="py-3 px-3 w-20 text-center border-r border-slate-200 dark:border-slate-700/80">No / Kode</th>
              <th rowspan="2" class="py-3 px-3.5 min-w-[180px] max-w-[240px] border-r border-slate-200 dark:border-slate-700/80 bg-indigo-50/50 dark:bg-indigo-950/20 text-indigo-700 dark:text-indigo-300 font-black">Misi</th>
              <th rowspan="2" class="py-3 px-3.5 min-w-[200px] max-w-[260px] border-r border-slate-200 dark:border-slate-700/80 bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black">Tujuan Terkait</th>
              <th rowspan="2" class="py-3 px-4 min-w-[260px] border-r border-slate-200 dark:border-slate-700/80">Sasaran Pembangunan / Indikator Sasaran</th>
              <th rowspan="2" class="py-3 px-3 w-20 text-center border-r border-slate-200 dark:border-slate-700/80">Satuan</th>
              <th rowspan="2" class="py-3 px-3 w-24 text-center border-r border-slate-200 dark:border-slate-700/80 bg-amber-50/50 dark:bg-amber-950/20 text-amber-800 dark:text-amber-300">Baseline</th>
              <th colspan="6" class="py-2 px-2 text-center border-b border-r border-slate-200 dark:border-slate-700/80 bg-teal-500/10 text-teal-700 dark:text-teal-300 font-black">
                Target Per Tahun Periode RPJMD 2025–2030
              </th>
              <th rowspan="2" class="py-3 px-4 w-24 text-center">Aksi</th>
            </tr>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[10px] font-bold text-slate-600 dark:text-slate-300">
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-blue-700 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20">
                2025<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(target0)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-cyan-700 dark:text-cyan-400 bg-cyan-50/40 dark:bg-cyan-950/20">
                2026<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(target1)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-teal-700 dark:text-teal-400 bg-teal-50/40 dark:bg-teal-950/20">
                2027<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(target2)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-indigo-700 dark:text-indigo-400 bg-indigo-50/40 dark:bg-indigo-950/20">
                2028<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(target3)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-amber-700 dark:text-amber-400 bg-amber-50/40 dark:bg-amber-950/20">
                2029<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(target4)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-emerald-700 dark:text-emerald-400 bg-emerald-50/40 dark:bg-emerald-950/20 font-black">
                2030<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(Akhir)</span>
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
            <template v-for="s in filteredSasaranList" :key="s.idsasaran">
              <!-- PARENT ROW: SASARAN RPJMD -->
              <tr 
                @click="toggleSasaranExpand(s.idsasaran)"
                class="bg-slate-50/90 dark:bg-slate-800/70 hover:bg-slate-100/90 dark:hover:bg-slate-800 font-bold transition-colors cursor-pointer border-t-2 border-slate-200 dark:border-slate-700 select-none"
              >
                <!-- Kode & Expand Toggle -->
                <td class="py-3 px-3 border-r border-slate-200/60 dark:border-slate-800/60 align-top">
                  <div class="flex items-center space-x-1.5">
                    <button 
                      @click.stop="toggleSasaranExpand(s.idsasaran)" 
                      class="p-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 transition-transform"
                    >
                      <ChevronDown v-if="expandedSasaranMap[s.idsasaran]" class="w-4 h-4 text-[#308e87]" />
                      <ChevronRight v-else class="w-4 h-4 text-slate-400" />
                    </button>
                    <span class="px-2 py-0.5 rounded-lg text-xs font-black bg-[#f39159] text-white shadow-sm shadow-[#f39159]/20">
                      S-{{ s.urut }}
                    </span>
                  </div>
                </td>

                <!-- Misi Column with Sentence -->
                <td class="py-3 px-3.5 border-r border-slate-200/60 dark:border-slate-800/60 bg-indigo-50/15 dark:bg-indigo-950/10 align-top">
                  <div v-if="s.uraimisi || s.urut_misi" class="space-y-1">
                    <span class="inline-block px-1.5 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 text-[10px] font-black border border-indigo-200 dark:border-indigo-800 whitespace-nowrap">
                      Misi {{ s.urut_misi }}
                    </span>
                    <p class="text-[11px] text-slate-700 dark:text-slate-300 font-medium leading-snug">
                      {{ s.uraimisi }}
                    </p>
                  </div>
                  <span v-else class="text-slate-400 text-[10px]">-</span>
                </td>

                <!-- Tujuan Column with Sentence -->
                <td class="py-3 px-3.5 border-r border-slate-200/60 dark:border-slate-800/60 bg-[#308e87]/5 dark:bg-[#308e87]/10 align-top">
                  <div v-if="s.uraitujuan || s.urut_tujuan" class="space-y-1">
                    <span class="inline-block px-1.5 py-0.5 rounded bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] text-[10px] font-black border border-[#308e87]/30 whitespace-nowrap">
                      T-{{ s.urut_tujuan }}
                    </span>
                    <p class="text-[11px] text-slate-700 dark:text-slate-300 font-medium leading-snug">
                      {{ s.uraitujuan }}
                    </p>
                  </div>
                  <span v-else class="text-slate-400 text-[10px]">-</span>
                </td>

                <!-- Uraian Sasaran -->
                <td class="py-3 px-4 text-slate-900 dark:text-white font-extrabold text-xs leading-snug border-r border-slate-200/60 dark:border-slate-800/60 align-top">
                  <div class="flex items-center space-x-2">
                    <span>{{ s.uraisasaran }}</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#f39159]/10 text-[#f39159] border border-[#f39159]/20 shrink-0">
                      {{ s.indikator_list ? s.indikator_list.length : 0 }} Indikator
                    </span>
                  </div>
                </td>

                <!-- Blank Columns for Parent (6 Target Columns) -->
                <td class="py-3 px-3 text-center text-slate-400 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-3 text-center text-slate-400 border-r border-slate-200/60 dark:border-slate-800/60 bg-amber-50/10">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-blue-50/20 dark:bg-blue-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-cyan-50/20 dark:bg-cyan-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-teal-50/20 dark:bg-teal-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-indigo-50/20 dark:bg-indigo-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-amber-50/20 dark:bg-amber-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-emerald-50/20 dark:bg-emerald-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>

                <!-- Parent Actions -->
                <td class="py-3 px-4 text-center" @click.stop>
                  <div class="flex items-center justify-center space-x-1">
                    <button 
                      @click="openAddIndikatorSasaranModal(s.idsasaran)"
                      class="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 cursor-pointer"
                      title="Tambah Indikator di Sasaran ini"
                    >
                      <Plus class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="openEditSasaranModal(s)"
                      class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 cursor-pointer"
                      title="Edit Sasaran"
                    >
                      <Edit3 class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="handleDeleteSasaran(s)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                      title="Hapus Sasaran"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>

              <!-- CHILD ROWS: INDIKATOR SASARAN (Tampil saat expanded) -->
              <template v-if="expandedSasaranMap[s.idsasaran]">
                <tr v-if="!s.indikator_list || s.indikator_list.length === 0">
                  <td colspan="13" class="py-4 pl-12 pr-4 text-slate-400 italic bg-white dark:bg-[#141d30]">
                    <div class="flex items-center space-x-2 text-xs">
                      <CornerDownRight class="w-4 h-4 text-slate-400" />
                      <span>Belum ada indikator sasaran terdaftar. Klik tombol <strong>+</strong> pada baris di atas untuk menambahkan indikator.</span>
                    </div>
                  </td>
                </tr>

                <tr 
                  v-for="ind in s.indikator_list" 
                  :key="ind.idsasaran_indikator"
                  class="bg-white dark:bg-[#141d30] hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <!-- Indikator Kode with Tree Branch Icon -->
                  <td class="py-2.5 px-3 pl-6 border-r border-slate-100 dark:border-slate-800/60">
                    <div class="flex items-center space-x-1.5 font-mono text-xs">
                      <CornerDownRight class="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span class="font-bold text-[#f39159]">
                        #{{ ind.urut }}
                      </span>
                    </div>
                  </td>

                  <!-- Misi & Tujuan blank cell for Child Row -->
                  <td class="py-2.5 px-3 text-center border-r border-slate-100 dark:border-slate-800/60 bg-slate-50/30 dark:bg-slate-900/20 text-slate-300 dark:text-slate-600">
                    -
                  </td>
                  <td class="py-2.5 px-3 text-center border-r border-slate-100 dark:border-slate-800/60 bg-slate-50/30 dark:bg-slate-900/20 text-slate-300 dark:text-slate-600">
                    -
                  </td>

                  <!-- Uraian Indikator Sasaran -->
                  <td class="py-2.5 px-4 text-slate-800 dark:text-slate-200 font-semibold leading-relaxed border-r border-slate-100 dark:border-slate-800/60">
                    <div class="space-y-1">
                      <div class="flex flex-wrap items-center gap-1.5">
                        <span class="text-xs font-bold">{{ ind.uraisasaran_indikator }}</span>
                        <span v-if="ind.iku === '1' || ind.iku === true" class="px-1.5 py-0.2 rounded text-[9px] font-black bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                          IKU
                        </span>
                        <span v-if="ind.ikd === '1' || ind.ikd === true" class="px-1.5 py-0.2 rounded text-[9px] font-black bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                          IKD
                        </span>
                      </div>
                      <span v-if="ind.uraiaspek" class="text-[10px] text-slate-400 block font-normal">
                        Aspek: {{ ind.uraiaspek }}
                      </span>
                    </div>
                  </td>

                  <!-- Satuan -->
                  <td class="py-2.5 px-3 text-center text-slate-500 font-medium border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.satuan || '-' }}
                  </td>

                  <!-- Baseline -->
                  <td class="py-2.5 px-3 text-center font-bold text-amber-700 dark:text-amber-400 bg-amber-50/30 dark:bg-amber-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.baseline || '-' }}
                  </td>

                  <!-- Target 2025 (target0) -->
                  <td class="py-2.5 px-2 text-center font-bold text-blue-600 dark:text-blue-400 bg-blue-50/20 dark:bg-blue-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target0 || '-' }}
                  </td>

                  <!-- Target 2026 (target1) -->
                  <td class="py-2.5 px-2 text-center font-bold text-cyan-600 dark:text-cyan-400 bg-cyan-50/20 dark:bg-cyan-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target1 || '-' }}
                  </td>

                  <!-- Target 2027 (target2) -->
                  <td class="py-2.5 px-2 text-center font-bold text-teal-600 dark:text-teal-400 bg-teal-50/20 dark:bg-teal-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target2 || '-' }}
                  </td>

                  <!-- Target 2028 (target3) -->
                  <td class="py-2.5 px-2 text-center font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50/20 dark:bg-indigo-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target3 || '-' }}
                  </td>

                  <!-- Target 2029 (target4) -->
                  <td class="py-2.5 px-2 text-center font-bold text-amber-600 dark:text-amber-400 bg-amber-50/20 dark:bg-amber-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target4 || '-' }}
                  </td>

                  <!-- Target 2030 (target5 / Akhir) -->
                  <td class="py-2.5 px-2 text-center font-black text-emerald-600 dark:text-emerald-400 bg-emerald-50/30 dark:bg-emerald-950/20 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target5 || '-' }}
                  </td>

                  <!-- Child Actions -->
                  <td class="py-2.5 px-4 text-center">
                    <div class="flex items-center justify-center space-x-1">
                      <button 
                        @click="openEditIndikatorSasaranModal(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer"
                        title="Edit Indikator Sasaran"
                      >
                        <Edit3 class="w-3.5 h-3.5" />
                      </button>
                      <button 
                        @click="handleDeleteIndikatorSasaran(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 cursor-pointer"
                        title="Hapus Indikator Sasaran"
                      >
                        <Trash2 class="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              </template>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ==================== MODAL: TAMBAH / EDIT SASARAN ==================== -->
    <div 
      v-if="showSasaranModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showSasaranModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#f39159]/10 text-[#f39159] flex items-center justify-center">
              <Compass class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditSasaran ? 'Edit Sasaran RPJMD' : 'Tambah Sasaran RPJMD' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjmd_sasaran</code></p>
            </div>
          </div>
          <button @click="showSasaranModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveSasaranData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Tujuan RPJMD Terkait</label>
              <select 
                v-model="sasaranForm.idtujuan" 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              >
                <option value="">-- Pilih Tujuan --</option>
                <option v-for="t in tujuanList" :key="t.idtujuan" :value="t.idtujuan">
                  [T-{{ t.urut }}] {{ t.uraitujuan.substring(0, 45) }}...
                </option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut Sasaran</label>
              <input 
                v-model.number="sasaranForm.urut" 
                type="number" 
                min="1"
                required
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Sasaran Pembangunan RPJMD</label>
            <textarea 
              v-model="sasaranForm.uraisasaran" 
              rows="3" 
              required
              placeholder="Masukkan uraian sasaran pembangunan RPJMD..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-semibold leading-relaxed"
            ></textarea>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showSasaranModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingSasaran"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingSasaran" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditSasaran ? 'Simpan Perubahan' : 'Tambah Sasaran' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== MODAL: TAMBAH / EDIT INDIKATOR SASARAN ==================== -->
    <div 
      v-if="showIndikatorSasaranModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showIndikatorSasaranModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-2xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150 my-8 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-teal-500/10 text-teal-600 flex items-center justify-center">
              <Compass class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditIndikatorSasaran ? 'Edit Indikator Sasaran RPJMD' : 'Tambah Indikator Sasaran RPJMD' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjmd_indikator_sasaran</code></p>
            </div>
          </div>
          <button @click="showIndikatorSasaranModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveIndikatorSasaranData" class="space-y-4 text-xs">
          <!-- Pilih Sasaran -->
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Sasaran RPJMD Terkait</label>
            <select 
              v-model="indikatorSasaranForm.idsasaran" 
              required
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
            >
              <option value="">-- Pilih Sasaran --</option>
              <option v-for="s in sasaranList" :key="s.idsasaran" :value="s.idsasaran">
                [S-{{ s.urut }}] {{ s.uraisasaran.substring(0, 60) }}...
              </option>
            </select>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Indikator Sasaran</label>
              <input 
                v-model="indikatorSasaranForm.uraisasaran_indikator" 
                type="text" 
                required
                placeholder="Nama tolok ukur/indikator..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut Indikator</label>
              <input 
                v-model.number="indikatorSasaranForm.urut" 
                type="number" 
                min="1"
                required
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Satuan</label>
              <input 
                v-model="indikatorSasaranForm.satuan" 
                type="text" 
                placeholder="Angka, %, Nilai, Tahun" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Status Polaritas</label>
              <select 
                v-model="indikatorSasaranForm.status" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              >
                <option value="positif">Positif (Makin tinggi makin baik)</option>
                <option value="negatif">Negatif (Makin rendah makin baik)</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Baseline / 2024</label>
              <input 
                v-model="indikatorSasaranForm.baseline" 
                type="text" 
                placeholder="Contoh: 68.57" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
          </div>

          <!-- Target RPJMD 2025–2030 (target0 to target5) -->
          <div class="p-3.5 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-200/80 dark:border-slate-700/80 space-y-2">
            <span class="block text-[10px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Target Tahunan RPJMD (2025–2030)
            </span>
            <div class="grid grid-cols-2 sm:grid-cols-6 gap-2">
              <div>
                <label class="block text-[10px] font-bold text-blue-600 dark:text-blue-400 mb-1">2025 (target0)</label>
                <input 
                  v-model="indikatorSasaranForm.target0" 
                  type="text" 
                  placeholder="69.03" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-cyan-600 dark:text-cyan-400 mb-1">2026 (target1)</label>
                <input 
                  v-model="indikatorSasaranForm.target1" 
                  type="text" 
                  placeholder="69.50" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-teal-600 dark:text-teal-400 mb-1">2027 (target2)</label>
                <input 
                  v-model="indikatorSasaranForm.target2" 
                  type="text" 
                  placeholder="69.96" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-indigo-600 dark:text-indigo-400 mb-1">2028 (target3)</label>
                <input 
                  v-model="indikatorSasaranForm.target3" 
                  type="text" 
                  placeholder="70.43" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-amber-600 dark:text-amber-400 mb-1">2029 (target4)</label>
                <input 
                  v-model="indikatorSasaranForm.target4" 
                  type="text" 
                  placeholder="70.89" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mb-1">2030 (target5)</label>
                <input 
                  v-model="indikatorSasaranForm.target5" 
                  type="text" 
                  placeholder="71.35" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-black text-xs"
                />
              </div>
            </div>
          </div>

          <!-- Aspek -->
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Aspek</label>
            <input 
              v-model="indikatorSasaranForm.uraiaspek" 
              type="text" 
              placeholder="Contoh: ASPEK KESEJAHTERAAN MASYARAKAT / ASPEK PELAYANAN UMUM" 
              class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white"
            />
          </div>

          <!-- Tagging IKU / IKD -->
          <div class="flex items-center space-x-6 p-2 rounded-xl bg-slate-50 dark:bg-slate-800/40">
            <label class="flex items-center space-x-2 cursor-pointer">
              <input type="checkbox" v-model="indikatorSasaranForm.iku" class="rounded text-[#308e87] focus:ring-[#308e87] w-4 h-4" />
              <span class="font-bold text-slate-700 dark:text-slate-200">Indikator Kinerja Utama (IKU)</span>
            </label>
            <label class="flex items-center space-x-2 cursor-pointer">
              <input type="checkbox" v-model="indikatorSasaranForm.ikd" class="rounded text-[#308e87] focus:ring-[#308e87] w-4 h-4" />
              <span class="font-bold text-slate-700 dark:text-slate-200">Indikator Kinerja Daerah (IKD)</span>
            </label>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showIndikatorSasaranModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingIndikatorSasaran"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingIndikatorSasaran" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditIndikatorSasaran ? 'Simpan Perubahan' : 'Tambah Indikator' }}</span>
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
import { Compass, Search, Plus, RotateCw, Loader2, Edit3, Trash2, ChevronDown, ChevronRight, CornerDownRight } from 'lucide-vue-next'

const searchQuerySasaran = ref('')
const expandedSasaranMap = ref({})
const loadingSasaran = ref(false)
const savingSasaran = ref(false)
const savingIndikatorSasaran = ref(false)

const sasaranList = ref([])
const tujuanList = ref([])

const showSasaranModal = ref(false)
const isEditSasaran = ref(false)
const currentSasaranId = ref(null)
const sasaranForm = ref({
  uraisasaran: '',
  urut: 1,
  idtujuan: ''
})

const showIndikatorSasaranModal = ref(false)
const isEditIndikatorSasaran = ref(false)
const currentIndikatorSasaranId = ref(null)
const indikatorSasaranForm = ref({
  idsasaran: '',
  uraisasaran_indikator: '',
  satuan: 'Angka',
  status: 'positif',
  baseline: '',
  target0: '',
  target1: '',
  target2: '',
  target3: '',
  target4: '',
  target5: '',
  tipe_data: 'numeric',
  kodeindikator_master: '',
  sumber: 'MASTER',
  iku: false,
  ikd: false,
  uraiaspek: '',
  urut: 1
})

const totalIndikatorSasaranCount = computed(() => {
  return sasaranList.value.reduce((acc, s) => acc + (s.indikator_list ? s.indikator_list.length : 0), 0)
})

const filteredSasaranList = computed(() => {
  if (!searchQuerySasaran.value) return sasaranList.value
  const q = searchQuerySasaran.value.toLowerCase()
  return sasaranList.value.filter(s => {
    const matchSasaran = (s.uraisasaran && s.uraisasaran.toLowerCase().includes(q)) || 
                         (s.urut && s.urut.toString().includes(q)) ||
                         (s.uraitujuan && s.uraitujuan.toLowerCase().includes(q)) ||
                         (s.uraimisi && s.uraimisi.toLowerCase().includes(q)) ||
                         (s.urut_misi && s.urut_misi.toString().includes(q))
    const matchIndikator = s.indikator_list && s.indikator_list.some(ind => 
      (ind.uraisasaran_indikator && ind.uraisasaran_indikator.toLowerCase().includes(q)) ||
      (ind.satuan && ind.satuan.toLowerCase().includes(q)) ||
      (ind.uraiaspek && ind.uraiaspek.toLowerCase().includes(q))
    )
    if (matchSasaran || matchIndikator) {
      expandedSasaranMap.value[s.idsasaran] = true
      return true
    }
    return false
  })
})

function toggleSasaranExpand(idsasaran) {
  expandedSasaranMap.value[idsasaran] = !expandedSasaranMap.value[idsasaran]
}

function expandAllSasaran() {
  sasaranList.value.forEach(s => {
    expandedSasaranMap.value[s.idsasaran] = true
  })
}

function collapseAllSasaran() {
  sasaranList.value.forEach(s => {
    expandedSasaranMap.value[s.idsasaran] = false
  })
}

async function fetchSasaranData() {
  loadingSasaran.value = true
  try {
    const [resSasaran, resTujuan] = await Promise.all([
      axios.get('/api/v1/rpjmd/sasaran-lengkap'),
      axios.get('/api/v1/rpjmd/tujuan')
    ])

    if (resSasaran.data && resSasaran.data.daftar_sasaran) {
      sasaranList.value = resSasaran.data.daftar_sasaran
      resSasaran.data.daftar_sasaran.forEach(s => {
        if (expandedSasaranMap.value[s.idsasaran] === undefined) {
          expandedSasaranMap.value[s.idsasaran] = true
        }
      })
    }

    if (Array.isArray(resTujuan.data)) {
      tujuanList.value = resTujuan.data
    }
  } catch (err) {
    console.error('Error fetching RPJMD Sasaran data:', err)
  } finally {
    loadingSasaran.value = false
  }
}

function openAddSasaranModal() {
  isEditSasaran.value = false
  currentSasaranId.value = null
  sasaranForm.value = {
    uraisasaran: '',
    urut: sasaranList.value.length + 1,
    idtujuan: tujuanList.value[0]?.idtujuan || ''
  }
  showSasaranModal.value = true
}

function openEditSasaranModal(s) {
  isEditSasaran.value = true
  currentSasaranId.value = s.idsasaran
  sasaranForm.value = {
    uraisasaran: s.uraisasaran,
    urut: s.urut || 1,
    idtujuan: s.idtujuan || ''
  }
  showSasaranModal.value = true
}

async function saveSasaranData() {
  savingSasaran.value = true
  try {
    const payload = {
      uraisasaran: sasaranForm.value.uraisasaran,
      urut: sasaranForm.value.urut,
      idtujuan: sasaranForm.value.idtujuan || null
    }

    if (isEditSasaran.value) {
      await axios.put(`/api/v1/rpjmd/sasaran/${currentSasaranId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjmd/sasaran', payload)
    }
    showSasaranModal.value = false
    await fetchSasaranData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditSasaran.value ? 'Sasaran RPJMD berhasil diperbarui' : 'Sasaran RPJMD baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Sasaran RPJMD', 'error')
  } finally {
    savingSasaran.value = false
  }
}

async function handleDeleteSasaran(s) {
  const res = await Swal.fire({
    title: 'Hapus Sasaran RPJMD?',
    text: `Sasaran "S-${s.urut}: ${s.uraisasaran}" beserta seluruh indikator terkait akan dihapus permanen!`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus!',
    cancelButtonText: 'Batal'
  })

  if (res.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjmd/sasaran/${s.idsasaran}`)
      await fetchSasaranData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Sasaran RPJMD berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Sasaran RPJMD', 'error')
    }
  }
}

function openAddIndikatorSasaranModal(idsasaran) {
  isEditIndikatorSasaran.value = false
  currentIndikatorSasaranId.value = null
  const parentSasaran = sasaranList.value.find(s => s.idsasaran === idsasaran)
  const nextUrut = (parentSasaran && parentSasaran.indikator_list) ? parentSasaran.indikator_list.length + 1 : 1

  indikatorSasaranForm.value = {
    idsasaran: idsasaran,
    uraisasaran_indikator: '',
    satuan: 'Angka',
    status: 'positif',
    baseline: '',
    target0: '',
    target1: '',
    target2: '',
    target3: '',
    target4: '',
    target5: '',
    tipe_data: 'numeric',
    kodeindikator_master: '',
    sumber: 'MASTER',
    iku: false,
    ikd: false,
    uraiaspek: '',
    urut: nextUrut
  }
  showIndikatorSasaranModal.value = true
}

function openEditIndikatorSasaranModal(ind) {
  isEditIndikatorSasaran.value = true
  currentIndikatorSasaranId.value = ind.idsasaran_indikator
  indikatorSasaranForm.value = {
    idsasaran: ind.idsasaran,
    uraisasaran_indikator: ind.uraisasaran_indikator,
    satuan: ind.satuan || 'Angka',
    status: ind.status || 'positif',
    baseline: ind.baseline || '',
    target0: ind.target0 || '',
    target1: ind.target1 || '',
    target2: ind.target2 || '',
    target3: ind.target3 || '',
    target4: ind.target4 || '',
    target5: ind.target5 || '',
    tipe_data: ind.tipe_data || 'numeric',
    kodeindikator_master: ind.kodeindikator_master || '',
    sumber: ind.sumber || 'MASTER',
    iku: ind.iku === '1' || ind.iku === true,
    ikd: ind.ikd === '1' || ind.ikd === true,
    uraiaspek: ind.uraiaspek || '',
    urut: ind.urut || 1
  }
  showIndikatorSasaranModal.value = true
}

async function saveIndikatorSasaranData() {
  savingIndikatorSasaran.value = true
  try {
    const payload = {
      idsasaran: indikatorSasaranForm.value.idsasaran,
      uraisasaran_indikator: indikatorSasaranForm.value.uraisasaran_indikator,
      satuan: indikatorSasaranForm.value.satuan,
      status: indikatorSasaranForm.value.status,
      baseline: indikatorSasaranForm.value.baseline,
      target0: indikatorSasaranForm.value.target0,
      target1: indikatorSasaranForm.value.target1,
      target2: indikatorSasaranForm.value.target2,
      target3: indikatorSasaranForm.value.target3,
      target4: indikatorSasaranForm.value.target4,
      target5: indikatorSasaranForm.value.target5,
      tipe_data: indikatorSasaranForm.value.tipe_data,
      kodeindikator_master: indikatorSasaranForm.value.kodeindikator_master || null,
      sumber: indikatorSasaranForm.value.sumber,
      iku: indikatorSasaranForm.value.iku,
      ikd: indikatorSasaranForm.value.ikd,
      uraiaspek: indikatorSasaranForm.value.uraiaspek || null,
      urut: indikatorSasaranForm.value.urut
    }

    if (isEditIndikatorSasaran.value) {
      await axios.put(`/api/v1/rpjmd/indikator-sasaran/${currentIndikatorSasaranId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjmd/indikator-sasaran', payload)
    }
    showIndikatorSasaranModal.value = false
    await fetchSasaranData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditIndikatorSasaran.value ? 'Indikator Sasaran berhasil diperbarui' : 'Indikator Sasaran baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Indikator Sasaran', 'error')
  } finally {
    savingIndikatorSasaran.value = false
  }
}

async function handleDeleteIndikatorSasaran(ind) {
  const res = await Swal.fire({
    title: 'Hapus Indikator Sasaran?',
    text: `Indikator "${ind.uraisasaran_indikator}" akan dihapus permanen!`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus!',
    cancelButtonText: 'Batal'
  })

  if (res.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjmd/indikator-sasaran/${ind.idsasaran_indikator}`)
      await fetchSasaranData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Indikator Sasaran berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Indikator Sasaran', 'error')
    }
  }
}

defineExpose({
  fetchSasaranData,
  openAddSasaranModal
})

onMounted(() => {
  fetchSasaranData()
})
</script>
