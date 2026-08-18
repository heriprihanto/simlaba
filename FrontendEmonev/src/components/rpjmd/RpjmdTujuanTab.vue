<template>
  <div class="space-y-4">
    
    <!-- Toolbar & Actions -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <!-- Search input -->
        <div class="relative w-full md:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQueryTujuan"
            type="text" 
            placeholder="Cari tujuan atau indikator tujuan..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>

        <!-- Expand / Collapse All Buttons -->
        <div class="flex items-center space-x-1.5 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shrink-0">
          <button 
            @click="expandAllTujuan"
            class="px-2.5 py-1 text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#308e87] rounded-lg transition-colors cursor-pointer"
            title="Buka Semua Tree Tujuan"
          >
            Buka Semua
          </button>
          <span class="text-slate-300 dark:text-slate-600">|</span>
          <button 
            @click="collapseAllTujuan"
            class="px-2.5 py-1 text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#308e87] rounded-lg transition-colors cursor-pointer"
            title="Tutup Semua Tree Tujuan"
          >
            Tutup Semua
          </button>
        </div>

        <button 
          @click="fetchTujuanData"
          class="p-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer shrink-0"
          title="Segarkan Data Tujuan RPJMD"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loadingTujuan }" />
        </button>
      </div>

      <div class="flex items-center space-x-3 self-end md:self-center">
        <span class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <strong>{{ tujuanList.length }}</strong> Tujuan • <strong>{{ totalIndikatorTujuanCount }}</strong> Indikator
        </span>
        <button 
          @click="openAddTujuanModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#308e87] hover:bg-[#27756f] text-white flex items-center space-x-1.5 shadow-sm shadow-[#308e87]/30 cursor-pointer"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Tujuan RPJMD</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingTujuan" class="py-16 flex flex-col items-center justify-center space-y-3 text-slate-400">
      <Loader2 class="w-8 h-8 animate-spin text-[#308e87]" />
      <span class="text-xs font-bold">Memuat Tree Tabel Tujuan RPJMD...</span>
    </div>

    <!-- ==================== UNIFIED TREE TABLE: TUJUAN RPJMD ==================== -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-100/90 dark:bg-slate-800/90 text-[10px] font-black uppercase tracking-wider text-slate-600 dark:text-slate-300 select-none">
              <th rowspan="2" class="py-3 px-3 w-20 text-center border-r border-slate-200 dark:border-slate-700/80">No / Kode</th>
              <th rowspan="2" class="py-3 px-3.5 min-w-[200px] max-w-[260px] border-r border-slate-200 dark:border-slate-700/80 bg-indigo-50/50 dark:bg-indigo-950/20 text-indigo-700 dark:text-indigo-300 font-black">Misi RPJMD</th>
              <th rowspan="2" class="py-3 px-4 min-w-[260px] border-r border-slate-200 dark:border-slate-700/80">Tujuan Pembangunan / Indikator Kinerja</th>
              <th rowspan="2" class="py-3 px-3 w-20 text-center border-r border-slate-200 dark:border-slate-700/80">Satuan</th>
              <th rowspan="2" class="py-3 px-3 w-24 text-center border-r border-slate-200 dark:border-slate-700/80 bg-amber-50/50 dark:bg-amber-950/20 text-amber-800 dark:text-amber-300">Baseline</th>
              <th colspan="6" class="py-2 px-2 text-center border-b border-r border-slate-200 dark:border-slate-700/80 bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black">
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
            <template v-for="t in filteredTujuanList" :key="t.idtujuan">
              <!-- PARENT ROW: TUJUAN RPJMD -->
              <tr 
                @click="toggleTujuanExpand(t.idtujuan)"
                class="bg-slate-50/90 dark:bg-slate-800/70 hover:bg-slate-100/90 dark:hover:bg-slate-800 font-bold transition-colors cursor-pointer border-t-2 border-slate-200 dark:border-slate-700 select-none"
              >
                <!-- Kode & Expand Toggle -->
                <td class="py-3 px-3 border-r border-slate-200/60 dark:border-slate-800/60 align-top">
                  <div class="flex items-center space-x-1.5">
                    <button 
                      @click.stop="toggleTujuanExpand(t.idtujuan)" 
                      class="p-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 transition-transform"
                    >
                      <ChevronDown v-if="expandedTujuanMap[t.idtujuan]" class="w-4 h-4 text-[#308e87]" />
                      <ChevronRight v-else class="w-4 h-4 text-slate-400" />
                    </button>
                    <span class="px-2 py-0.5 rounded-lg text-xs font-black bg-[#308e87] text-white shadow-sm shadow-[#308e87]/20">
                      T-{{ t.urut }}
                    </span>
                  </div>
                </td>

                <!-- Misi Column with Full Sentence -->
                <td class="py-3 px-3.5 border-r border-slate-200/60 dark:border-slate-800/60 bg-indigo-50/15 dark:bg-indigo-950/10 align-top">
                  <div v-if="t.uraimisi || t.urut_misi" class="space-y-1">
                    <span class="inline-block px-1.5 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 text-[10px] font-black border border-indigo-200 dark:border-indigo-800 whitespace-nowrap">
                      Misi {{ t.urut_misi }}
                    </span>
                    <p class="text-[11px] text-slate-700 dark:text-slate-300 font-semibold leading-snug">
                      {{ t.uraimisi }}
                    </p>
                  </div>
                  <span v-else class="text-slate-400 text-[10px]">-</span>
                </td>

                <!-- Uraian Tujuan -->
                <td class="py-3 px-4 text-slate-900 dark:text-white font-extrabold text-xs leading-snug border-r border-slate-200/60 dark:border-slate-800/60 align-top">
                  <div class="flex items-center space-x-2">
                    <span>{{ t.uraitujuan }}</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#308e87]/10 text-[#308e87] border border-[#308e87]/20 shrink-0">
                      {{ t.indikator_list ? t.indikator_list.length : 0 }} Indikator
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
                      @click="openAddIndikatorTujuanModal(t.idtujuan)"
                      class="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 cursor-pointer"
                      title="Tambah Indikator di Tujuan ini"
                    >
                      <Plus class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="openEditTujuanModal(t)"
                      class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 cursor-pointer"
                      title="Edit Tujuan"
                    >
                      <Edit3 class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="handleDeleteTujuan(t)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                      title="Hapus Tujuan"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>

              <!-- CHILD ROWS: INDIKATOR TUJUAN (Tampil saat expanded) -->
              <template v-if="expandedTujuanMap[t.idtujuan]">
                <tr v-if="!t.indikator_list || t.indikator_list.length === 0">
                  <td colspan="12" class="py-4 pl-12 pr-4 text-slate-400 italic bg-white dark:bg-[#141d30]">
                    <div class="flex items-center space-x-2 text-xs">
                      <CornerDownRight class="w-4 h-4 text-slate-400" />
                      <span>Belum ada indikator tujuan terdaftar. Klik tombol <strong>+</strong> pada baris di atas untuk menambahkan indikator.</span>
                    </div>
                  </td>
                </tr>

                <tr 
                  v-for="ind in t.indikator_list" 
                  :key="ind.idtujuan_indikator"
                  class="bg-white dark:bg-[#141d30] hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <!-- Indikator Kode with Tree Branch Icon -->
                  <td class="py-2.5 px-3 pl-6 border-r border-slate-100 dark:border-slate-800/60">
                    <div class="flex items-center space-x-1.5 font-mono text-xs">
                      <CornerDownRight class="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span class="font-bold text-[#308e87] dark:text-[#3aada4]">
                        #{{ ind.urut }}
                      </span>
                    </div>
                  </td>

                  <!-- Misi blank cell for Child Row -->
                  <td class="py-2.5 px-3 text-center border-r border-slate-100 dark:border-slate-800/60 bg-slate-50/30 dark:bg-slate-900/20 text-slate-300 dark:text-slate-600">
                    -
                  </td>

                  <!-- Uraian Indikator Tujuan -->
                  <td class="py-2.5 px-4 text-slate-800 dark:text-slate-200 font-semibold leading-relaxed border-r border-slate-100 dark:border-slate-800/60">
                    <div class="space-y-1">
                      <div class="flex flex-wrap items-center gap-1.5">
                        <span class="text-xs font-bold">{{ ind.uraitujuan_indikator }}</span>
                        <span v-if="ind.iku" class="px-1.5 py-0.2 rounded text-[9px] font-black bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                          IKU
                        </span>
                        <span v-if="ind.ikd" class="px-1.5 py-0.2 rounded text-[9px] font-black bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
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
                        @click="openEditIndikatorTujuanModal(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer"
                        title="Edit Indikator Tujuan"
                      >
                        <Edit3 class="w-3.5 h-3.5" />
                      </button>
                      <button 
                        @click="handleDeleteIndikatorTujuan(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 cursor-pointer"
                        title="Hapus Indikator Tujuan"
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

    <!-- ==================== MODAL: TAMBAH / EDIT TUJUAN ==================== -->
    <div 
      v-if="showTujuanModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showTujuanModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Target class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditTujuan ? 'Edit Tujuan RPJMD' : 'Tambah Tujuan RPJMD' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjmd_tujuan</code></p>
            </div>
          </div>
          <button @click="showTujuanModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveTujuanData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Misi RPJMD Terkait</label>
              <select 
                v-model="tujuanForm.idmisi" 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              >
                <option value="">-- Pilih Misi --</option>
                <option v-for="m in misiList" :key="m.idmisi" :value="m.idmisi">
                  [Misi {{ m.urut }}] {{ m.uraimisi.substring(0, 40) }}...
                </option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut Tujuan</label>
              <input 
                v-model.number="tujuanForm.urut" 
                type="number" 
                min="1"
                required
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Tujuan Pembangunan RPJMD</label>
            <textarea 
              v-model="tujuanForm.uraitujuan" 
              rows="3" 
              required
              placeholder="Masukkan uraian tujuan pembangunan RPJMD..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-semibold leading-relaxed"
            ></textarea>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showTujuanModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingTujuan"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingTujuan" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditTujuan ? 'Simpan Perubahan' : 'Tambah Tujuan' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== MODAL: TAMBAH / EDIT INDIKATOR TUJUAN ==================== -->
    <div 
      v-if="showIndikatorTujuanModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showIndikatorTujuanModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-2xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Sparkles class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditIndikatorTujuan ? 'Edit Indikator Tujuan' : 'Tambah Indikator Tujuan' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjmd_indikator_tujuan</code></p>
            </div>
          </div>
          <button @click="showIndikatorTujuanModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveIndikatorTujuanData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Tujuan Induk</label>
              <select 
                v-model="indikatorTujuanForm.idtujuan" 
                required
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              >
                <option v-for="t in tujuanList" :key="t.idtujuan" :value="t.idtujuan">
                  [T-{{ t.urut }}] {{ t.uraitujuan.substring(0, 45) }}...
                </option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut Indikator</label>
              <input 
                v-model.number="indikatorTujuanForm.urut" 
                type="number" 
                min="1"
                required
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Indikator Kinerja Tujuan</label>
            <input 
              v-model="indikatorTujuanForm.uraitujuan_indikator" 
              type="text" 
              required
              placeholder="Contoh: Indeks Pembangunan Manusia, Tingkat Kemiskinan..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
            />
          </div>

          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Satuan</label>
              <input 
                v-model="indikatorTujuanForm.satuan" 
                type="text" 
                placeholder="Angka, %, Tahun" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Status Polaritas</label>
              <select 
                v-model="indikatorTujuanForm.status" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              >
                <option value="positif">Positif (Makin tinggi makin baik)</option>
                <option value="negatif">Negatif (Makin rendah makin baik)</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Baseline / 2024</label>
              <input 
                v-model="indikatorTujuanForm.baseline" 
                type="text" 
                placeholder="Contoh: 77.43" 
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
                  v-model="indikatorTujuanForm.target0" 
                  type="text" 
                  placeholder="84.85" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-cyan-600 dark:text-cyan-400 mb-1">2026 (target1)</label>
                <input 
                  v-model="indikatorTujuanForm.target1" 
                  type="text" 
                  placeholder="86.14" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-teal-600 dark:text-teal-400 mb-1">2027 (target2)</label>
                <input 
                  v-model="indikatorTujuanForm.target2" 
                  type="text" 
                  placeholder="87.43" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-indigo-600 dark:text-indigo-400 mb-1">2028 (target3)</label>
                <input 
                  v-model="indikatorTujuanForm.target3" 
                  type="text" 
                  placeholder="88.72" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-amber-600 dark:text-amber-400 mb-1">2029 (target4)</label>
                <input 
                  v-model="indikatorTujuanForm.target4" 
                  type="text" 
                  placeholder="90.01" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold text-xs"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mb-1">2030 (target5)</label>
                <input 
                  v-model="indikatorTujuanForm.target5" 
                  type="text" 
                  placeholder="91.30" 
                  class="w-full px-2 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-black text-xs"
                />
              </div>
            </div>
          </div>

          <!-- Tagging IKU / IKD -->
          <div class="flex items-center space-x-6 p-2 rounded-xl bg-slate-50 dark:bg-slate-800/40">
            <label class="flex items-center space-x-2 cursor-pointer">
              <input type="checkbox" v-model="indikatorTujuanForm.iku" class="rounded text-[#308e87] focus:ring-[#308e87] w-4 h-4" />
              <span class="font-bold text-slate-700 dark:text-slate-200">Indikator Kinerja Utama (IKU)</span>
            </label>
            <label class="flex items-center space-x-2 cursor-pointer">
              <input type="checkbox" v-model="indikatorTujuanForm.ikd" class="rounded text-[#308e87] focus:ring-[#308e87] w-4 h-4" />
              <span class="font-bold text-slate-700 dark:text-slate-200">Indikator Kinerja Daerah (IKD)</span>
            </label>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showIndikatorTujuanModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingIndikatorTujuan"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingIndikatorTujuan" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditIndikatorTujuan ? 'Simpan Perubahan' : 'Tambah Indikator' }}</span>
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
import { Target, Search, Plus, RotateCw, Loader2, Edit3, Trash2, ChevronDown, ChevronRight, CornerDownRight, Sparkles } from 'lucide-vue-next'

