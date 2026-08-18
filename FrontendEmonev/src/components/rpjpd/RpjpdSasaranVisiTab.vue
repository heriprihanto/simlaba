<template>
  <div class="space-y-4">
    
    <!-- Toolbar & Actions -->
    <div class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <!-- Search input -->
        <div class="relative w-full md:w-80">
          <Search class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            v-model="searchQuerySasaran"
            type="text" 
            placeholder="Cari sasaran visi atau indikator..."
            class="w-full pl-9 pr-4 py-2 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#308e87]"
          />
        </div>

        <!-- Expand / Collapse All Buttons -->
        <div class="flex items-center space-x-1.5 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shrink-0">
          <button 
            @click="expandAllSasaran"
            class="px-2.5 py-1 text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#308e87] rounded-lg transition-colors cursor-pointer"
            title="Buka Semua Tree"
          >
            Buka Semua
          </button>
          <span class="text-slate-300 dark:text-slate-600">|</span>
          <button 
            @click="collapseAllSasaran"
            class="px-2.5 py-1 text-[11px] font-bold text-slate-600 dark:text-slate-300 hover:text-[#308e87] rounded-lg transition-colors cursor-pointer"
            title="Tutup Semua Tree"
          >
            Tutup Semua
          </button>
        </div>

        <button 
          @click="fetchSasaranVisiData"
          class="p-2 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer shrink-0"
          title="Segarkan Data"
        >
          <RotateCw class="w-4 h-4" :class="{ 'animate-spin': loadingSasaran }" />
        </button>
      </div>

      <div class="flex items-center space-x-3 self-end md:self-center">
        <span class="text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <strong>{{ sasaranVisiList.length }}</strong> Sasaran • <strong>{{ totalIndikatorCount }}</strong> Indikator
        </span>
        <button 
          @click="openAddSasaranVisiModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#308e87] hover:bg-[#27756f] text-white flex items-center space-x-1.5 shadow-sm cursor-pointer"
        >
          <Plus class="w-3.5 h-3.5" />
          <span>Tambah Sasaran Visi</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loadingSasaran" class="py-16 flex flex-col items-center justify-center space-y-3 text-slate-400">
      <Loader2 class="w-8 h-8 animate-spin text-[#308e87]" />
      <span class="text-xs font-bold">Memuat Tree Tabel Sasaran Visi...</span>
    </div>

    <!-- ==================== UNIFIED TREE TABLE: SASARAN VISI ==================== -->
    <div v-else class="bg-white dark:bg-[#141d30] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="border-b border-slate-200 dark:border-slate-800 bg-slate-100/90 dark:bg-slate-800/90 text-[10px] font-black uppercase tracking-wider text-slate-600 dark:text-slate-300 select-none">
              <th class="py-3 px-4 w-28">Kode</th>
              <th class="py-3 px-4 min-w-[280px]">Sasaran Visi / Indikator Kinerja</th>
              <th class="py-3 px-4 w-40">Target RPJPN / Kewenangan</th>
              <th class="py-3 px-4 w-24 text-center">Kondisi Awal</th>
              <th class="py-3 px-4 w-20 text-center bg-blue-50/60 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300">
                Target 1<br/><span class="text-[8px] font-normal font-sans">(2025–2029)</span>
              </th>
              <th class="py-3 px-4 w-20 text-center bg-teal-50/60 dark:bg-teal-950/30 text-teal-700 dark:text-teal-300">
                Target 2<br/><span class="text-[8px] font-normal font-sans">(2030–2034)</span>
              </th>
              <th class="py-3 px-4 w-20 text-center bg-amber-50/60 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300">
                Target 3<br/><span class="text-[8px] font-normal font-sans">(2035–2039)</span>
              </th>
              <th class="py-3 px-4 w-20 text-center bg-emerald-50/60 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300">
                Target 4<br/><span class="text-[8px] font-normal font-sans">(2040–2045)</span>
              </th>
              <th class="py-3 px-4 w-24 text-center">Aksi</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
            <template v-for="sv in filteredSasaranVisiList" :key="sv.id || sv.kode">
              <!-- PARENT ROW: SASARAN VISI -->
              <tr 
                @click="toggleSasaranExpand(sv.kode)"
                class="bg-slate-50/90 dark:bg-slate-800/70 hover:bg-slate-100/90 dark:hover:bg-slate-800 font-bold transition-colors cursor-pointer border-t-2 border-slate-200 dark:border-slate-700 select-none"
              >
                <!-- Kode & Expand Toggle -->
                <td class="py-3 px-4">
                  <div class="flex items-center space-x-2">
                    <button 
                      @click.stop="toggleSasaranExpand(sv.kode)" 
                      class="p-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 transition-transform"
                    >
                      <ChevronDown v-if="expandedSasaranMap[sv.kode]" class="w-4 h-4 text-[#308e87]" />
                      <ChevronRight v-else class="w-4 h-4 text-slate-400" />
                    </button>
                    <span class="px-2.5 py-0.5 rounded-lg text-xs font-black bg-[#308e87] text-white shadow-sm shadow-[#308e87]/20">
                      {{ sv.kode }}
                    </span>
                  </div>
                </td>

                <!-- Uraian Sasaran Visi -->
                <td class="py-3 px-4 text-slate-900 dark:text-white font-extrabold text-xs leading-snug">
                  <div class="flex items-center space-x-2">
                    <span>{{ sv.urai }}</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#308e87]/10 text-[#308e87] border border-[#308e87]/20 shrink-0">
                      {{ sv.indikator_list ? sv.indikator_list.length : 0 }} Indikator
                    </span>
                  </div>
                </td>

                <!-- Blank Columns for Parent -->
                <td class="py-3 px-4 text-slate-400 text-xs">-</td>
                <td class="py-3 px-4 text-center text-slate-400">-</td>
                <td class="py-3 px-4 text-center text-slate-400 bg-blue-50/20 dark:bg-blue-950/10">-</td>
                <td class="py-3 px-4 text-center text-slate-400 bg-teal-50/20 dark:bg-teal-950/10">-</td>
                <td class="py-3 px-4 text-center text-slate-400 bg-amber-50/20 dark:bg-amber-950/10">-</td>
                <td class="py-3 px-4 text-center text-slate-400 bg-emerald-50/20 dark:bg-emerald-950/10">-</td>

                <!-- Parent Actions -->
                <td class="py-3 px-4 text-center" @click.stop>
                  <div class="flex items-center justify-center space-x-1">
                    <button 
                      @click="openAddIndikatorModal(sv.kode)"
                      class="p-1.5 rounded-lg text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 cursor-pointer"
                      title="Tambah Indikator di Sasaran ini"
                    >
                      <Plus class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="openEditSasaranModal(sv)"
                      class="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 cursor-pointer"
                      title="Edit Sasaran Visi"
                    >
                      <Edit3 class="w-3.5 h-3.5" />
                    </button>
                    <button 
                      @click="handleDeleteSasaran(sv)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                      title="Hapus Sasaran Visi"
                    >
                      <Trash2 class="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>

              <!-- CHILD ROWS: INDIKATOR SASARAN VISI -->
              <template v-if="expandedSasaranMap[sv.kode]">
                <tr v-if="!sv.indikator_list || sv.indikator_list.length === 0">
                  <td colspan="9" class="py-4 pl-12 pr-4 text-slate-400 italic bg-white dark:bg-[#141d30]">
                    <div class="flex items-center space-x-2 text-xs">
                      <CornerDownRight class="w-4 h-4 text-slate-400" />
                      <span>Belum ada indikator sasaran visi terdaftar. Klik tombol <strong>+</strong> pada baris di atas untuk menambahkan indikator.</span>
                    </div>
                  </td>
                </tr>

                <tr 
                  v-for="ind in sv.indikator_list" 
                  :key="ind.id || ind.kode_indikator"
                  class="bg-white dark:bg-[#141d30] hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <!-- Indikator Kode with Tree Branch Icon -->
                  <td class="py-2.5 px-4 pl-8">
                    <div class="flex items-center space-x-1.5 font-mono text-xs">
                      <CornerDownRight class="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span class="font-bold text-[#308e87] dark:text-[#3aada4]">
                        #{{ ind.kode_indikator }}
                      </span>
                    </div>
                  </td>

                  <!-- Uraian Indikator Kinerja -->
                  <td class="py-2.5 px-4 text-slate-800 dark:text-slate-200 font-semibold leading-relaxed">
                    {{ ind.urai_indikator }}
                  </td>

                  <!-- Target RPJPN / Tagging -->
                  <td class="py-2.5 px-4">
                    <div class="flex flex-wrap gap-1" v-if="ind.tag_indikator_rpjpn && ind.tag_indikator_rpjpn.length > 0">
                      <span 
                        v-for="(tag, tagIdx) in ind.tag_indikator_rpjpn" 
                        :key="tagIdx"
                        class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800"
                      >
                        {{ tag }}
                      </span>
                    </div>
                    <span v-else class="text-slate-400 text-xs italic">-</span>
                  </td>

                  <!-- Kondisi Awal -->
                  <td class="py-2.5 px-4 text-center font-semibold text-slate-700 dark:text-slate-300">
                    {{ ind.kondisi_awal || '-' }}
                  </td>

                  <!-- Target 1 (2025–2029) -->
                  <td class="py-2.5 px-4 text-center font-bold text-blue-600 dark:text-blue-400 bg-blue-50/20 dark:bg-blue-950/10">
                    {{ ind.target_1 || '-' }}
                  </td>

                  <!-- Target 2 (2030–2034) -->
                  <td class="py-2.5 px-4 text-center font-bold text-teal-600 dark:text-teal-400 bg-teal-50/20 dark:bg-teal-950/10">
                    {{ ind.target_2 || '-' }}
                  </td>

                  <!-- Target 3 (2035–2039) -->
                  <td class="py-2.5 px-4 text-center font-bold text-amber-600 dark:text-amber-400 bg-amber-50/20 dark:bg-amber-950/10">
                    {{ ind.target_3 || '-' }}
                  </td>

                  <!-- Target 4 (2040–2045) -->
                  <td class="py-2.5 px-4 text-center font-black text-emerald-600 dark:text-emerald-400 bg-emerald-50/30 dark:bg-emerald-950/20">
                    {{ ind.target_4 || '-' }}
                  </td>

                  <!-- Child Actions -->
                  <td class="py-2.5 px-4 text-center">
                    <div class="flex items-center justify-center space-x-1">
                      <button 
                        @click="openEditIndikatorModal(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer"
                        title="Edit Indikator"
                      >
                        <Edit3 class="w-3.5 h-3.5" />
                      </button>
                      <button 
                        @click="handleDeleteIndikator(ind)"
                        class="p-1 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 cursor-pointer"
                        title="Hapus Indikator"
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

    <!-- ==================== MODAL 3: TAMBAH / EDIT SASARAN VISI ==================== -->
    <div 
      v-if="showSasaranModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showSasaranModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Target class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditSasaran ? 'Edit Sasaran Visi RPJPD' : 'Tambah Sasaran Visi RPJPD' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_sasaran_visi</code></p>
            </div>
          </div>
          <button @click="showSasaranModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveSasaranVisiData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kode Sasaran Visi</label>
              <input 
                v-model="sasaranForm.kode" 
                type="text" 
                required
                placeholder="Contoh: 1115, 1116..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold font-mono"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Nomor Urut</label>
              <input 
                v-model.number="sasaranForm.urut" 
                type="number" 
                min="1"
                placeholder="1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Sasaran Visi</label>
            <textarea 
              v-model="sasaranForm.urai" 
              rows="3" 
              required
              placeholder="Masukkan uraian sasaran visi RPJPD secara lengkap..." 
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none leading-relaxed"
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
              <span>{{ isEditSasaran ? 'Simpan Perubahan' : 'Tambah Sasaran Visi' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== MODAL 4: TAMBAH / EDIT INDIKATOR SASARAN VISI ==================== -->
    <div 
      v-if="showIndikatorModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="showIndikatorModal = false"
    >
      <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-2xl shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <div class="flex items-center space-x-2.5">
            <div class="w-8 h-8 rounded-xl bg-[#308e87]/10 text-[#308e87] flex items-center justify-center">
              <Sparkles class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-base font-black text-slate-900 dark:text-white">
                {{ isEditIndikator ? 'Edit Indikator Sasaran Visi' : 'Tambah Indikator Sasaran Visi' }}
              </h3>
              <p class="text-[10px] text-slate-400">Database: <code class="font-mono">rpjpd_indikator_sasaran_visi</code></p>
            </div>
          </div>
          <button @click="showIndikatorModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <form @submit.prevent="saveIndikatorVisiData" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Sasaran Visi Induk</label>
              <select 
                v-model="indikatorForm.kode_sasaran_visi" 
                required
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
              >
                <option v-for="sv in sasaranVisiList" :key="sv.kode" :value="sv.kode">
                  [{{ sv.kode }}] {{ sv.urai.substring(0, 45) }}...
                </option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kode Indikator</label>
              <input 
                v-model="indikatorForm.kode_indikator" 
                type="text" 
                required
                placeholder="Contoh: 1, 2, 3..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-mono"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Uraian Indikator Kinerja</label>
            <input 
              v-model="indikatorForm.urai_indikator" 
              type="text" 
              required
              placeholder="Contoh: Pendapatan Perkapita (Juta Rp), Indeks Gini..." 
              class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Target / Tagging RPJPN (Pisahkan koma)</label>
              <input 
                v-model="indikatorForm.tag_rpjpn_text" 
                type="text" 
                placeholder="Contoh: 01.01.01, 01.01.02" 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-mono"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-300 mb-1">Kondisi Awal (Baseline)</label>
              <input 
                v-model="indikatorForm.kondisi_awal" 
                type="text" 
                placeholder="Contoh: 54.34, 0.380..." 
                class="w-full px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-[#308e87] focus:outline-none font-bold"
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
                  v-model="indikatorForm.target_1" 
                  type="text" 
                  placeholder="55.00" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-teal-600 dark:text-teal-400 mb-1">Tahap 2 (2030–2034)</label>
                <input 
                  v-model="indikatorForm.target_2" 
                  type="text" 
                  placeholder="65.00" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-amber-600 dark:text-amber-400 mb-1">Tahap 3 (2035–2039)</label>
                <input 
                  v-model="indikatorForm.target_3" 
                  type="text" 
                  placeholder="75.00" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-bold"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-emerald-600 dark:text-emerald-400 mb-1">Tahap 4 (2040–2045)</label>
                <input 
                  v-model="indikatorForm.target_4" 
                  type="text" 
                  placeholder="85.00" 
                  class="w-full px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-center font-black"
                />
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-2 pt-3 border-t border-slate-100 dark:border-slate-800">
            <button 
              type="button"
              @click="showIndikatorModal = false"
              class="px-4 py-2 rounded-xl font-bold text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
            >
              Batal
            </button>
            <button 
              type="submit"
              :disabled="savingIndikator"
              class="px-5 py-2 rounded-xl font-black text-xs bg-[#308e87] hover:bg-[#27756f] text-white shadow-md shadow-[#308e87]/25 flex items-center space-x-1.5 disabled:opacity-50"
            >
              <Loader2 v-if="savingIndikator" class="w-3.5 h-3.5 animate-spin" />
              <span>{{ isEditIndikator ? 'Simpan Perubahan' : 'Tambah Indikator' }}</span>
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

const searchQuerySasaran = ref('')
const expandedSasaranMap = ref({})
const loadingSasaran = ref(false)
const savingSasaran = ref(false)
const savingIndikator = ref(false)

const sasaranVisiList = ref([])

const showSasaranModal = ref(false)
const isEditSasaran = ref(false)
const currentSasaranId = ref(null)
const sasaranForm = ref({
  kode: '',
  urai: '',
  urut: 1,
  no: 1
})

const showIndikatorModal = ref(false)
const isEditIndikator = ref(false)
const currentIndikatorId = ref(null)
const indikatorForm = ref({
  kode_sasaran_visi: '',
  kode_indikator: '',
  urai_indikator: '',
  tag_rpjpn_text: '',
  kondisi_awal: '',
  baseline: '',
  target_1: '',
  target_2: '',
  target_3: '',
  target_4: ''
})

const totalIndikatorCount = computed(() => {
  return sasaranVisiList.value.reduce((acc, sv) => acc + (sv.indikator_list ? sv.indikator_list.length : 0), 0)
})

const filteredSasaranVisiList = computed(() => {
  if (!searchQuerySasaran.value) return sasaranVisiList.value
  const q = searchQuerySasaran.value.toLowerCase()
  return sasaranVisiList.value.filter(sv => {
    const matchSasaran = (sv.urai && sv.urai.toLowerCase().includes(q)) || 
                         (sv.kode && sv.kode.toLowerCase().includes(q))
    const matchIndikator = sv.indikator_list && sv.indikator_list.some(ind => 
      (ind.urai_indikator && ind.urai_indikator.toLowerCase().includes(q)) || 
      (ind.kode_indikator && ind.kode_indikator.toLowerCase().includes(q))
    )
    if (matchSasaran || matchIndikator) {
      expandedSasaranMap.value[sv.kode] = true
      return true
    }
    return false
  })
})

function toggleSasaranExpand(kode) {
  expandedSasaranMap.value[kode] = !expandedSasaranMap.value[kode]
}

function expandAllSasaran() {
  sasaranVisiList.value.forEach(sv => {
    expandedSasaranMap.value[sv.kode] = true
  })
}

function collapseAllSasaran() {
  sasaranVisiList.value.forEach(sv => {
    expandedSasaranMap.value[sv.kode] = false
  })
}

async function fetchSasaranVisiData() {
  loadingSasaran.value = true
  try {
    const res = await axios.get('/api/v1/rpjpd/sasaran-visi-lengkap')
    if (res.data && res.data.daftar_sasaran_visi) {
      sasaranVisiList.value = res.data.daftar_sasaran_visi
      res.data.daftar_sasaran_visi.forEach(sv => {
        if (expandedSasaranMap.value[sv.kode] === undefined) {
          expandedSasaranMap.value[sv.kode] = true
        }
      })
    }
  } catch (err) {
    console.error('Error fetching RPJPD Sasaran Visi data:', err)
  } finally {
    loadingSasaran.value = false
  }
}

function openAddSasaranVisiModal() {
  isEditSasaran.value = false
  currentSasaranId.value = null
  sasaranForm.value = {
    kode: (1114 + sasaranVisiList.value.length + 1).toString(),
    urai: '',
    urut: sasaranVisiList.value.length + 1,
    no: sasaranVisiList.value.length + 1
  }
  showSasaranModal.value = true
}

function openEditSasaranModal(sv) {
  isEditSasaran.value = true
  currentSasaranId.value = sv.id
  sasaranForm.value = {
    kode: sv.kode,
    urai: sv.urai,
    urut: sv.urut || 1,
    no: sv.no || 1
  }
  showSasaranModal.value = true
}

async function saveSasaranVisiData() {
  savingSasaran.value = true
  try {
    const payload = {
      kode: sasaranForm.value.kode,
      urai: sasaranForm.value.urai,
      urut: sasaranForm.value.urut,
      no: sasaranForm.value.no
    }
    if (isEditSasaran.value) {
      await axios.put(`/api/v1/rpjpd/sasaran-visi/${currentSasaranId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/sasaran-visi', {
        ...payload,
        idperiode: '20252045',
        kodepemda: '3376'
      })
    }
    showSasaranModal.value = false
    await fetchSasaranVisiData()
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditSasaran.value ? 'Sasaran Visi berhasil diperbarui' : 'Sasaran Visi baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Sasaran Visi', 'error')
  } finally {
    savingSasaran.value = false
  }
}

async function handleDeleteSasaran(sv) {
  const result = await Swal.fire({
    title: 'Hapus Sasaran Visi?',
    html: `Apakah Anda yakin ingin menghapus Sasaran Visi [<strong>${sv.kode}</strong>]: <br/>"${sv.urai.substring(0, 80)}..."?<br/><br/><span class="text-xs text-red-500">Perhatian: Pastikan tidak ada indikator yang terkait sebelum menghapus.</span>`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/sasaran-visi/${sv.id}`)
      await fetchSasaranVisiData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Sasaran Visi berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Sasaran Visi', 'error')
    }
  }
}

function openAddIndikatorModal(kodeSasaran) {
  isEditIndikator.value = false
  currentIndikatorId.value = null
  const parentSasaran = sasaranVisiList.value.find(s => s.kode === kodeSasaran)
  const indCount = parentSasaran?.indikator_list?.length || 0
  
  indikatorForm.value = {
    kode_sasaran_visi: kodeSasaran || sasaranVisiList.value[0]?.kode || '',
    kode_indikator: (totalIndikatorCount.value + 1).toString(),
    urai_indikator: '',
    tag_rpjpn_text: '',
    kondisi_awal: '',
    baseline: '',
    target_1: '',
    target_2: '',
    target_3: '',
    target_4: '',
    urut: indCount + 1
  }
  showIndikatorModal.value = true
}

function openEditIndikatorModal(ind) {
  isEditIndikator.value = true
  currentIndikatorId.value = ind.id
  const tagStr = Array.isArray(ind.tag_indikator_rpjpn) ? ind.tag_indikator_rpjpn.join(', ') : (ind.tag_indikator_rpjpn || '')
  indikatorForm.value = {
    kode_sasaran_visi: ind.kode_sasaran_visi,
    kode_indikator: ind.kode_indikator,
    urai_indikator: ind.urai_indikator,
    tag_rpjpn_text: tagStr,
    kondisi_awal: ind.kondisi_awal || '',
    baseline: ind.baseline || '',
    target_1: ind.target_1 || '',
    target_2: ind.target_2 || '',
    target_3: ind.target_3 || '',
    target_4: ind.target_4 || '',
    urut: ind.urut || 1
  }
  showIndikatorModal.value = true
}

async function saveIndikatorVisiData() {
  savingIndikator.value = true
  try {
    const tagArray = indikatorForm.value.tag_rpjpn_text
      ? indikatorForm.value.tag_rpjpn_text.split(',').map(s => s.trim()).filter(Boolean)
      : []

    const payload = {
      kode_sasaran_visi: indikatorForm.value.kode_sasaran_visi,
      kode_indikator: indikatorForm.value.kode_indikator,
      urai_indikator: indikatorForm.value.urai_indikator,
      tag_indikator_rpjpn: tagArray,
      kondisi_awal: indikatorForm.value.kondisi_awal,
      baseline: indikatorForm.value.baseline || indikatorForm.value.kondisi_awal,
      target_1: indikatorForm.value.target_1,
      target_2: indikatorForm.value.target_2,
      target_3: indikatorForm.value.target_3,
      target_4: indikatorForm.value.target_4,
      urut: indikatorForm.value.urut
    }

    if (isEditIndikator.value) {
      await axios.put(`/api/v1/rpjpd/indikator-sasaran-visi/${currentIndikatorId.value}`, payload)
    } else {
      await axios.post('/api/v1/rpjpd/indikator-sasaran-visi', {
        ...payload,
        idperiode: '20252045',
        kodepemda: '3376'
      })
    }
    showIndikatorModal.value = false
    await fetchSasaranVisiData()
    expandedSasaranMap.value[indikatorForm.value.kode_sasaran_visi] = true
    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: 'success',
      title: isEditIndikator.value ? 'Indikator berhasil diperbarui' : 'Indikator baru berhasil ditambahkan',
      showConfirmButton: false,
      timer: 2000
    })
  } catch (err) {
    Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menyimpan Indikator Sasaran Visi', 'error')
  } finally {
    savingIndikator.value = false
  }
}

async function handleDeleteIndikator(ind) {
  const result = await Swal.fire({
    title: 'Hapus Indikator?',
    html: `Apakah Anda yakin ingin menghapus Indikator [<strong>#${ind.kode_indikator}</strong>]: <br/>"${ind.urai_indikator.substring(0, 80)}..."?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#64748b',
    confirmButtonText: 'Ya, Hapus',
    cancelButtonText: 'Batal'
  })

  if (result.isConfirmed) {
    try {
      await axios.delete(`/api/v1/rpjpd/indikator-sasaran-visi/${ind.id}`)
      await fetchSasaranVisiData()
      Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Indikator berhasil dihapus',
        showConfirmButton: false,
        timer: 2000
      })
    } catch (err) {
      Swal.fire('Gagal', err.response?.data?.detail || 'Gagal menghapus Indikator', 'error')
    }
  }
}

onMounted(() => {
  fetchSasaranVisiData()
})

defineExpose({
  fetchSasaranVisiData,
  sasaranVisiList,
  totalIndikatorCount
})
</script>
