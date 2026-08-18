<template>
  <div class="space-y-4">
    
    <!-- Toolbar & Actions -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <!-- Search input -->
        <div class="relative w-full md:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQuerySasaranPokok"
            type="text" 
            placeholder="Cari sasaran pokok atau indikator..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#f39159]"
          />
        </div>

        <!-- Expand / Collapse All Buttons -->
        <div class="flex items-center space-x-1.5 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shrink-0">
          <button 
            @click="expandAllSasaranPokok"
            class="px-2.5 py-1 text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#f39159] rounded-lg transition-colors cursor-pointer"
            title="Buka Semua Tree Sasaran Pokok"
          >
            Buka Semua
          </button>
          <span class="text-slate-300 dark:text-slate-600">|</span>
          <button 
            @click="collapseAllSasaranPokok"
            class="px-2.5 py-1 text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#f39159] rounded-lg transition-colors cursor-pointer"
            title="Tutup Semua Tree Sasaran Pokok"
          >
            Tutup Semua
          </button>
        </div>

        <button 
          @click="fetchSasaranPokokData"
          class="p-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer shrink-0"
          title="Segarkan Data Sasaran Pokok"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loadingSasaranPokok }" />
        </button>
      </div>

      <div class="flex items-center space-x-3 self-end md:self-center">
        <span class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <strong>{{ sasaranPokokList.length }}</strong> Sasaran Pokok • <strong>{{ totalIndikatorPokokCount }}</strong> Indikator
        </span>
        <button 
          @click="openAddSasaranPokokModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#f39159] hover:bg-[#e27b41] text-white flex items-center space-x-1.5 shadow-sm shadow-[#f39159]/30 cursor-pointer"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Sasaran Pokok</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingSasaranPokok" class="py-16 flex flex-col items-center justify-center space-y-3 text-slate-400">
      <Loader2 class="w-8 h-8 animate-spin text-[#f39159]" />
      <span class="text-xs font-bold">Memuat Tree Tabel Sasaran Pokok...</span>
    </div>

    <!-- ==================== UNIFIED TREE TABLE: SASARAN POKOK ==================== -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-100/90 dark:bg-slate-800/90 text-[10px] font-black uppercase tracking-wider text-slate-600 dark:text-slate-300 select-none">
              <th rowspan="2" class="py-3 px-3 w-24 text-center border-r border-slate-200 dark:border-slate-700/80">Kode</th>
              <th rowspan="2" class="py-3 px-3 w-24 text-center border-r border-slate-200 dark:border-slate-700/80">Misi</th>
              <th rowspan="2" class="py-3 px-4 min-w-[260px] border-r border-slate-200 dark:border-slate-700/80">Sasaran Pokok / Indikator Kinerja</th>
              <th rowspan="2" class="py-3 px-3 w-20 text-center border-r border-slate-200 dark:border-slate-700/80">Satuan</th>
              <th rowspan="2" class="py-3 px-3 w-24 text-center border-r border-slate-200 dark:border-slate-700/80">Kondisi Awal</th>
              <th rowspan="2" class="py-3 px-3 w-24 text-center border-r border-slate-200 dark:border-slate-700/80 bg-amber-50/50 dark:bg-amber-950/20 text-amber-800 dark:text-amber-300">Baseline</th>
              <th colspan="4" class="py-2 px-2 text-center border-b border-r border-slate-200 dark:border-slate-700/80 bg-amber-500/10 text-amber-700 dark:text-amber-300 font-black">
                Periode Pelaksanaan RPJMD
              </th>
              <th rowspan="2" class="py-3 px-4 w-24 text-center">Aksi</th>
            </tr>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-amber-50/5 dark:bg-amber-950/20 text-[10px] font-bold text-slate-600 dark:text-slate-300">
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-blue-700 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20">
                1<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2025–2029)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-teal-700 dark:text-teal-400 bg-teal-50/40 dark:bg-teal-950/20">
                2<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2030–2034)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-amber-700 dark:text-amber-400 bg-amber-50/40 dark:bg-amber-950/20">
                3<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2035–2039)</span>
              </th>
              <th class="py-1.5 px-2 w-20 text-center border-r border-slate-200 dark:border-slate-700/80 text-emerald-700 dark:text-emerald-400 bg-emerald-50/40 dark:bg-emerald-950/20">
                4<br/><span class="text-[8px] font-normal font-sans text-slate-500 dark:text-slate-400">(2040–2045)</span>
              </th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
            <template v-for="sp in filteredSasaranPokokList" :key="sp.id || sp.idsasaran">
              <!-- PARENT ROW: SASARAN POKOK -->
              <tr 
                @click="toggleSasaranPokokExpand(sp.idsasaran)"
                class="bg-slate-50/90 dark:bg-slate-800/70 hover:bg-slate-100/90 dark:hover:bg-slate-800 font-bold transition-colors cursor-pointer border-t-2 border-slate-200 dark:border-slate-700 select-none"
              >
                <!-- Kode & Expand Toggle -->
                <td class="py-3 px-3 border-r border-slate-200/60 dark:border-slate-800/60">
                  <div class="flex items-center space-x-1.5">
                    <button 
                      @click.stop="toggleSasaranPokokExpand(sp.idsasaran)" 
                      class="p-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 transition-transform"
                    >
                      <ChevronDown v-if="expandedSasaranPokokMap[sp.idsasaran]" class="w-4 h-4 text-[#f39159]" />
                      <ChevronRight v-else class="w-4 h-4 text-slate-400" />
                    </button>
                    <span class="px-2 py-0.5 rounded-lg text-xs font-black bg-[#f39159] text-white shadow-sm shadow-[#f39159]/20">
                      {{ sp.idsasaran }}
                    </span>
                  </div>
                </td>

                <!-- Kolom Misi -->
                <td class="py-3 px-3 text-center border-r border-slate-200/60 dark:border-slate-800/60">
                  <span class="px-2 py-0.5 rounded-md text-[10px] font-black bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border border-indigo-500/20">
                    Misi {{ sp.idmisi || '1' }}
                  </span>
                </td>

                <!-- Uraian Sasaran Pokok -->
                <td class="py-3 px-4 text-slate-900 dark:text-white font-extrabold text-xs leading-snug border-r border-slate-200/60 dark:border-slate-800/60">
                  <div class="flex items-center space-x-2">
                    <span>{{ sp.uraisasaran }}</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#f39159]/10 text-[#f39159] border border-[#f39159]/20 shrink-0">
                      {{ sp.indikator_list ? sp.indikator_list.length : 0 }} Indikator
                    </span>
                  </div>
                </td>

                <!-- Blank Columns for Parent -->
                <td class="py-3 px-3 text-center text-slate-400 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-3 text-center text-slate-400 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-3 text-center text-slate-400 border-r border-slate-200/60 dark:border-slate-800/60 bg-amber-50/10">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-blue-50/20 dark:bg-blue-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-teal-50/20 dark:bg-teal-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-amber-50/20 dark:bg-amber-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>
                <td class="py-3 px-2 text-center text-slate-400 bg-emerald-50/20 dark:bg-emerald-950/10 border-r border-slate-200/60 dark:border-slate-800/60">-</td>

                <!-- Parent Actions -->
                <td class="py-3 px-4 text-center" @click.stop>
                  <div class="flex items-center justify-center space-x-1">
                    <button 
                      @click="openAddIndikatorPokokModal(sp.idsasaran)"
                      class="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 cursor-pointer"
                      title="Tambah Indikator di Sasaran Pokok ini"
                    >
                      <Plus class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="openEditSasaranPokokModal(sp)"
                      class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 cursor-pointer"
                      title="Edit Sasaran Pokok"
                    >
                      <Edit3 class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="handleDeleteSasaranPokok(sp)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                      title="Hapus Sasaran Pokok"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>

              <!-- CHILD ROWS: INDIKATOR SASARAN POKOK (Tampil saat expanded) -->
              <template v-if="expandedSasaranPokokMap[sp.idsasaran]">
                <tr v-if="!sp.indikator_list || sp.indikator_list.length === 0">
                  <td colspan="11" class="py-4 pl-12 pr-4 text-slate-400 italic bg-white dark:bg-[#141d30]">
                    <div class="flex items-center space-x-2 text-xs">
                      <CornerDownRight class="w-4 h-4 text-slate-400" />
                      <span>Belum ada indikator sasaran pokok terdaftar. Klik tombol <strong>+</strong> pada baris di atas untuk menambahkan indikator.</span>
                    </div>
                  </td>
                </tr>

                <tr 
                  v-for="ind in sp.indikator_list" 
                  :key="ind.id || ind.idsasaran_indikator"
                  class="bg-white dark:bg-[#141d30] hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <!-- Indikator Kode with Tree Branch Icon -->
                  <td class="py-2.5 px-3 pl-6 border-r border-slate-100 dark:border-slate-800/60">
                    <div class="flex items-center space-x-1.5 font-mono text-xs">
                      <CornerDownRight class="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span class="font-bold text-[#f39159] dark:text-[#f8b088]">
                        #{{ ind.idsasaran_indikator }}
                      </span>
                    </div>
                  </td>

                  <!-- Kolom Misi Child -->
                  <td class="py-2.5 px-3 text-center border-r border-slate-100 dark:border-slate-800/60">
                    <span class="text-[10px] font-mono text-slate-400 dark:text-slate-500">
                      Misi {{ ind.idmisi || sp.idmisi || '1' }}
                    </span>
                  </td>

                  <!-- Uraian Indikator Sasaran Pokok -->
                  <td class="py-2.5 px-4 text-slate-800 dark:text-slate-200 font-semibold leading-relaxed border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.uraisasaran_indikator }}
                  </td>

                  <!-- Satuan -->
                  <td class="py-2.5 px-3 text-center text-slate-500 font-medium border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.satuan || '-' }}
                  </td>

                  <!-- Kondisi Awal -->
                  <td class="py-2.5 px-3 text-center font-semibold text-slate-700 dark:text-slate-300 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.kondisi_awal || '-' }}
                  </td>

                  <!-- Baseline -->
                  <td class="py-2.5 px-3 text-center font-bold text-amber-700 dark:text-amber-400 bg-amber-50/30 dark:bg-amber-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.baseline || '-' }}
                  </td>

                  <!-- Target 1 (2025–2029) -->
                  <td class="py-2.5 px-2 text-center font-bold text-blue-600 dark:text-blue-400 bg-blue-50/20 dark:bg-blue-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target_1 || '-' }}
                  </td>

                  <!-- Target 2 (2030–2034) -->
                  <td class="py-2.5 px-2 text-center font-bold text-teal-600 dark:text-teal-400 bg-teal-50/20 dark:bg-teal-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target_2 || '-' }}
                  </td>

                  <!-- Target 3 (2035–2039) -->
                  <td class="py-2.5 px-2 text-center font-bold text-amber-600 dark:text-amber-400 bg-amber-50/20 dark:bg-amber-950/10 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target_3 || '-' }}
                  </td>

                  <!-- Target 4 (2040–2045) -->
                  <td class="py-2.5 px-2 text-center font-black text-emerald-600 dark:text-emerald-400 bg-emerald-50/30 dark:bg-emerald-950/20 border-r border-slate-100 dark:border-slate-800/60">
                    {{ ind.target_4 || '-' }}
                  </td>

                  <!-- Child Actions -->
                  <td class="py-2.5 px-4 text-center">
                    <div class="flex items-center justify-center space-x-1">
                      <button 
                        @click="openEditIndikatorPokokModal(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer"
                        title="Edit Indikator Sasaran Pokok"
                      >
                        <Edit3 class="w-3.5 h-3.5" />
                      </button>
                      <button 
                        @click="handleDeleteIndikatorPokok(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 cursor-pointer"
                        title="Hapus Indikator Sasaran Pokok"
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

    <!-- ==================== MODAL: TAMBAH / EDIT SASARAN POKOK ==================== -->
    <div 
      v-if="showSasaranPokokModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showSasaranPokokModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#f39159]/10 text-[#f39159] flex items-center justify-center">
              <CheckCircle2 class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditSasaranPokok ? 'Edit Sasaran Pokok RPJPD' : 'Tambah Sasaran Pokok RPJPD' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_sasaran_pokok</code></p>
            </div>
          </div>
          <button @click="showSasaranPokokModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveSasaranPokokData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kode / ID Sasaran Pokok</label>
              <input 
                v-model="sasaranPokokForm.idsasaran" 
                type="text" 
                required
                placeholder="Contoh: 1.1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-bold"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut</label>
              <input 
                v-model.number="sasaranPokokForm.urut" 
                type="number" 
                min="1"
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Misi Terkait</label>
            <select 
              v-model="sasaranPokokForm.idmisi" 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-bold"
            >
              <option v-for="m in misiList" :key="m.idmisi" :value="m.idmisi">
                Misi {{ m.idmisi }}: {{ m.uraimisi.substring(0, 45) }}...
              </option>
            </select>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Sasaran Pokok</label>
            <textarea 
              v-model="sasaranPokokForm.uraisasaran" 
              rows="3" 
              required
              placeholder="Masukkan uraian sasaran pokok RPJPD secara lengkap..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none leading-relaxed"
            ></textarea>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showSasaranPokokModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingSasaranPokok"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#f39159] hover:bg-[#e27b41] text-white shadow-md shadow-[#f39159]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingSasaranPokok" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditSasaranPokok ? 'Simpan Perubahan' : 'Tambah Sasaran Pokok' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== MODAL: TAMBAH / EDIT INDIKATOR SASARAN POKOK ==================== -->
    <div 
      v-if="showIndikatorPokokModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showIndikatorPokokModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-2xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#f39159]/10 text-[#f39159] flex items-center justify-center">
              <Sparkles class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditIndikatorPokok ? 'Edit Indikator Sasaran Pokok' : 'Tambah Indikator Sasaran Pokok' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_indikator_sasaran_pokok</code></p>
            </div>
          </div>
          <button @click="showIndikatorPokokModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveIndikatorPokokData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Sasaran Pokok Induk</label>
              <select 
                v-model="indikatorPokokForm.idsasaran" 
                required
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-bold"
              >
                <option v-for="sp in sasaranPokokList" :key="sp.idsasaran" :value="sp.idsasaran">
                  [{{ sp.idsasaran }}] {{ sp.uraisasaran.substring(0, 45) }}...
                </option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor / ID Indikator</label>
              <input 
                v-model="indikatorPokokForm.idsasaran_indikator" 
                type="text" 
                required
                placeholder="Contoh: 1, 2, 20..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-mono"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Indikator Kinerja</label>
            <input 
              v-model="indikatorPokokForm.uraisasaran_indikator" 
              type="text" 
              required
              placeholder="Contoh: Usia Harapan Hidup (UHH)" 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-bold"
            />
          </div>

          <div class="grid grid-cols-3 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Satuan</label>
              <input 
                v-model="indikatorPokokForm.satuan" 
                type="text" 
                placeholder="Contoh: %, Tahun, Angka" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kondisi Awal</label>
              <input 
                v-model="indikatorPokokForm.kondisi_awal" 
                type="text" 
                placeholder="Contoh: 74.8" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Baseline</label>
              <input 
                v-model="indikatorPokokForm.baseline" 
                type="text" 
                placeholder="Contoh: 74.8" 
                class="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#f39159] focus:outline-none font-bold"
              />
            </div>
          </div>

          <!-- 4 Target Tahapan RPJMD 2025–2045 -->
          <div class="p-3.5 bg-slate-50 dark:bg-slate-800/50 rounded-2xl border border-slate-200/80 dark:border-slate-700/80 space-y-2">
            <span class="block text-[10px] font-black uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Target 4 Tahapan Periode RPJMD 2025–2045
            </span>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              <div>
                <label class="block text-[10px] font-bold text-blue-600 dark:text-blue-400 mb-1">Tahap 1 (2025–2029)</label>
                <input 
                  v-model="indikatorPokokForm.target_1" 
                  type="text" 
                  placeholder="76.32" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-teal-600 dark:text-teal-400 mb-1">Tahap 2 (2030–2034)</label>
                <input 
                  v-model="indikatorPokokForm.target_2" 
                  type="text" 
                  placeholder="77.92" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-amber-600 dark:text-amber-400 mb-1">Tahap 3 (2035–2039)</label>
                <input 
                  v-model="indikatorPokokForm.target_3" 
                  type="text" 
                  placeholder="79.52" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mb-1">Tahap 4 (2040–2045)</label>
                <input 
                  v-model="indikatorPokokForm.target_4" 
                  type="text" 
                  placeholder="81.08" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-black"
                />
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showIndikatorPokokModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingIndikatorPokok"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#f39159] hover:bg-[#e27b41] text-white shadow-md shadow-[#f39159]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingIndikatorPokok" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditIndikatorPokok ? 'Simpan Perubahan' : 'Tambah Indikator' }}</span>
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
import { CheckCircle2, Search, Plus, RotateCw, Loader2, Edit3, Trash2, ChevronDown, ChevronRight, CornerDownRight, Sparkles } from 'lucide-vue-next'

