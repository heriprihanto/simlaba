<template>
  <div class="h-full flex flex-col bg-slate-50 dark:bg-[#0f172a] text-slate-900 dark:text-slate-100 overflow-hidden select-none">
    <div class="bg-white dark:bg-[#141d30] border-b border-slate-200 dark:border-slate-800 px-5 py-3.5 flex items-center space-x-3 shrink-0">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-slate-700 to-slate-900 text-white flex items-center justify-center shadow-md">
        <Settings class="w-5 h-5" />
      </div>
      <div>
        <h2 class="text-sm font-black text-slate-900 dark:text-white">Pengaturan Sistem &amp; Pengguna</h2>
        <p class="text-[11px] text-slate-500">Konfigurasi Pengguna SSO, Role Akses, dan Master Perangkat Daerah</p>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-teal-500/10 text-teal-600 flex items-center justify-center">
              <UserCog class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-xs font-black">Manajemen Pengguna &amp; Hak Akses</h3>
              <p class="text-[11px] text-slate-400">Total 124 Akun Terdaftar</p>
            </div>
          </div>
          <p class="text-xs text-slate-500">Kelola kredensial SSO, penugasan OPD, dan penetapan role pengguna.</p>
        </div>

        <div class="bg-white dark:bg-[#141d30] border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-600 flex items-center justify-center">
              <Building2 class="w-4 h-4" />
            </div>
            <div>
              <h3 class="text-xs font-black">Master Perangkat Daerah (OPD)</h3>
              <p class="text-[11px] text-slate-400">34 Dinas &amp; Badan Aktif</p>
            </div>
          </div>
          <p class="text-xs text-slate-500">Pengaturan kode urusan, nomenklatur OPD, dan kepala perangkat daerah.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Settings, UserCog, Building2 } from 'lucide-vue-next'
</script>