const searchQueryTujuan = ref('')
const expandedTujuanMap = ref({})
const loadingTujuan = ref(false)
const savingTujuan = ref(false)
const savingIndikatorTujuan = ref(false)

const tujuanList = ref([])
const misiList = ref([])

const showTujuanModal = ref(false)
const isEditTujuan = ref(false)
const currentTujuanId = ref(null)
const tujuanForm = ref({
  uraitujuan: '',
  urut: 1,
  idmisi: ''
})

const showIndikatorTujuanModal = ref(false)
const isEditIndikatorTujuan = ref(false)
const currentIndikatorTujuanId = ref(null)
const indikatorTujuanForm = ref({
  idtujuan: '',
  uraitujuan_indikator: '',
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
  iku: true,
  ikd: false,
  uraiaspek: '',
  urut: 1
})

const totalIndikatorTujuanCount = computed(() => {
  return tujuanList.value.reduce((acc, t) => acc + (t.indikator_list ? t.indikator_list.length : 0), 0)
})

const filteredTujuanList = computed(() => {
  if (!searchQueryTujuan.value) return tujuanList.value
  const q = searchQueryTujuan.value.toLowerCase()
  return tujuanList.value.filter(t => {
    const matchTujuan = (t.uraitujuan && t.uraitujuan.toLowerCase().includes(q)) || 
                        (t.uraimisi && t.uraimisi.toLowerCase().includes(q)) ||
                        (t.urut && t.urut.toString().includes(q)) ||
                        (t.urut_misi && t.urut_misi.toString().includes(q))
    const matchIndikator = t.indikator_list && t.indikator_list.some(ind => 
      (ind.uraitujuan_indikator && ind.uraitujuan_indikator.toLowerCase().includes(q)) ||
      (ind.satuan && ind.satuan.toLowerCase().includes(q)) ||
      (ind.uraiaspek && ind.uraiaspek.toLowerCase().includes(q))
    )
    if (matchTujuan || matchIndikator) {
      expandedTujuanMap.value[t.idtujuan] = true
      return true
    }
    return false
  })
})