const searchQuerySasaranPokok = ref('')
const expandedSasaranPokokMap = ref({})
const loadingSasaranPokok = ref(false)
const savingSasaranPokok = ref(false)
const savingIndikatorPokok = ref(false)

const sasaranPokokList = ref([])
const misiList = ref([])

const showSasaranPokokModal = ref(false)
const isEditSasaranPokok = ref(false)
const currentSasaranPokokId = ref(null)
const sasaranPokokForm = ref({
  idsasaran: '',
  uraisasaran: '',
  idmisi: '1',
  uraimisi: '',
  urut: 1,
  no: 1
})

const showIndikatorPokokModal = ref(false)
const isEditIndikatorPokok = ref(false)
const currentIndikatorPokokId = ref(null)
const indikatorPokokForm = ref({
  idsasaran: '',
  idsasaran_indikator: '',
  uraisasaran_indikator: '',
  satuan: '%',
  kondisi_awal: '',
  baseline: '',
  target_1: '',
  target_2: '',
  target_3: '',
  target_4: '',
  kodeindikator_master: '',
  urut: 1
})

const totalIndikatorPokokCount = computed(() => {
  return sasaranPokokList.value.reduce((acc, sp) => acc + (sp.indikator_list ? sp.indikator_list.length : 0), 0)
})

