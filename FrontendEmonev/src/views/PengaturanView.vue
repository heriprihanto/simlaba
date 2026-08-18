<template>
  <div class="space-y-6 pb-12">

    <!-- Header Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#1a4845] via-[#245f5a] to-[#308e87] dark:from-[#0f1729] dark:via-[#162032] dark:to-[#1a2940] p-6 text-white shadow-lg">
      <div class="absolute inset-0 opacity-[0.05]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;40&quot; height=&quot;40&quot; viewBox=&quot;0 0 40 40&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot; fill-rule=&quot;evenodd&quot;%3E%3Cpath d=&quot;M0 40L40 0H20L0 20M40 40V20L20 40&quot;/%3E%3C/g%3E%3C/svg%3E')"></div>
      <div class="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2 mb-2">
            <span class="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-widest bg-[#3aada4] text-white shadow-sm shadow-[#3aada4]/30">
              Pengaturan Sistem
            </span>
            <span class="text-xs text-white/60 font-semibold">SIMLABA Kota Tegal</span>
          </div>
          <h1 class="text-2xl font-black tracking-tight text-white">Manajemen Pengguna, OPD &amp; Tagging</h1>
          <p class="text-xs text-[#3aada4] mt-1 font-semibold">Kelola hak akses pengguna, reset password, master data Perangkat Daerah, dan Referensi Tagging</p>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs (User | Perangkat Daerah | Tagging) -->
    <div class="flex items-center justify-between border-b-2 border-slate-200 dark:border-slate-800">
      <div class="flex space-x-2">
        <button
          @click="activeTab = 'user'"
          class="px-5 py-3 font-black text-xs transition-all border-b-2 flex items-center space-x-2 cursor-pointer"
          :class="activeTab === 'user' 
            ? 'border-[#308e87] text-[#308e87] dark:text-[#3aada4]' 
            : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'"
        >
          <UserCog class="w-4 h-4" />
          <span>Pengaturan User</span>
          <span class="ml-1.5 px-2 py-0.5 rounded-full text-[10px] font-black bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4]">
            {{ userTotal }}
          </span>
        </button>

        <button
          @click="activeTab = 'opd'"
          class="px-5 py-3 font-black text-xs transition-all border-b-2 flex items-center space-x-2 cursor-pointer"
          :class="activeTab === 'opd' 
            ? 'border-[#308e87] text-[#308e87] dark:text-[#3aada4]' 
            : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'"
        >
          <Building2 class="w-4 h-4" />
          <span>Perangkat Daerah</span>
          <span class="ml-1.5 px-2 py-0.5 rounded-full text-[10px] font-black bg-[#f39159]/10 text-[#f39159] dark:text-[#f8b088]">
            {{ opdList.length }}
          </span>
        </button>

        <button
          @click="activeTab = 'tagging'"
          class="px-5 py-3 font-black text-xs transition-all border-b-2 flex items-center space-x-2 cursor-pointer"
          :class="activeTab === 'tagging' 
            ? 'border-[#308e87] text-[#308e87] dark:text-[#3aada4]' 
            : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'"
        >
          <Tag class="w-4 h-4" />
          <span>Tagging</span>
          <span class="ml-1.5 px-2 py-0.5 rounded-full text-[10px] font-black bg-purple-500/10 text-purple-600 dark:text-purple-400">
            {{ taggingList.length }}
          </span>
        </button>
      </div>
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

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- TAB 1: PENGATURAN USER (sso_users) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="activeTab === 'user'" class="space-y-5">

      <!-- Action & Search Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <!-- Search User Input -->
          <div class="relative w-full sm:w-72">
            <Search class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-[10px]" />
            <input 
              v-model="searchUserQuery"
              @input="debouncedFetchUsers"
              type="text"
              placeholder="Cari Username, Nama, Email..."
              class="w-full pl-10 pr-9 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-[#308e87] shadow-sm transition-all"
            />
            <button v-if="searchUserQuery" @click="clearUserSearch" class="absolute right-3 top-[10px] text-slate-400 hover:text-[#308e87]">
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Role Filter -->
          <select 
            v-model="selectedRoleFilter"
            @change="fetchUsers"
            class="px-3 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 font-bold focus:outline-none focus:border-[#308e87] shadow-sm transition-all"
          >
            <option :value="null">Semua Role Pengguna</option>
            <option v-for="(name, id) in rolesMap" :key="id" :value="Number(id)">
              {{ id }}. {{ name }}
            </option>
          </select>
        </div>

        <button 
          @click="openAddUserModal"
          class="px-4 py-2.5 bg-[#308e87] hover:bg-[#256e69] text-white font-black text-xs rounded-xl shadow-sm shadow-[#308e87]/30 flex items-center justify-center space-x-1.5 transition-all cursor-pointer"
        >
          <Plus class="w-4 h-4" />
          <span>Tambah User Baru</span>
        </button>
      </div>

      <!-- Users Table -->
      <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-4 w-12 text-center">No</th>
                <th class="py-3.5 px-4">Username &amp; Nama</th>
                <th class="py-3.5 px-4">Role Akses</th>
                <th class="py-3.5 px-4">Email &amp; Telp</th>
                <th class="py-3.5 px-4">Akses Perangkat Daerah</th>
                <th class="py-3.5 px-4 text-center">Status</th>
                <th class="py-3.5 px-4 text-center w-36" title="Aksi"><Settings class="w-4 h-4 mx-auto" /></th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/40">
              <tr v-if="loadingUsers">
                <td colspan="7" class="py-16 text-center">
                  <Loader2 class="w-7 h-7 animate-spin mx-auto mb-2 text-[#308e87]" />
                  <span class="font-bold text-xs text-slate-400">Memuat data pengguna...</span>
                </td>
              </tr>

              <tr v-else-if="userList.length === 0">
                <td colspan="7" class="py-16 text-center">
                  <UserX class="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p class="font-bold text-xs text-slate-500 dark:text-slate-400">Tidak ada pengguna ditemukan</p>
                </td>
              </tr>

              <tr 
                v-for="(u, idx) in userList" 
                :key="u.id"
                class="even:bg-[#308e87]/[0.02] dark:even:bg-[#308e87]/[0.04] hover:bg-[#308e87]/[0.06] dark:hover:bg-[#308e87]/[0.08] transition-colors"
              >
                <!-- No -->
                <td class="py-3.5 px-4 text-center font-black text-slate-400 dark:text-slate-500 border-b border-slate-100 dark:border-slate-800/40">
                  {{ (userPage - 1) * userLimit + idx + 1 }}
                </td>

                <!-- Username & Nama -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <div class="font-black text-slate-900 dark:text-white text-xs">{{ u.username }}</div>
                  <div class="text-[11px] font-bold text-slate-500 dark:text-slate-400 mt-0.5">{{ u.nama }}</div>
                  <div v-if="u.jabatan" class="text-[10px] text-slate-400 dark:text-slate-500 italic">{{ u.jabatan }}</div>
                </td>

                <!-- Role Akses -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <span class="px-2.5 py-1 rounded-full text-[10px] font-black bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] border border-[#308e87]/20">
                    {{ u.role_id }}. {{ u.role_name }}
                  </span>
                </td>

                <!-- Email & Telp -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <div class="font-semibold text-slate-700 dark:text-slate-300 text-[11px]">{{ u.email || '-' }}</div>
                  <div class="text-[10px] text-slate-400 font-mono mt-0.5">{{ u.no_telp || '-' }}</div>
                </td>

                <!-- Akses OPD -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <span v-if="!u.id_opds || u.id_opds.length === 0" class="text-[11px] font-bold text-emerald-600 dark:text-emerald-400">
                    Semua OPD (Akses Penuh)
                  </span>
                  <div v-else class="flex flex-wrap gap-1 max-w-xs">
                    <span 
                      v-for="opdId in u.id_opds" 
                      :key="opdId"
                      class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700"
                    >
                      {{ getOpdNameById(opdId) }}
                    </span>
                  </div>
                </td>

                <!-- Status Active Toggle -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40">
                  <button 
                    @click="toggleUserActive(u)"
                    class="px-2.5 py-1 rounded-full text-[10px] font-black transition-all cursor-pointer"
                    :class="u.active === 1 ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20' : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20 hover:bg-rose-500/20'"
                  >
                    {{ u.active === 1 ? 'Aktif' : 'Non-Aktif' }}
                  </button>
                </td>

                <!-- Aksi Dropdown Menu -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40 relative">
                  <button 
                    @click.stop="activeUserMenuId = (activeUserMenuId === u.id ? null : u.id)"
                    class="p-1.5 rounded-xl bg-slate-100 dark:bg-slate-800/80 hover:bg-[#308e87]/15 hover:text-[#308e87] dark:hover:text-[#3aada4] transition-all cursor-pointer shadow-sm border border-slate-200 dark:border-slate-700/60"
                    title="Menu Aksi User"
                  >
                    <MoreVertical class="w-4 h-4" />
                  </button>

                  <div 
                    v-if="activeUserMenuId === u.id"
                    @click.stop
                    class="absolute right-4 top-10 z-50 w-44 bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl p-1.5 space-y-1 animate-in fade-in zoom-in-95 duration-150 text-left"
                  >
                    <button 
                      @click="activeUserMenuId = null; openEditUserModal(u)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-blue-500/10 hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <Pencil class="w-3.5 h-3.5 text-blue-500" />
                      <span>Edit User</span>
                    </button>
                    <button 
                      @click="activeUserMenuId = null; openResetPasswordModal(u)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-amber-500/10 hover:text-amber-600 dark:hover:text-amber-400 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <KeyRound class="w-3.5 h-3.5 text-amber-500" />
                      <span>Reset Password</span>
                    </button>
                    <div class="border-t border-slate-100 dark:border-slate-800 my-1"></div>
                    <button 
                      @click="activeUserMenuId = null; confirmDeleteUser(u)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <Trash2 class="w-3.5 h-3.5 text-rose-500" />
                      <span>Hapus User</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination Bar -->
        <div class="p-4 bg-slate-50/50 dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-xs">
          <span class="text-slate-500 font-medium">
            Menampilkan {{ userList.length }} dari {{ userTotal }} total user
          </span>

          <div class="flex items-center space-x-2">
            <button 
              @click="changeUserPage(userPage - 1)"
              :disabled="userPage <= 1"
              class="px-3 py-1.5 rounded-lg bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-700 font-bold text-slate-700 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
            >
              Prev
            </button>
            <span class="font-black text-slate-800 dark:text-slate-200">Halaman {{ userPage }} dari {{ Math.ceil(userTotal / userLimit) || 1 }}</span>
            <button 
              @click="changeUserPage(userPage + 1)"
              :disabled="userPage >= Math.ceil(userTotal / userLimit)"
              class="px-3 py-1.5 rounded-lg bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-700 font-bold text-slate-700 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
            >
              Next
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- TAB 2: MANAGEMENT PERANGKAT DAERAH (ta_opd) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 'opd'" class="space-y-5">

      <!-- Action & Search Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-[10px]" />
          <input 
            v-model="searchOpdQuery"
            type="text"
            placeholder="Cari Kode atau Nama OPD..."
            class="w-full pl-10 pr-9 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-[#308e87] shadow-sm transition-all"
          />
          <button v-if="searchOpdQuery" @click="searchOpdQuery = ''" class="absolute right-3 top-[10px] text-slate-400 hover:text-[#308e87]">
            <X class="w-4 h-4" />
          </button>
        </div>

        <button 
          @click="openAddOpdModal"
          class="px-4 py-2.5 bg-[#f39159] hover:bg-[#e07f47] text-white font-black text-xs rounded-xl shadow-sm shadow-[#f39159]/30 flex items-center justify-center space-x-1.5 transition-all cursor-pointer"
        >
          <Plus class="w-4 h-4" />
          <span>Tambah OPD Baru</span>
        </button>
      </div>

      <!-- OPD Table -->
      <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-4 w-12 text-center">No</th>
                <th class="py-3.5 px-4 w-40">Kode OPD</th>
                <th class="py-3.5 px-4">Nama Perangkat Daerah</th>
                <th class="py-3.5 px-4">Kepala OPD &amp; NIP</th>
                <th class="py-3.5 px-4">Alamat &amp; Kontak</th>
                <th class="py-3.5 px-4 text-center w-28" title="Aksi"><Settings class="w-4 h-4 mx-auto" /></th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/40">
              <tr v-if="loadingOpd">
                <td colspan="6" class="py-16 text-center">
                  <Loader2 class="w-7 h-7 animate-spin mx-auto mb-2 text-[#308e87]" />
                  <span class="font-bold text-xs text-slate-400">Memuat data Perangkat Daerah...</span>
                </td>
              </tr>

              <tr v-else-if="filteredOpdList.length === 0">
                <td colspan="6" class="py-16 text-center">
                  <Building2 class="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p class="font-bold text-xs text-slate-500 dark:text-slate-400">Tidak ada Perangkat Daerah ditemukan</p>
                </td>
              </tr>

              <tr 
                v-for="(opd, idx) in filteredOpdList" 
                :key="opd.id_sub_pd"
                class="even:bg-[#308e87]/[0.02] dark:even:bg-[#308e87]/[0.04] hover:bg-[#308e87]/[0.06] dark:hover:bg-[#308e87]/[0.08] transition-colors"
              >
                <!-- No -->
                <td class="py-3.5 px-4 text-center font-black text-slate-400 dark:text-slate-500 border-b border-slate-100 dark:border-slate-800/40">
                  {{ idx + 1 }}
                </td>

                <!-- Kode OPD -->
                <td class="py-3.5 px-4 font-mono font-bold text-[#308e87] dark:text-[#3aada4] text-[11px] border-b border-slate-100 dark:border-slate-800/40">
                  <span class="px-2 py-0.5 rounded-md bg-[#308e87]/10 dark:bg-[#308e87]/15 border border-[#308e87]/20">
                    {{ opd.kode }}
                  </span>
                </td>

                <!-- Nama OPD -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <div class="font-black text-slate-900 dark:text-white text-xs">{{ opd.nama_pd }}</div>
                  <div v-if="opd.nama_pd_singkat" class="text-[10px] font-bold text-slate-400 mt-0.5">({{ opd.nama_pd_singkat }})</div>
                </td>

                <!-- Kepala OPD & NIP -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <div class="font-bold text-slate-800 dark:text-slate-200 text-[11px]">{{ opd.nama_kepala || '-' }}</div>
                  <div v-if="opd.nip_kepala" class="text-[10px] text-slate-400 font-mono mt-0.5">NIP: {{ opd.nip_kepala }}</div>
                  <div v-if="opd.jabatan_kepala" class="text-[10px] text-slate-400 italic">{{ opd.jabatan_kepala }}</div>
                </td>

                <!-- Alamat & Kontak -->
                <td class="py-3.5 px-4 border-b border-slate-100 dark:border-slate-800/40">
                  <div class="text-[11px] text-slate-700 dark:text-slate-300 truncate max-w-xs">{{ opd.alamat || '-' }}</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">{{ opd.telp || opd.email || '-' }}</div>
                </td>

                <!-- Aksi Dropdown Menu -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40 relative">
                  <button 
                    @click.stop="activeOpdMenuId = (activeOpdMenuId === opd.id_sub_pd ? null : opd.id_sub_pd)"
                    class="p-1.5 rounded-xl bg-slate-100 dark:bg-slate-800/80 hover:bg-[#308e87]/15 hover:text-[#308e87] dark:hover:text-[#3aada4] transition-all cursor-pointer shadow-sm border border-slate-200 dark:border-slate-700/60"
                    title="Menu Aksi OPD"
                  >
                    <MoreVertical class="w-4 h-4" />
                  </button>

                  <div 
                    v-if="activeOpdMenuId === opd.id_sub_pd"
                    @click.stop
                    class="absolute right-4 top-10 z-50 w-44 bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl p-1.5 space-y-1 animate-in fade-in zoom-in-95 duration-150 text-left"
                  >
                    <button 
                      @click="activeOpdMenuId = null; openEditOpdModal(opd)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-blue-500/10 hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <Pencil class="w-3.5 h-3.5 text-blue-500" />
                      <span>Edit OPD</span>
                    </button>
                    <div class="border-t border-slate-100 dark:border-slate-800 my-1"></div>
                    <button 
                      @click="activeOpdMenuId = null; confirmDeleteOpd(opd)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <Trash2 class="w-3.5 h-3.5 text-rose-500" />
                      <span>Hapus OPD</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- TAB 3: MANAGEMENT TAGGING (ref_tagging) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 'tagging'" class="space-y-5">

      <!-- Action & Search Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="relative w-full sm:w-80">
          <Search class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-[10px]" />
          <input 
            v-model="searchTaggingQuery"
            type="text"
            placeholder="Cari Tagging atau Keterangan..."
            class="w-full pl-10 pr-9 py-2.5 bg-white dark:bg-[#141d30] border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-[#308e87] shadow-sm transition-all"
          />
          <button v-if="searchTaggingQuery" @click="searchTaggingQuery = ''" class="absolute right-3 top-[10px] text-slate-400 hover:text-[#308e87]">
            <X class="w-4 h-4" />
          </button>
        </div>

        <button 
          @click="openAddTaggingModal"
          class="px-4 py-2.5 bg-purple-600 hover:bg-purple-700 text-white font-black text-xs rounded-xl shadow-sm shadow-purple-600/30 flex items-center justify-center space-x-1.5 transition-all cursor-pointer"
        >
          <Plus class="w-4 h-4" />
          <span>Tambah Tagging Baru</span>
        </button>
      </div>

      <!-- Tagging Table -->
      <div class="bg-white dark:bg-[#141d30] rounded-2xl border-2 border-slate-100 dark:border-slate-800/50 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="bg-[#308e87]/5 dark:bg-[#308e87]/10 text-[#308e87] dark:text-[#3aada4] font-black uppercase tracking-wider border-b-2 border-[#308e87]/10 dark:border-[#308e87]/15">
                <th class="py-3.5 px-4 w-12 text-center">No</th>
                <th class="py-3.5 px-4 w-20 text-center">ID</th>
                <th class="py-3.5 px-4">Nama Referensi Tagging</th>
                <th class="py-3.5 px-4">Keterangan</th>
                <th class="py-3.5 px-4 text-center w-28" title="Aksi"><Settings class="w-4 h-4 mx-auto" /></th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/40">
              <tr v-if="loadingTagging">
                <td colspan="5" class="py-16 text-center">
                  <Loader2 class="w-7 h-7 animate-spin mx-auto mb-2 text-[#308e87]" />
                  <span class="font-bold text-xs text-slate-400">Memuat data referensi tagging...</span>
                </td>
              </tr>

              <tr v-else-if="filteredTaggingList.length === 0">
                <td colspan="5" class="py-16 text-center">
                  <Tag class="w-8 h-8 mx-auto mb-2 text-slate-300 dark:text-slate-600" />
                  <p class="font-bold text-xs text-slate-500 dark:text-slate-400">Tidak ada referensi tagging ditemukan</p>
                </td>
              </tr>

              <tr 
                v-for="(t, idx) in filteredTaggingList" 
                :key="t.id"
                class="even:bg-[#308e87]/[0.02] dark:even:bg-[#308e87]/[0.04] hover:bg-[#308e87]/[0.06] dark:hover:bg-[#308e87]/[0.08] transition-colors"
              >
                <!-- No -->
                <td class="py-3.5 px-4 text-center font-black text-slate-400 dark:text-slate-500 border-b border-slate-100 dark:border-slate-800/40">
                  {{ idx + 1 }}
                </td>

                <!-- ID -->
                <td class="py-3.5 px-4 text-center font-mono font-bold text-slate-500 border-b border-slate-100 dark:border-slate-800/40">
                  <span class="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
                    {{ t.id }}
                  </span>
                </td>

                <!-- Nama Tagging -->
                <td class="py-3.5 px-4 font-black text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800/40">
                  <div class="flex items-center space-x-1.5">
                    <Tag class="w-3.5 h-3.5 text-purple-500 shrink-0" />
                    <span>{{ t.tag }}</span>
                  </div>
                </td>

                <!-- Keterangan -->
                <td class="py-3.5 px-4 text-slate-600 dark:text-slate-300 border-b border-slate-100 dark:border-slate-800/40">
                  {{ t.ket || '-' }}
                </td>

                <!-- Aksi Dropdown Menu -->
                <td class="py-3.5 px-4 text-center border-b border-slate-100 dark:border-slate-800/40 relative">
                  <button 
                    @click.stop="activeTaggingMenuId = (activeTaggingMenuId === t.id ? null : t.id)"
                    class="p-1.5 rounded-xl bg-slate-100 dark:bg-slate-800/80 hover:bg-[#308e87]/15 hover:text-[#308e87] dark:hover:text-[#3aada4] transition-all cursor-pointer shadow-sm border border-slate-200 dark:border-slate-700/60"
                    title="Menu Aksi Tagging"
                  >
                    <MoreVertical class="w-4 h-4" />
                  </button>

                  <div 
                    v-if="activeTaggingMenuId === t.id"
                    @click.stop
                    class="absolute right-4 top-10 z-50 w-44 bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl p-1.5 space-y-1 animate-in fade-in zoom-in-95 duration-150 text-left"
                  >
                    <button 
                      @click="activeTaggingMenuId = null; openEditTaggingModal(t)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-blue-500/10 hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <Pencil class="w-3.5 h-3.5 text-blue-500" />
                      <span>Edit Tagging</span>
                    </button>
                    <div class="border-t border-slate-100 dark:border-slate-800 my-1"></div>
                    <button 
                      @click="activeTaggingMenuId = null; confirmDeleteTagging(t)"
                      class="w-full px-3 py-1.5 rounded-xl text-xs font-bold text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 flex items-center space-x-2 transition-colors cursor-pointer"
                    >
                      <Trash2 class="w-3.5 h-3.5 text-rose-500" />
                      <span>Hapus Tagging</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL 1: FORM USER (TAMBAH / EDIT) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl w-full max-w-xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden my-auto">
        <div class="px-6 py-4 bg-gradient-to-r from-[#1a4845] to-[#308e87] text-white flex items-center justify-between">
          <div>
            <span class="text-[10px] font-black uppercase tracking-widest text-[#3aada4]">Pengaturan User</span>
            <h3 class="text-base font-black">{{ isEditUserMode ? 'Edit User Pengguna' : 'Tambah User Pengguna Baru' }}</h3>
          </div>
          <button @click="showUserModal = false" class="p-1 rounded-full hover:bg-white/20 text-white cursor-pointer">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="saveUser" class="p-6 space-y-4 overflow-y-auto text-xs">
          <!-- Username -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Username <span class="text-red-500">*</span></label>
            <input 
              v-model="userForm.username" 
              :readonly="isEditUserMode"
              type="text" 
              required 
              placeholder="Contoh: admin_bappeda (Tanpa spasi)" 
              class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-mono font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87] disabled:opacity-60" 
            />
          </div>

          <!-- Nama Lengkap -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Nama Lengkap <span class="text-red-500">*</span></label>
            <input v-model="userForm.nama" type="text" required placeholder="Masukkan Nama Lengkap..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
          </div>

          <!-- Email -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Alamat Email</label>
            <input v-model="userForm.email" type="email" placeholder="contoh@tegalkota.go.id" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
          </div>

          <!-- Password (Required on Create, Optional on Edit) -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">
              Password {{ isEditUserMode ? '(Kosongkan jika tidak diubah)' : '*' }}
            </label>
            <input v-model="userForm.password" type="password" :required="!isEditUserMode" placeholder="••••••••" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
          </div>

          <!-- Role Akses Combobox -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Role Hak Akses <span class="text-red-500">*</span></label>
            <select v-model.number="userForm.role_id" required class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]">
              <option v-for="(name, id) in rolesMap" :key="id" :value="Number(id)">
                {{ id }}. {{ name }}
              </option>
            </select>
          </div>

          <!-- Multi Select OPD (Only for role_id > 5) -->
          <div v-if="userForm.role_id > 5" class="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
            <label class="font-bold text-slate-700 dark:text-slate-300 block">
              Pilih Perangkat Daerah (Khusus Role > 5)
            </label>
            <div class="p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl max-h-40 overflow-y-auto space-y-1.5">
              <label v-for="opd in opdList" :key="opd.id_sub_pd" class="flex items-center space-x-2 text-xs cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-800 p-1 rounded">
                <input type="checkbox" :value="opd.id_sub_pd" v-model="userForm.id_opds" class="rounded text-[#308e87] focus:ring-[#308e87]" />
                <span class="font-mono text-[11px] text-[#308e87] font-bold">[{{ opd.kode }}]</span>
                <span class="text-slate-800 dark:text-slate-200">{{ opd.nama_pd }}</span>
              </label>
            </div>
          </div>

          <!-- No Telp & Jabatan -->
          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1">
              <label class="font-bold text-slate-700 dark:text-slate-300">No. WhatsApp/Telp</label>
              <input v-model="userForm.no_telp" type="text" placeholder="0812..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
            </div>
            <div class="space-y-1">
              <label class="font-bold text-slate-700 dark:text-slate-300">Jabatan</label>
              <input v-model="userForm.jabatan" type="text" placeholder="Jabatan..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
            </div>
          </div>

          <!-- Buttons -->
          <div class="pt-4 flex items-center justify-end space-x-2">
            <button type="button" @click="showUserModal = false" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-700 dark:text-slate-300 cursor-pointer">Batal</button>
            <button type="submit" :disabled="savingUser" class="px-5 py-2 rounded-xl bg-[#308e87] hover:bg-[#256e69] text-white font-black flex items-center space-x-1.5 cursor-pointer">
              <Loader2 v-if="savingUser" class="w-4 h-4 animate-spin" />
              <span>Simpan User</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL 2: RESET PASSWORD EMAIL CONFIRMATION -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showResetModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-md space-y-4 shadow-2xl">
        <div class="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-500 flex items-center justify-center mx-auto">
          <KeyRound class="w-6 h-6" />
        </div>
        <div class="text-center space-y-1">
          <h3 class="text-base font-black text-slate-900 dark:text-white">Reset Password Pengguna?</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Password acak (8 karakter) baru akan di-generate dan otomatis dikirimkan ke email <strong class="text-amber-600 dark:text-amber-400">{{ targetUserForReset?.email || 'user' }}</strong>.
          </p>
        </div>

        <div v-if="resetResult" class="p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-300/40 rounded-xl space-y-1 text-xs">
          <div class="font-black text-amber-800 dark:text-amber-300">Password Baru Berhasil Di-generate:</div>
          <div class="font-mono font-black text-sm text-slate-900 dark:text-white select-all bg-white dark:bg-slate-900 p-2 rounded text-center border border-amber-300">
            {{ resetResult.generated_password }}
          </div>
          <div class="text-[10px] text-slate-500 text-center mt-1">
            {{ resetResult.email_sent ? '✓ Email berhasil dikirim via SMTP' : '⚠️ Email tidak dikirim (User tidak memiliki email / SMTP error)' }}
          </div>
        </div>

        <div class="flex items-center justify-center space-x-2 pt-2">
          <button @click="showResetModal = false" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-xs cursor-pointer">
            {{ resetResult ? 'Tutup' : 'Batal' }}
          </button>
          <button v-if="!resetResult" @click="executeResetPassword" :disabled="resetting" class="px-5 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-black text-xs flex items-center space-x-1 cursor-pointer">
            <Loader2 v-if="resetting" class="w-3.5 h-3.5 animate-spin" />
            <span>Ya, Reset &amp; Kirim Email</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL 3: FORM OPD (TAMBAH / EDIT) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showOpdModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl w-full max-w-xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden my-auto">
        <div class="px-6 py-4 bg-gradient-to-r from-[#1a4845] to-[#308e87] text-white flex items-center justify-between">
          <div>
            <span class="text-[10px] font-black uppercase tracking-widest text-[#3aada4]">Master Perangkat Daerah</span>
            <h3 class="text-base font-black">{{ isEditOpdMode ? 'Edit Perangkat Daerah' : 'Tambah Perangkat Daerah Baru' }}</h3>
          </div>
          <button @click="showOpdModal = false" class="p-1 rounded-full hover:bg-white/20 text-white cursor-pointer">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="saveOpd" class="p-6 space-y-4 overflow-y-auto text-xs">
          <!-- Kode OPD & Singkatan -->
          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1">
              <label class="font-bold text-slate-700 dark:text-slate-300">Kode OPD <span class="text-red-500">*</span></label>
              <input v-model="opdForm.kode" type="text" required placeholder="Contoh: 1.01.01" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-mono font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
            </div>
            <div class="space-y-1">
              <label class="font-bold text-slate-700 dark:text-slate-300">Nama Singkat OPD</label>
              <input v-model="opdForm.nama_pd_singkat" type="text" placeholder="Contoh: Disdikbud" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
            </div>
          </div>

          <!-- Nama Lengkap OPD -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Nama Perangkat Daerah <span class="text-red-500">*</span></label>
            <input v-model="opdForm.nama_pd" type="text" required placeholder="Dinas Pendidikan dan Kebudayaan..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
          </div>

          <!-- Nama Kepala & NIP -->
          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1">
              <label class="font-bold text-slate-700 dark:text-slate-300">Nama Kepala OPD</label>
              <input v-model="opdForm.nama_kepala" type="text" placeholder="Nama Kepala..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
            </div>
            <div class="space-y-1">
              <label class="font-bold text-slate-700 dark:text-slate-300">NIP Kepala OPD</label>
              <input v-model="opdForm.nip_kepala" type="text" placeholder="NIP (Tanpa Spasi)..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-mono text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]" />
            </div>
          </div>

          <!-- Alamat -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Alamat OPD</label>
            <textarea v-model="opdForm.alamat" rows="2" placeholder="Alamat Kantor..." class="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87]"></textarea>
          </div>

          <!-- Buttons -->
          <div class="pt-4 flex items-center justify-end space-x-2">
            <button type="button" @click="showOpdModal = false" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-700 dark:text-slate-300 cursor-pointer">Batal</button>
            <button type="submit" :disabled="savingOpd" class="px-5 py-2 rounded-xl bg-[#f39159] hover:bg-[#e07f47] text-white font-black flex items-center space-x-1.5 cursor-pointer">
              <Loader2 v-if="savingOpd" class="w-4 h-4 animate-spin" />
              <span>Simpan OPD</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL 4: FORM TAGGING (TAMBAH / EDIT) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showTaggingModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl w-full max-w-lg max-h-[90vh] flex flex-col shadow-2xl overflow-hidden my-auto animate-in fade-in zoom-in-95 duration-200">
        <div class="px-6 py-4 bg-gradient-to-r from-purple-800 to-purple-600 text-white flex items-center justify-between">
          <div>
            <span class="text-[10px] font-black uppercase tracking-widest text-purple-200">Referensi Tagging</span>
            <h3 class="text-base font-black">{{ isEditTaggingMode ? 'Edit Referensi Tagging' : 'Tambah Tagging Baru' }}</h3>
          </div>
          <button @click="showTaggingModal = false" class="p-1 rounded-full hover:bg-white/20 text-white cursor-pointer">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="saveTagging" class="p-6 space-y-4 overflow-y-auto text-xs">
          <!-- Nama Tagging -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Nama Referensi Tagging <span class="text-red-500">*</span></label>
            <input v-model="taggingForm.tag" type="text" required placeholder="Contoh: Indikator Makro, SPM, SDGs..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl font-bold text-slate-900 dark:text-white focus:outline-none focus:border-purple-600" />
          </div>

          <!-- Keterangan -->
          <div class="space-y-1">
            <label class="font-bold text-slate-700 dark:text-slate-300">Keterangan / Deskripsi</label>
            <textarea v-model="taggingForm.ket" rows="3" placeholder="Keterangan opsional mengenai referensi tagging..." class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-purple-600"></textarea>
          </div>

          <!-- Buttons -->
          <div class="pt-4 flex items-center justify-end space-x-2">
            <button type="button" @click="showTaggingModal = false" class="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-700 dark:text-slate-300 cursor-pointer">Batal</button>
            <button type="submit" :disabled="savingTagging" class="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-black flex items-center space-x-1.5 shadow-md shadow-purple-600/30 cursor-pointer">
              <Loader2 v-if="savingTagging" class="w-4 h-4 animate-spin" />
              <Save v-else class="w-4 h-4" />
              <span>{{ isEditTaggingMode ? 'Simpan Perubahan' : 'Tambah Tagging' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MODAL CONFIRM DELETE (USER / OPD / TAGGING) -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div class="bg-white dark:bg-[#141d30] border-2 border-slate-200 dark:border-slate-800 rounded-3xl p-6 w-full max-w-md space-y-4 shadow-2xl">
        <div class="w-12 h-12 rounded-2xl bg-rose-500/10 text-rose-500 flex items-center justify-center mx-auto">
          <Trash2 class="w-6 h-6" />
        </div>
        <div class="text-center space-y-1">
          <h3 class="text-base font-black text-slate-900 dark:text-white">Konfirmasi Hapus Data</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Apakah Anda yakin ingin menghapus data <strong class="text-slate-800 dark:text-slate-200">"{{ deleteItemTitle }}"</strong>? Data yang dihapus tidak dapat dikembalikan.
          </p>
        </div>
        <div class="flex items-center justify-center space-x-2 pt-2">
          <button @click="showDeleteModal = false" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-xs cursor-pointer">
            Batal
          </button>
          <button @click="executeDelete" :disabled="deleting" class="px-5 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-black text-xs flex items-center space-x-1 cursor-pointer">
            <Loader2 v-if="deleting" class="w-3.5 h-3.5 animate-spin" />
            <span>Ya, Hapus Data</span>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { 
  UserCog, 
  Building2, 
  Tag,
  Search, 
  Plus, 
  Pencil, 
  Trash2, 
  KeyRound, 
  X, 
  CheckCircle, 
  AlertCircle, 
  Loader2, 
  UserX,
  Save,
  Settings,
  MoreVertical
} from 'lucide-vue-next'

const activeTab = ref('user')

// Toast State
const toast = ref({ show: false, message: '', type: 'success' })
const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 4000)
}