function toggleTujuanExpand(idtujuan) {
  expandedTujuanMap.value[idtujuan] = !expandedTujuanMap.value[idtujuan]
}

function expandAllTujuan() {
  tujuanList.value.forEach(t => {
    expandedTujuanMap.value[t.idtujuan] = true
  })
}

function collapseAllTujuan() {
  tujuanList.value.forEach(t => {
    expandedTujuanMap.value[t.idtujuan] = false
  })
}

async function fetchTujuanData() {
  loadingTujuan.value = true
  try {
    const [resTujuan, resMisi] = await Promise.all([
      axios.get('/api/v1/rpjmd/tujuan-lengkap'),
      axios.get('/api/v1/rpjmd/misi')
    ])

    if (resTujuan.data && resTujuan.data.daftar_tujuan) {
      tujuanList.value = resTujuan.data.daftar_tujuan
      resTujuan.data.daftar_tujuan.forEach(t => {
        if (expandedTujuanMap.value[t.idtujuan] === undefined) {
          expandedTujuanMap.value[t.idtujuan] = true
        }
      })
    }

    if (Array.isArray(resMisi.data)) {
      misiList.value = resMisi.data
    }
  } catch (err) {
    console.error('Error fetching RPJMD Tujuan data:', err)
  } finally {
    loadingTujuan.value = false
  }
}