const filteredSasaranPokokList = computed(() => {
  if (!searchQuerySasaranPokok.value) return sasaranPokokList.value
  const q = searchQuerySasaranPokok.value.toLowerCase()
  return sasaranPokokList.value.filter(sp => {
    const matchSasaran = (sp.uraisasaran && sp.uraisasaran.toLowerCase().includes(q)) || 
                         (sp.idsasaran && sp.idsasaran.toLowerCase().includes(q))
    const matchIndikator = sp.indikator_list && sp.indikator_list.some(ind => 
      (ind.uraisasaran_indikator && ind.uraisasaran_indikator.toLowerCase().includes(q)) ||
      (ind.idsasaran_indikator && ind.idsasaran_indikator.toLowerCase().includes(q)) ||
      (ind.satuan && ind.satuan.toLowerCase().includes(q))
    )
    if (matchSasaran || matchIndikator) {
      expandedSasaranPokokMap.value[sp.idsasaran] = true
      return true
    }
    return false
  })
})

function toggleSasaranPokokExpand(idsasaran) {
  expandedSasaranPokokMap.value[idsasaran] = !expandedSasaranPokokMap.value[idsasaran]
}

function expandAllSasaranPokok() {
  sasaranPokokList.value.forEach(sp => {
    expandedSasaranPokokMap.value[sp.idsasaran] = true
  })
}