// Roles Mapping
const rolesMap = ref({
  1: "User Admin",
  2: "Admin Bidang",
  3: "Supervisor",
  4: "Auditor",
  5: "Verifikator",
  6: "Kepala OPD",
  7: "Kepala Bidang OPD",
  8: "Kepala Sub Bidang OPD",
  9: "Staff OPD"
})

// ════════════════════════════════════════════════════════════════════
// 1. PENGATURAN USER STATES & HANDLERS
// ════════════════════════════════════════════════════════════════════

const userList = ref([])
const userTotal = ref(0)
const userPage = ref(1)
const userLimit = ref(50)
const loadingUsers = ref(false)
const searchUserQuery = ref('')
const selectedRoleFilter = ref(null)

const showUserModal = ref(false)
const isEditUserMode = ref(false)
const savingUser = ref(false)
const userForm = ref({
  id: '',
  username: '',
  nama: '',
  email: '',
  password: '',
  role_id: 9,
  id_opds: [],
  no_telp: '',
  jabatan: '',
  active: 1
})

const showResetModal = ref(false)
const targetUserForReset = ref(null)
const resetting = ref(false)
const resetResult = ref(null)

let debounceTimer = null
const debouncedFetchUsers = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    userPage.value = 1
    fetchUsers()
  }, 350)
}