function openAddTujuanModal() {
  isEditTujuan.value = false
  currentTujuanId.value = null
  tujuanForm.value = {
    uraitujuan: '',
    urut: tujuanList.value.length + 1,
    idmisi: misiList.value[0]?.idmisi || ''
  }
  showTujuanModal.value = true
}

function openEditTujuanModal(t) {
  isEditTujuan.value = true
  currentTujuanId.value = t.idtujuan
  tujuanForm.value = {
    uraitujuan: t.uraitujuan,
    urut: t.urut || 1,
    idmisi: t.idmisi || ''
  }
  showTujuanModal.value = true
}

async function saveTujuanData() {
  savingTujuan.value = true
  try {
    const payload = {
      uraitujuan: tujuanForm.value.uraitujuan,
      urut: tujuanForm.value.urut,
      idmisi: tujuanForm.value.idmisi || null
    }

    if (isEditTujuan.value) {
      await axios.put(`/api/v1/rpjmd/tujuan/${currentTujuanId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjmd/tujuan', payload)
    }
    showTujuanModal.value = false
    await fetchTujuanData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditTujuan.value ? 'Tujuan RPJMD berhasil diperbarui' : 'Tujuan RPJMD baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Tujuan RPJMD', 'error')
  } finally {
    savingTujuan.value = false
  }
}

async function handleDeleteTujuan(t) {
  const result = await Swal.fire({
    title: 'Hapus Tujuan RPJMD?',
    html: `Apakah Anda yakin ingin menghapus Tujuan [<strong>T-${t.urut}</strong>]: <br/>"${t.uraitujuan.substring(0, 80)}..."?<br/><br/><span class="text-xs text-red-500">Perhatian: Indikator terkait juga akan terhapus.</span>`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjmd/tujuan/${t.idtujuan}`)
      await fetchTujuanData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Tujuan RPJMD berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Tujuan RPJMD', 'error')
    }
  }
}