function collapseAllSasaranPokok() {
  sasaranPokokList.value.forEach(sp => {
    expandedSasaranPokokMap.value[sp.idsasaran] = false
  })
}

async function fetchSasaranPokokData() {
  loadingSasaranPokok.value = true
  try {
    const res = await axios.get('/api/v1/rpjpd/sasaran-pokok-lengkap')
    if (res.data && res.data.daftar_sasaran_pokok) {
      sasaranPokokList.value = res.data.daftar_sasaran_pokok
      res.data.daftar_sasaran_pokok.forEach(sp => {
        if (expandedSasaranPokokMap.value[sp.idsasaran] === undefined) {
          expandedSasaranPokokMap.value[sp.idsasaran] = true
        }
      })
    }
  } catch (err) {
    console.error('Error fetching RPJPD Sasaran Pokok data:', err)
  } finally {
    loadingSasaranPokok.value = false
  }
}

async function fetchMisiList() {
  try {
    const res = await axios.get('/api/v1/rpjpd/misi')
    if (Array.isArray(res.data)) {
      misiList.value = res.data
    }
  } catch (err) {
    console.error('Error fetching Misi list for Sasaran Pokok:', err)
  }
}

function openAddSasaranPokokModal() {
  isEditSasaranPokok.value = false
  currentSasaranPokokId.value = null
  sasaranPokokForm.value = {
    idsasaran: (sasaranPokokList.value.length + 1).toString(),
    uraisasaran: '',
    idmisi: misiList.value[0]?.idmisi || '1',
    uraimisi: '',
    urut: sasaranPokokList.value.length + 1,
    no: sasaranPokokList.value.length + 1
  }
  showSasaranPokokModal.value = true
}