const clearUserSearch = () => {
  searchUserQuery.value = ''
  userPage.value = 1
  fetchUsers()
}

const fetchUsers = async () => {
  loadingUsers.value = true
  try {
    const params = {
      page: userPage.value,
      limit: userLimit.value
    }
    if (searchUserQuery.value.trim()) params.q = searchUserQuery.value.trim()
    if (selectedRoleFilter.value !== null) params.role_id = selectedRoleFilter.value

    const res = await axios.get('/api/v1/pengaturan/users', { params })
    userList.value = res.data.data
    userTotal.value = res.data.total
  } catch (err) {
    showToast('Gagal memuat data pengguna', 'error')
  } finally {
    loadingUsers.value = false
  }
}

const changeUserPage = (p) => {
  userPage.value = p
  fetchUsers()
}

const toggleUserActive = async (u) => {
  const newStatus = u.active === 1 ? 0 : 1
  try {
    await axios.put(`/api/v1/pengaturan/users/${u.id}/status`, { active: newStatus })
    u.active = newStatus
    showToast(`Status user '${u.username}' berhasil diubah`)
  } catch (err) {
    showToast('Gagal mengubah status user', 'error')
  }
}

const openAddUserModal = () => {
  isEditUserMode.value = false
  userForm.value = {
    id: '',
    username: '',
    nama: '',
    email: '',
    password: '',
    role_id: 9,
    id_opds: [],
    no_telp: '',
    jabatan: '',
    active: 1
  }
  showUserModal.value = true
}