function openAddIndikatorTujuanModal(idtujuan) {
  isEditIndikatorTujuan.value = false
  currentIndikatorTujuanId.value = null
  const parentT = tujuanList.value.find(t => t.idtujuan === idtujuan)
  const indCount = parentT?.indikator_list?.length || 0
  
  indikatorTujuanForm.value = {
    idtujuan: idtujuan || tujuanList.value[0]?.idtujuan || '',
    uraitujuan_indikator: '',
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
    iku: true,
    ikd: false,
    uraiaspek: '',
    urut: indCount + 1
  }
  showIndikatorTujuanModal.value = true
}

function openEditIndikatorTujuanModal(ind) {
  isEditIndikatorTujuan.value = true
  currentIndikatorTujuanId.value = ind.idtujuan_indikator
  indikatorTujuanForm.value = {
    idtujuan: ind.idtujuan,
    uraitujuan_indikator: ind.uraitujuan_indikator,
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
    iku: ind.iku || false,
    ikd: ind.ikd || false,
    uraiaspek: ind.uraiaspek || '',
    urut: ind.urut || 1
  }
  showIndikatorTujuanModal.value = true
}

async function saveIndikatorTujuanData() {
  savingIndikatorTujuan.value = true
  try {
    const payload = {
      idtujuan: indikatorTujuanForm.value.idtujuan,
      uraitujuan_indikator: indikatorTujuanForm.value.uraitujuan_indikator,
      satuan: indikatorTujuanForm.value.satuan,
      status: indikatorTujuanForm.value.status,
      baseline: indikatorTujuanForm.value.baseline,
      target0: indikatorTujuanForm.value.target0 || indikatorTujuanForm.value.baseline,
      target1: indikatorTujuanForm.value.target1,
      target2: indikatorTujuanForm.value.target2,
      target3: indikatorTujuanForm.value.target3,
      target4: indikatorTujuanForm.value.target4,
      target5: indikatorTujuanForm.value.target5,
      tipe_data: indikatorTujuanForm.value.tipe_data,
      kodeindikator_master: indikatorTujuanForm.value.kodeindikator_master,
      sumber: indikatorTujuanForm.value.sumber,
      iku: indikatorTujuanForm.value.iku,
      ikd: indikatorTujuanForm.value.ikd,
      uraiaspek: indikatorTujuanForm.value.uraiaspek,
      urut: indikatorTujuanForm.value.urut
    }

    if (isEditIndikatorTujuan.value) {
      await axios.put(`/api/v1/rpjmd/indikator-tujuan/${currentIndikatorTujuanId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjmd/indikator-tujuan', payload)
    }
    showIndikatorTujuanModal.value = false
    await fetchTujuanData()
    expandedTujuanMap.value[indikatorTujuanForm.value.idtujuan] = true
    
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditIndikatorTujuan.value ? 'Indikator Tujuan berhasil diperbarui' : 'Indikator Tujuan baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Indikator Tujuan RPJMD', 'error')
  } finally {
    savingIndikatorTujuan.value = false
  }
}

async function handleDeleteIndikatorTujuan(ind) {
  const result = await Swal.fire({
    title: 'Hapus Indikator Tujuan?',
    html: `Apakah Anda yakin ingin menghapus Indikator [<strong>#${ind.urut}</strong>]: <br/>"${ind.uraitujuan_indikator.substring(0, 80)}..."?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjmd/indikator-tujuan/${ind.idtujuan_indikator}`)
      await fetchTujuanData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Indikator Tujuan berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Indikator Tujuan', 'error')
    }
  }
}

onMounted(() => {
  fetchTujuanData()
})

defineExpose({
  fetchTujuanData,
  tujuanList,
  totalIndikatorTujuanCount
})
</script>