function openEditSasaranPokokModal(sp) {
  isEditSasaranPokok.value = true
  currentSasaranPokokId.value = sp.id
  sasaranPokokForm.value = {
    idsasaran: sp.idsasaran,
    uraisasaran: sp.uraisasaran,
    idmisi: sp.idmisi || '1',
    uraimisi: sp.uraimisi || '',
    urut: sp.urut || sp.no || 1,
    no: sp.no || 1
  }
  showSasaranPokokModal.value = true
}

async function saveSasaranPokokData() {
  savingSasaranPokok.value = true
  try {
    const selectedMisiObj = misiList.value.find(m => m.idmisi === sasaranPokokForm.value.idmisi)
    const payload = {
      idsasaran: sasaranPokokForm.value.idsasaran,
      uraisasaran: sasaranPokokForm.value.uraisasaran,
      idmisi: sasaranPokokForm.value.idmisi,
      uraimisi: selectedMisiObj ? selectedMisiObj.uraimisi : '',
      urut: sasaranPokokForm.value.urut,
      no: sasaranPokokForm.value.no
    }

    if (isEditSasaranPokok.value) {
      await axios.put(`/api/v1/rpjpd/sasaran-pokok/${currentSasaranPokokId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/sasaran-pokok', {
        ...payload,
        idperiode: '20252045',
        kodepemda: '3376'
      })
    }
    showSasaranPokokModal.value = false
    await fetchSasaranPokokData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditSasaranPokok.value ? 'Sasaran Pokok berhasil diperbarui' : 'Sasaran Pokok baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Sasaran Pokok', 'error')
  } finally {
    savingSasaranPokok.value = false
  }
}

async function handleDeleteSasaranPokok(sp) {
  const result = await Swal.fire({
    title: 'Hapus Sasaran Pokok?',
    html: `Apakah Anda yakin ingin menghapus Sasaran Pokok [<strong>${sp.idsasaran}</strong>]: <br/>"${sp.uraisasaran.substring(0, 80)}..."?<br/><br/><span class="text-xs text-red-500">Perhatian: Pastikan tidak ada indikator yang terkait sebelum menghapus.</span>`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/sasaran-pokok/${sp.id}`)
      await fetchSasaranPokokData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Sasaran Pokok berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Sasaran Pokok', 'error')
    }
  }
}