const openEditUserModal = (u) => {
  isEditUserMode.value = true
  userForm.value = {
    id: u.id,
    username: u.username,
    nama: u.nama || '',
    email: u.email || '',
    password: '',
    role_id: u.role_id,
    id_opds: u.id_opds ? [...u.id_opds] : [],
    no_telp: u.no_telp || '',
    jabatan: u.jabatan || '',
    active: u.active ?? 1
  }
  showUserModal.value = true
}

const saveUser = async () => {
  savingUser.value = true
  try {
    if (isEditUserMode.value) {
      await axios.put(`/api/v1/pengaturan/users/${userForm.value.id}`, {
        nama: userForm.value.nama,
        email: userForm.value.email,
        password: userForm.value.password || undefined,
        role_id: userForm.value.role_id,
        id_opds: userForm.value.id_opds,
        no_telp: userForm.value.no_telp,
        jabatan: userForm.value.jabatan
      })
      showToast('User berhasil diperbarui')
    } else {
      await axios.post('/api/v1/pengaturan/users', {
        username: userForm.value.username,
        nama: userForm.value.nama,
        email: userForm.value.email,
        password: userForm.value.password,
        role_id: userForm.value.role_id,
        id_opds: userForm.value.id_opds,
        no_telp: userForm.value.no_telp,
        jabatan: userForm.value.jabatan
      })
      showToast('User baru berhasil ditambahkan')
    }
    showUserModal.value = false
    fetchUsers()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal menyimpan user', 'error')
  } finally {
    savingUser.value = false
  }
}

