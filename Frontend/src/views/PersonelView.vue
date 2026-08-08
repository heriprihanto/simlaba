<template>
  <div class="space-y-6 pb-12">
    <!-- Header Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] dark:from-[#0f1729] dark:via-[#162032] dark:to-[#1a2940] p-6 sm:p-7 text-white shadow-lg transition-colors duration-300">
      <div class="absolute inset-0 opacity-[0.05]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;40&quot; height=&quot;40&quot; viewBox=&quot;0 0 40 40&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot; fill-rule=&quot;evenodd&quot;%3E%3Cpath d=&quot;M0 40L40 0H20L0 20M40 40V20L20 40&quot;/%3E%3C/g%3E%3C/svg%3E')"></div>
      <div class="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2 mb-2">
            <span class="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest bg-[#3aada4] text-white shadow-sm shadow-[#3aada4]/30">
              SDM Aparatur
            </span>
            <span class="text-xs text-white/60 font-semibold">SIMLABA Kota Tegal</span>
          </div>
          <h1 class="text-2xl font-black tracking-tight text-white">Manajemen Personel & Pegawai</h1>
          <p class="text-xs text-[#3aada4] mt-1 font-semibold">
            {{ viewMode === 'opd' ? 'Pilih Perangkat Daerah untuk mengelola daftar pegawai' : selectedOpd?.nama_pd }}
          </p>
        </div>

        <div v-if="viewMode === 'personel'" class="flex items-center space-x-2">
          <button @click="backToOpdList"
            class="px-4 py-2.5 bg-white/10 hover:bg-white/20 backdrop-blur text-white text-xs font-bold rounded-xl border border-white/20 flex items-center space-x-1.5 transition-all">
            <ArrowLeft class="w-4 h-4" />
            <span>Kembali ke OPD</span>
          </button>
          <button @click="openAddModal"
            class="px-4 py-2.5 bg-gradient-to-r from-[#f39159] to-[#f8b088] text-white text-xs font-black rounded-xl shadow-lg shadow-[#f39159]/25 flex items-center space-x-1.5 transition-all hover:shadow-xl active:scale-[0.98]">
            <UserPlus class="w-4 h-4" />
            <span>Tambah Personel Baru</span>
          </button>
        </div>
      </div>
    </div>

    <!-- LEVEL 1: TABEL OPD -->
    <div v-if="viewMode === 'opd'" class="space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-[11px]" />
          <input v-model="searchOpdQuery" type="text" placeholder="Cari Kode atau Nama OPD..."
            class="w-full pl-10 pr-9 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-[#308e87] transition-all shadow-sm" />
          <button v-if="searchOpdQuery" @click="searchOpdQuery = ''" class="absolute right-3 top-[11px] text-slate-400 hover:text-[#308e87]">
            <X class="w-4 h-4" />
          </button>
        </div>
        <span class="text-xs font-bold text-slate-500 dark:text-slate-400">
          Total: <strong class="text-[#308e87] dark:text-[#3aada4]">{{ filteredOpdList.length }}</strong> Perangkat Daerah
        </span>
      </div>

      <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-5 w-12 text-center">No</th>
                <th class="py-3.5 px-5 w-52">Kode OPD</th>
                <th class="py-3.5 px-5">Nama Perangkat Daerah</th>
                <th class="py-3.5 px-5 text-center w-36">Jumlah Personel</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50">
              <tr v-if="loadingOpd">
                <td colspan="5" class="py-20 text-center">
                  <Loader2 class="w-7 h-7 animate-spin mx-auto mb-2 text-[#308e87]" />
                  <span class="font-bold text-xs text-slate-400">Memuat data Perangkat Daerah...</span>
                </td>
              </tr>
              <tr v-else-if="filteredOpdList.length === 0">
                <td colspan="5" class="py-20 text-center">
                  <Building2 class="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p class="font-bold text-xs text-slate-500 dark:text-slate-400">Tidak ada Perangkat Daerah ditemukan</p>
                </td>
              </tr>
              <tr v-for="(opd, idx) in filteredOpdList" :key="opd.id_sub_pd"
                  @click="selectOpd(opd)"
                  class="even:bg-[#308e87]/[0.02] dark:even:bg-[#308e87]/[0.04] hover:bg-[#308e87]/[0.06] dark:hover:bg-[#308e87]/[0.08] transition-colors cursor-pointer group">
                <td class="py-3.5 px-5 text-center font-black text-slate-400 dark:text-slate-500">{{ idx + 1 }}</td>
                <td class="py-3.5 px-5 font-mono font-bold text-[#308e87] dark:text-[#3aada4] text-[11px]">{{ opd.kode || '-' }}</td>
                <td class="py-3.5 px-5 font-bold text-slate-800 dark:text-slate-200 group-hover:text-[#308e87] dark:group-hover:text-[#3aada4] transition-colors">
                  <div>{{ opd.nama_pd }}</div>
                  
                </td>
                <td class="py-3.5 px-5 text-center">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-[11px] font-black"
                        :class="opd.jumlah_personel > 0 ? 'bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'">
                    <Users class="w-3.5 h-3.5 mr-1.5" />
                    {{ opd.jumlah_personel }} Pegawai
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- LEVEL 2: DAFTAR PERSONEL PER OPD -->
    <div v-else-if="viewMode === 'personel'" class="space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-[11px]" />
          <input v-model="searchPersonelQuery" @input="debouncedFetchPersonel" type="text" placeholder="Cari Nama, NIP, atau Jabatan..."
            class="w-full pl-10 pr-9 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-[#308e87] transition-all shadow-sm" />
          <button v-if="searchPersonelQuery" @click="clearPersonelSearch" class="absolute right-3 top-[11px] text-slate-400 hover:text-[#308e87]">
            <X class="w-4 h-4" />
          </button>
        </div>
        <span class="text-xs font-bold text-slate-500 dark:text-slate-400">
          Total: <strong class="text-[#308e87] dark:text-[#3aada4]">{{ personelList.length }}</strong> Personel terdaftar
        </span>
      </div>

      <!-- Toast Notification -->
      <transition enter-active-class="transition duration-300 ease-out" enter-from-class="transform -translate-y-2 opacity-0" leave-active-class="transition duration-200 ease-in" leave-to-class="transform -translate-y-2 opacity-0">
        <div v-if="toast.show" class="p-3.5 rounded-xl border-2 flex items-center justify-between shadow-sm"
             :class="toast.type === 'success' ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-400/30 text-emerald-700 dark:text-emerald-400' : 'bg-red-50 dark:bg-red-950/20 border-red-400/30 text-red-700 dark:text-red-400'">
          <div class="flex items-center space-x-2 text-xs font-bold">
            <CheckCircle v-if="toast.type === 'success'" class="w-4 h-4" />
            <AlertCircle v-else class="w-4 h-4" />
            <span>{{ toast.message }}</span>
          </div>
          <button @click="toast.show = false" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300">
            <X class="w-4 h-4" />
          </button>
        </div>
      </transition>

      <!-- Personel Table -->
      <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-4 w-10 text-center">No</th>
                <th class="py-3.5 px-4 w-12 text-center">Foto</th>
                <th class="py-3.5 px-4">NIP</th>
                <th class="py-3.5 px-4">Nama Lengkap</th>
                <th class="py-3.5 px-4">Jabatan</th>
                <th class="py-3.5 px-4 text-center">Golongan & Pangkat</th>
                <th class="py-3.5 px-4 text-center w-28" title="Aksi"><Settings class="w-4 h-4 mx-auto" /></th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/50">
              <tr v-if="loadingPersonel">
                <td colspan="7" class="py-20 text-center">
                  <Loader2 class="w-7 h-7 animate-spin mx-auto mb-2 text-[#308e87]" />
                  <span class="font-bold text-xs text-slate-400">Memuat data personel...</span>
                </td>
              </tr>

              <tr v-else-if="personelList.length === 0">
                <td colspan="7" class="py-20 text-center">
                  <UserX class="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p class="font-bold text-xs text-slate-500 dark:text-slate-400">Belum ada personel pada OPD ini</p>
                  <button @click="openAddModal" class="mt-2 text-xs text-[#308e87] dark:text-[#3aada4] font-black hover:underline cursor-pointer">
                    + Tambah Personel Pertama
                  </button>
                </td>
              </tr>

              <tr v-for="(item, idx) in personelList" :key="item.id"
                  class="even:bg-[#308e87]/[0.02] dark:even:bg-[#308e87]/[0.04] hover:bg-[#308e87]/[0.06] dark:hover:bg-[#308e87]/[0.08] transition-colors group">
                <td class="py-3.5 px-4 text-center font-black text-slate-400 dark:text-slate-500">{{ idx + 1 }}</td>
                
                <!-- Foto Profil Avatar -->
                <td class="py-3.5 px-4 text-center">
                  <img v-if="item.foto_profil" :src="item.foto_profil" :alt="item.nama" class="w-9 h-9 rounded-full object-cover border-2 border-[#308e87]/20 mx-auto shadow-sm" />
                  <div v-else class="w-9 h-9 rounded-full bg-gradient-to-br from-[#308e87] to-[#3aada4] text-white flex items-center justify-center font-black text-xs mx-auto shadow-sm shadow-[#308e87]/25">
                    {{ getInitials(item.nama) }}
                  </div>
                </td>

                <td class="py-3.5 px-4 font-mono font-semibold text-slate-500 dark:text-slate-400 text-[11px]">{{ item.nip || '-' }}</td>
                <td class="py-3.5 px-4 font-bold text-slate-800 dark:text-slate-200 group-hover:text-[#308e87] dark:group-hover:text-[#3aada4] transition-colors">{{ item.nama }}</td>
                <td class="py-3.5 px-4">
                  <span class="inline-flex items-center px-2.5 py-1 rounded-lg text-[10px] font-bold bg-[#308e87]/10 dark:bg-[#308e87]/15 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/15">
                    {{ item.jabatan || 'Personel' }}
                  </span>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <span v-if="item.golongan || item.pangkat" class="inline-flex items-center px-2.5 py-0.5 rounded-lg font-mono text-[10px] font-black bg-[#f39159]/10 text-[#f39159] dark:text-[#f8b088] border border-[#f39159]/15">
                    {{ item.golongan || '' }} {{ item.pangkat ? `(${item.pangkat})` : '' }}
                  </span>
                  <span v-else class="text-slate-300 dark:text-slate-600">-</span>
                </td>
                <td class="py-3.5 px-4 text-center">
                  <div class="flex items-center justify-center space-x-1">
                    <button @click="openEditModal(item)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-[#308e87] dark:hover:text-[#3aada4] hover:bg-[#308e87]/10 transition-all cursor-pointer" title="Edit">
                      <Edit3 class="w-4 h-4" />
                    </button>
                    <button @click="confirmDelete(item)"
                      class="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-500/10 transition-all cursor-pointer" title="Hapus">
                      <Trash2 class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ═══ MODAL FORM TAMBAH / EDIT PERSONEL ═══ -->
    <div v-if="showFormModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm">
      <div class="bg-white dark:bg-[#141d30] rounded-2xl shadow-2xl max-w-lg w-full max-h-[90vh] flex flex-col overflow-hidden border-2 border-slate-200 dark:border-slate-700/50">
        
        <div class="px-6 py-4 bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] text-white flex items-center justify-between shrink-0">
          <div class="flex items-center space-x-2">
            <UserCheck class="w-5 h-5 text-[#3aada4]" />
            <h3 class="font-black text-sm">{{ isEditing ? 'Edit Personel' : 'Tambah Personel Baru' }}</h3>
          </div>
          <button @click="showFormModal = false" class="text-white/50 hover:text-white transition-colors cursor-pointer"><X class="w-5 h-5" /></button>
        </div>

        <form @submit.prevent="savePersonel" class="p-6 space-y-4 text-xs overflow-y-auto flex-1">
          
          <!-- OPD Indicator -->
          <div class="p-3 rounded-xl bg-[#308e87]/5 dark:bg-[#308e87]/10 border border-[#308e87]/15">
            <span class="text-[9px] text-[#308e87] dark:text-[#3aada4] block font-black uppercase tracking-widest">OPD Terpilih</span>
            <span class="font-bold text-slate-800 dark:text-white">{{ selectedOpd?.nama_pd || 'Kota Tegal' }}</span>
          </div>

          <!-- UPLOAD FOTO PROFIL -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border-2 border-dashed border-slate-200 dark:border-slate-700 flex items-center space-x-4">
            <div class="relative shrink-0">
              <img v-if="form.foto_profil" :src="form.foto_profil" class="w-14 h-14 rounded-full object-cover border-2 border-[#308e87]" />
              <div v-else class="w-14 h-14 rounded-full bg-gradient-to-br from-[#308e87] to-[#3aada4] text-white flex items-center justify-center font-black text-lg shadow-md shadow-[#308e87]/25">
                {{ getInitials(form.nama || 'P') }}
              </div>
              <button v-if="form.foto_profil" type="button" @click="form.foto_profil = ''" class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 hover:bg-red-600">
                <X class="w-3 h-3" />
              </button>
            </div>

            <div class="flex-1 space-y-1">
              <label class="block font-black text-slate-800 dark:text-slate-200 text-xs">Foto Profil Pegawai</label>
              <p class="text-[10px] text-slate-400">Format: JPG, PNG, WEBP (Max 2MB)</p>
              <div class="flex items-center space-x-2 pt-1">
                <label class="px-3 py-1.5 bg-[#308e87] hover:bg-[#256e69] text-white rounded-lg font-bold text-[11px] cursor-pointer inline-flex items-center space-x-1 shadow-sm">
                  <Upload class="w-3.5 h-3.5" />
                  <span>{{ uploadingPhoto ? 'Mengunggah...' : 'Pilih Foto' }}</span>
                  <input type="file" accept="image/*" @change="handleFileUpload" class="sr-only" :disabled="uploadingPhoto" />
                </label>
                <Loader2 v-if="uploadingPhoto" class="w-4 h-4 animate-spin text-[#308e87]" />
              </div>
            </div>
          </div>

          <!-- NIP -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="font-black text-[#308e87] dark:text-[#3aada4] uppercase tracking-wider text-[10px]">NIP (Nomor Induk Pegawai)</label>
              <span class="text-[9px] font-black text-[#f39159] bg-[#f39159]/10 px-2 py-0.5 rounded-lg border border-[#f39159]/15">Tanpa Spasi</span>
            </div>
            <input v-model="form.nip" @input="onNipInput" @keydown.space.prevent type="text" placeholder="198507202010012003"
              class="w-full px-3.5 py-2.5 bg-[#308e87]/5 dark:bg-[#308e87]/8 border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl font-mono text-slate-800 dark:text-white focus:outline-none focus:border-[#308e87] focus:ring-3 focus:ring-[#308e87]/10" />
          </div>

          <!-- Nama -->
          <div>
            <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">Nama Lengkap & Gelar <span class="text-red-400">*</span></label>
            <input v-model="form.nama" type="text" required placeholder="Budi Santoso, S.T., M.T."
              class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white focus:outline-none focus:border-[#308e87] focus:ring-3 focus:ring-[#308e87]/10" />
          </div>

          <!-- Jabatan -->
          <div>
            <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">Jabatan</label>
            <input v-model="form.jabatan" type="text" placeholder="Pejabat Pembuat Komitmen (PPK)"
              class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white focus:outline-none focus:border-[#308e87] focus:ring-3 focus:ring-[#308e87]/10" />
          </div>

          <!-- GOLONGAN & PANGKAT AUTO-MAPPING -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <!-- Golongan Select -->
            <div>
              <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">Golongan</label>
              <select v-model="form.golongan" @change="onGolonganChange"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-bold focus:outline-none focus:border-[#308e87]">
                <option value="">-- Pilih Golongan --</option>
                <option v-for="(pName, gCode) in golonganPangkatMap" :key="gCode" :value="gCode">
                  Golongan {{ gCode }}
                </option>
              </select>
            </div>

            <!-- Pangkat Input (Auto-filled) -->
            <div>
              <label class="block font-black text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider text-[10px]">Pangkat (Otomatis Terisi)</label>
              <input v-model="form.pangkat" type="text" placeholder="Penata Muda"
                class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800/50 border-2 border-slate-200 dark:border-slate-700/50 rounded-xl text-slate-800 dark:text-white font-bold focus:outline-none focus:border-[#308e87]" />
            </div>
          </div>

          <div class="pt-3 border-t-2 border-slate-100 dark:border-slate-800/50 flex items-center justify-end space-x-2">
            <button type="button" @click="showFormModal = false"
              class="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold rounded-xl cursor-pointer">Batal</button>
            <button type="submit" :disabled="submitting || uploadingPhoto"
              class="px-5 py-2.5 bg-gradient-to-r from-[#308e87] to-[#3aada4] text-white font-black rounded-xl shadow-md shadow-[#308e87]/20 flex items-center space-x-1.5 disabled:opacity-50 cursor-pointer">
              <Loader2 v-if="submitting" class="w-4 h-4 animate-spin" />
              <span>{{ submitting ? 'Menyimpan...' : (isEditing ? 'Simpan' : 'Tambah') }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL DELETE PERSONEL -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-sm">
      <div class="bg-white dark:bg-[#141d30] rounded-2xl shadow-2xl max-w-sm w-full p-7 text-center border-2 border-slate-200 dark:border-slate-700/50">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-red-500 to-rose-600 text-white inline-flex items-center justify-center mb-3 shadow-lg shadow-red-500/25">
          <Trash2 class="w-6 h-6" />
        </div>
        <h3 class="font-black text-base text-slate-900 dark:text-white">Hapus Personel?</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1.5">
          Apakah Anda yakin ingin menghapus personel <strong class="text-slate-800 dark:text-slate-200">{{ targetPersonel?.nama }}</strong>?
        </p>
        <div class="mt-5 flex items-center justify-center space-x-2">
          <button @click="showDeleteModal = false" class="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold rounded-xl text-xs cursor-pointer">
            Batal
          </button>
          <button @click="executeDelete" :disabled="submitting" class="px-4 py-2.5 bg-gradient-to-r from-red-500 to-rose-600 text-white font-black rounded-xl shadow-md shadow-red-500/20 text-xs disabled:opacity-50 cursor-pointer">
            {{ submitting ? 'Menghapus...' : 'Ya, Hapus' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { 
  Search, X, Users, Building2, ChevronRight, ArrowLeft,
  UserPlus, UserCheck, UserX, Edit3, Trash2, Upload,
  Loader2, CheckCircle, AlertCircle, Settings 
} from 'lucide-vue-next'

const authStore = useAuthStore()
const viewMode = ref('opd')
const opdList = ref([])
const searchOpdQuery = ref('')
const loadingOpd = ref(false)
const selectedOpd = ref(null)
const personelList = ref([])
const searchPersonelQuery = ref('')
const loadingPersonel = ref(false)
const submitting = ref(false)
const uploadingPhoto = ref(false)
const showFormModal = ref(false)
const showDeleteModal = ref(false)
const isEditing = ref(false)
const targetPersonel = ref(null)
const toast = ref({ show: false, message: '', type: 'success' })

const form = ref({
  id: null,
  nip: '',
  nama: '',
  jabatan: '',
  pangkat: '',
  golongan: '',
  tahun: 2026,
  kedudukan: 1,
  id_sub_pd: null,
  foto_profil: ''
})

// Golongan to Pangkat Mapping
const golonganPangkatMap = {
  'II/a': 'Pengatur Muda',
  'II/b': 'Pengatur Muda Tingkat I',
  'II/c': 'Pengatur',
  'II/d': 'Pengatur Tingkat I',
  'III/a': 'Penata Muda',
  'III/b': 'Penata Muda Tingkat I',
  'III/c': 'Penata',
  'III/d': 'Penata Tingkat I',
  'IV/a': 'Pembina',
  'IV/b': 'Pembina Tingkat II',
  'IV/c': 'Pembina Utama Muda',
  'IV/d': 'Pembina Utama Madya',
  'IV/e': 'Pembina Utama'
}

const onGolonganChange = () => {
  if (form.value.golongan && golonganPangkatMap[form.value.golongan]) {
    form.value.pangkat = golonganPangkatMap[form.value.golongan]
  }
}

const getInitials = (name) => {
  if (!name) return 'P'
  const parts = name.trim().split(' ')
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
}

const filteredOpdList = computed(() => {
  if (!searchOpdQuery.value.trim()) return opdList.value
  const q = searchOpdQuery.value.toLowerCase().trim()
  return opdList.value.filter(opd => 
    (opd.kode && opd.kode.toLowerCase().includes(q)) ||
    (opd.nama_pd && opd.nama_pd.toLowerCase().includes(q)) ||
    (opd.nama_pd_singkat && opd.nama_pd_singkat.toLowerCase().includes(q))
  )
})

const showToast = (msg, type = 'success') => {
  toast.value = { show: true, message: msg, type }
  setTimeout(() => { toast.value.show = false }, 4000)
}

const fetchOpdList = async () => {
  loadingOpd.value = true
  try { 
    const res = await axios.get('/api/v1/personel/opd')
    opdList.value = res.data
  }
  catch { showToast('Gagal memuat daftar OPD', 'error') }
  finally { loadingOpd.value = false }
}

const selectOpd = (opd) => { 
  selectedOpd.value = opd
  viewMode.value = 'personel'
  searchPersonelQuery.value = ''
  fetchPersonelByOpd() 
}

const backToOpdList = () => { 
  viewMode.value = 'opd'
  selectedOpd.value = null
  fetchOpdList() 
}

const fetchPersonelByOpd = async () => {
  if (!selectedOpd.value) return
  loadingPersonel.value = true
  try {
    const res = await axios.get('/api/v1/personel/', {
      params: { id_sub_pd: selectedOpd.value.id_sub_pd, q: searchPersonelQuery.value }
    })
    personelList.value = res.data.data
  } catch (err) {
    showToast('Gagal memuat daftar personel', 'error')
  } finally {
    loadingPersonel.value = false
  }
}

let searchTimeout = null
const debouncedFetchPersonel = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchPersonelByOpd(), 300)
}

const clearPersonelSearch = () => {
  searchPersonelQuery.value = ''
  fetchPersonelByOpd()
}

const onNipInput = () => {
  if (form.value.nip) {
    form.value.nip = form.value.nip.replace(/\s+/g, '')
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  uploadingPhoto.value = true

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await axios.post('/api/v1/personel/upload-foto', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    form.value.foto_profil = res.data.url
    showToast('Foto profil berhasil diunggah!')
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal mengunggah foto profil', 'error')
  } finally {
    uploadingPhoto.value = false
  }
}

const openAddModal = () => {
  isEditing.value = false
  form.value = {
    id: null,
    nip: '',
    nama: '',
    jabatan: '',
    pangkat: '',
    golongan: '',
    tahun: 2026,
    kedudukan: 1,
    id_sub_pd: selectedOpd.value?.id_sub_pd,
    foto_profil: ''
  }
  showFormModal.value = true
}

const openEditModal = (item) => {
  isEditing.value = true
  form.value = { 
    id: item.id,
    nip: item.nip || '',
    nama: item.nama || '',
    jabatan: item.jabatan || '',
    pangkat: item.pangkat || '',
    golongan: item.golongan || '',
    tahun: item.tahun || 2026,
    kedudukan: item.kedudukan || 1,
    id_sub_pd: item.id_sub_pd,
    foto_profil: item.foto_profil || ''
  }
  showFormModal.value = true
}

const savePersonel = async () => {
  if (!form.value.nama) return
  submitting.value = true

  try {
    if (isEditing.value) {
      await axios.put(`/api/v1/personel/${form.value.id}`, form.value)
      showToast('Data personel berhasil diperbarui!')
    } else {
      await axios.post('/api/v1/personel/', form.value)
      showToast('Personel baru berhasil ditambahkan!')
    }
    showFormModal.value = false
    fetchPersonelByOpd()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal menyimpan data personel', 'error')
  } finally {
    submitting.value = false
  }
}

const confirmDelete = (item) => {
  targetPersonel.value = item
  showDeleteModal.value = true
}

const executeDelete = async () => {
  if (!targetPersonel.value) return
  submitting.value = true
  try {
    await axios.delete(`/api/v1/personel/${targetPersonel.value.id}`)
    showToast('Personel berhasil dihapus!')
    showDeleteModal.value = false
    fetchPersonelByOpd()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal menghapus personel', 'error')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchOpdList()
})
</script>