function openAddIndikatorPokokModal(idsasaran) {
  isEditIndikatorPokok.value = false
  currentIndikatorPokokId.value = null
  const parentSp = sasaranPokokList.value.find(s => s.idsasaran === idsasaran)
  const indCount = parentSp?.indikator_list?.length || 0
  
  indikatorPokokForm.value = {
    idsasaran: idsasaran || sasaranPokokList.value[0]?.idsasaran || '1.1',
    idsasaran_indikator: (totalIndikatorPokokCount.value + 1).toString(),
    uraisasaran_indikator: '',
    satuan: '%',
    kondisi_awal: '',
    baseline: '',
    target_1: '',
    target_2: '',
    target_3: '',
    target_4: '',
    kodeindikator_master: '',
    urut: indCount + 1
  }
  showIndikatorPokokModal.value = true
}

function openEditIndikatorPokokModal(ind) {
  isEditIndikatorPokok.value = true
  currentIndikatorPokokId.value = ind.id
  indikatorPokokForm.value = {
    idsasaran: ind.idsasaran,
    idsasaran_indikator: ind.idsasaran_indikator,
    uraisasaran_indikator: ind.uraisasaran_indikator,
    satuan: ind.satuan || '%',
    kondisi_awal: ind.kondisi_awal || '',
    baseline: ind.baseline || '',
    target_1: ind.target_1 || '',
    target_2: ind.target_2 || '',
    target_3: ind.target_3 || '',
    target_4: ind.target_4 || '',
    kodeindikator_master: ind.kodeindikator_master || '',
    urut: ind.urut || 1
  }
  showIndikatorPokokModal.value = true
}