const openResetPasswordModal = (u) => {
  targetUserForReset.value = u
  resetResult.value = null
  showResetModal.value = true
}

const executeResetPassword = async () => {
  if (!targetUserForReset.value) return
  resetting.value = true
  try {
    const res = await axios.put(`/api/v1/pengaturan/users/${targetUserForReset.value.id}/reset-password`)
    resetResult.value = res.data
    showToast(`Password user '${targetUserForReset.value.username}' berhasil di-reset`)
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal reset password', 'error')
  } finally {
    resetting.value = false
  }
}

// ════════════════════════════════════════════════════════════════════
// 2. PERANGKAT DAERAH (OPD) STATES & HANDLERS
// ════════════════════════════════════════════════════════════════════

const opdList = ref([])
const loadingOpd = ref(false)
const searchOpdQuery = ref('')

const showOpdModal = ref(false)
const isEditOpdMode = ref(false)
const savingOpd = ref(false)
const opdForm = ref({
  id_sub_pd: null,
  kode: '',
  nama_pd: '',
  nama_pd_singkat: '',
  nip_kepala: '',
  nama_kepala: '',
  jabatan_kepala: '',
  alamat: '',
  telp: '',
  email: ''
})

const filteredOpdList = computed(() => {
  if (!searchOpdQuery.value.trim()) return opdList.value
  const q = searchOpdQuery.value.toLowerCase().trim()
  return opdList.value.filter(o => 
    (o.kode && o.kode.toLowerCase().includes(q)) ||
    (o.nama_pd && o.nama_pd.toLowerCase().includes(q)) ||
    (o.nama_pd_singkat && o.nama_pd_singkat.toLowerCase().includes(q)) ||
    (o.nama_kepala && o.nama_kepala.toLowerCase().includes(q))
  )
})

const fetchOpd = async () => {
  loadingOpd.value = true
  try {
    const res = await axios.get('/api/v1/pengaturan/opd')
    opdList.value = res.data
  } catch (err) {
    showToast('Gagal memuat data Perangkat Daerah', 'error')
  } finally {
    loadingOpd.value = false
  }
}

const getOpdNameById = (id_sub_pd) => {
  const found = opdList.value.find(o => o.id_sub_pd === id_sub_pd)
  return found ? found.nama_pd_singkat || found.nama_pd : `OPD ${id_sub_pd}`
}

const openAddOpdModal = () => {
  isEditOpdMode.value = false
  opdForm.value = {
    id_sub_pd: null,
    kode: '',
    nama_pd: '',
    nama_pd_singkat: '',
    nip_kepala: '',
    nama_kepala: '',
    jabatan_kepala: '',
    alamat: '',
    telp: '',
    email: ''
  }
  showOpdModal.value = true
}

const openEditOpdModal = (opd) => {
  isEditOpdMode.value = true
  opdForm.value = { ...opd }
  showOpdModal.value = true
}

const saveOpd = async () => {
  savingOpd.value = true
  try {
    if (isEditOpdMode.value) {
      await axios.put(`/api/v1/pengaturan/opd/${opdForm.value.id_sub_pd}`, opdForm.value)
      showToast('Data Perangkat Daerah berhasil diperbarui')
    } else {
      await axios.post('/api/v1/pengaturan/opd', opdForm.value)
      showToast('Perangkat Daerah baru berhasil ditambahkan')
    }
    showOpdModal.value = false
    fetchOpd()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal menyimpan OPD', 'error')
  } finally {
    savingOpd.value = false
  }
}