async function saveIndikatorPokokData() {
  savingIndikatorPokok.value = true
  try {
    const parentSp = sasaranPokokList.value.find(s => s.idsasaran === indikatorPokokForm.value.idsasaran)
    const payload = {
      idsasaran: indikatorPokokForm.value.idsasaran,
      idmisi: parentSp?.idmisi || '1',
      idsasaran_indikator: indikatorPokokForm.value.idsasaran_indikator,
      uraisasaran_indikator: indikatorPokokForm.value.uraisasaran_indikator,
      satuan: indikatorPokokForm.value.satuan,
      kondisi_awal: indikatorPokokForm.value.kondisi_awal,
      baseline: indikatorPokokForm.value.baseline,
      target_1: indikatorPokokForm.value.target_1,
      target_2: indikatorPokokForm.value.target_2,
      target_3: indikatorPokokForm.value.target_3,
      target_4: indikatorPokokForm.value.target_4,
      kodeindikator_master: indikatorPokokForm.value.kodeindikator_master,
      urut: indikatorPokokForm.value.urut
    }

    if (isEditIndikatorPokok.value) {
      await axios.put(`/api/v1/rpjpd/indikator-sasaran-pokok/${currentIndikatorPokokId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/indikator-sasaran-pokok', {
        ...payload,
        idperiode: '20252045',
        kodepemda: '3376'
      })
    }
    showIndikatorPokokModal.value = false
    await fetchSasaranPokokData()
    expandedSasaranPokokMap.value[indikatorPokokForm.value.idsasaran] = true
    
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditIndikatorPokok.value ? 'Indikator berhasil diperbarui' : 'Indikator baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Indikator Sasaran Pokok', 'error')
  } finally {
    savingIndikatorPokok.value = false
  }
}

async function handleDeleteIndikatorPokok(ind) {
  const result = await Swal.fire({
    title: 'Hapus Indikator Sasaran Pokok?',
    html: `Apakah Anda yakin ingin menghapus Indikator [<strong>#${ind.idsasaran_indikator}</strong>]: <br/>"${ind.uraisasaran_indikator.substring(0, 80)}..."?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/indikator-sasaran-pokok/${ind.id}`)
      await fetchSasaranPokokData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Indikator Sasaran Pokok berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Indikator Sasaran Pokok', 'error')
    }
  }
}

onMounted(() => {
  fetchSasaranPokokData()
  fetchMisiList()
})

defineExpose({
  fetchSasaranPokokData,
  sasaranPokokList,
  totalIndikatorPokokCount
})
</script>