// ════════════════════════════════════════════════════════════════════
// 3. TAGGING STATES & HANDLERS (ref_tagging)
// ════════════════════════════════════════════════════════════════════

const taggingList = ref([])
const loadingTagging = ref(false)
const searchTaggingQuery = ref('')

const showTaggingModal = ref(false)
const isEditTaggingMode = ref(false)
const savingTagging = ref(false)
const editingTaggingId = ref(null)
const taggingForm = ref({
  tag: '',
  ket: ''
})

const filteredTaggingList = computed(() => {
  if (!searchTaggingQuery.value.trim()) return taggingList.value
  const q = searchTaggingQuery.value.toLowerCase().trim()
  return taggingList.value.filter(t => 
    (t.tag && t.tag.toLowerCase().includes(q)) ||
    (t.ket && t.ket.toLowerCase().includes(q))
  )
})

const fetchTagging = async () => {
  loadingTagging.value = true
  try {
    const res = await axios.get('/api/v1/pengaturan/tagging')
    taggingList.value = res.data
  } catch (err) {
    showToast('Gagal memuat data referensi tagging', 'error')
  } finally {
    loadingTagging.value = false
  }
}

const openAddTaggingModal = () => {
  isEditTaggingMode.value = false
  editingTaggingId.value = null
  taggingForm.value = { tag: '', ket: '' }
  showTaggingModal.value = true
}

const openEditTaggingModal = (t) => {
  isEditTaggingMode.value = true
  editingTaggingId.value = t.id
  taggingForm.value = {
    tag: t.tag || '',
    ket: t.ket || ''
  }
  showTaggingModal.value = true
}

const saveTagging = async () => {
  savingTagging.value = true
  try {
    if (isEditTaggingMode.value) {
      await axios.put(`/api/v1/pengaturan/tagging/${editingTaggingId.value}`, taggingForm.value)
      showToast('Referensi Tagging berhasil diperbarui')
    } else {
      await axios.post('/api/v1/pengaturan/tagging', taggingForm.value)
      showToast('Referensi Tagging baru berhasil ditambahkan')
    }
    showTaggingModal.value = false
    fetchTagging()
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal menyimpan Tagging', 'error')
  } finally {
    savingTagging.value = false
  }
}

// ════════════════════════════════════════════════════════════════════
// 4. SHARED DELETE CONFIRMATION HANDLERS
// ════════════════════════════════════════════════════════════════════

const showDeleteModal = ref(false)
const deleteTargetType = ref('') // 'user' | 'opd' | 'tagging'
const deleteTargetId = ref(null)
const deleteItemTitle = ref('')
const deleting = ref(false)

const confirmDeleteUser = (u) => {
  deleteTargetType.value = 'user'
  deleteTargetId.value = u.id
  deleteItemTitle.value = `User: ${u.username} (${u.nama})`
  showDeleteModal.value = true
}

const confirmDeleteOpd = (opd) => {
  deleteTargetType.value = 'opd'
  deleteTargetId.value = opd.id_sub_pd
  deleteItemTitle.value = `OPD: ${opd.nama_pd}`
  showDeleteModal.value = true
}

const confirmDeleteTagging = (t) => {
  deleteTargetType.value = 'tagging'
  deleteTargetId.value = t.id
  deleteItemTitle.value = `Tagging: ${t.tag}`
  showDeleteModal.value = true
}

const executeDelete = async () => {
  deleting.value = true
  try {
    if (deleteTargetType.value === 'user') {
      await axios.delete(`/api/v1/pengaturan/users/${deleteTargetId.value}`)
      showToast('User berhasil dihapus')
      fetchUsers()
    } else if (deleteTargetType.value === 'opd') {
      await axios.delete(`/api/v1/pengaturan/opd/${deleteTargetId.value}`)
      showToast('Perangkat Daerah berhasil dihapus')
      fetchOpd()
    } else if (deleteTargetType.value === 'tagging') {
      await axios.delete(`/api/v1/pengaturan/tagging/${deleteTargetId.value}`)
      showToast('Referensi Tagging berhasil dihapus')
      fetchTagging()
    }
    showDeleteModal.value = false
  } catch (err) {
    showToast(err.response?.data?.detail || 'Gagal menghapus data', 'error')
  } finally {
    deleting.value = false
  }
}

const activeUserMenuId = ref(null)
const activeOpdMenuId = ref(null)
const activeTaggingMenuId = ref(null)

const closeAllMenus = () => {
  activeUserMenuId.value = null
  activeOpdMenuId.value = null
  activeTaggingMenuId.value = null
}

onMounted(() => {
  fetchUsers()
  fetchOpd()
  fetchTagging()
  window.addEventListener('click', closeAllMenus)
})

onUnmounted(() => {
  window.removeEventListener('click', closeAllMenus)
})
</script>
