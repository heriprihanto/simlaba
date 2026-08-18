<template>
  <div class="min-h-screen bg-gradient-to-br from-[#F8F8F4] via-[#f0f4f0] to-[#e8efe8] dark:from-[#0c1222] dark:via-[#111827] dark:to-[#0c1222] flex transition-colors duration-300">

    <!-- Left Panel (Desktop) -->
    <div class="hidden lg:flex lg:w-[48%] relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-[#1a4845] via-[#245f5a] to-[#308e87]"></div>
      
      <!-- Pattern -->
      <div class="absolute inset-0 opacity-[0.06]" style="background-image: url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;1&quot;%3E%3Cpath d=&quot;M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')"></div>
      
      <!-- Glowing blobs -->
      <div class="absolute top-20 -left-20 w-96 h-96 bg-[#3aada4]/25 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-10 right-0 w-72 h-72 bg-[#f39159]/20 rounded-full blur-[100px]"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-white/5 rounded-full blur-[80px]"></div>
      
      <!-- Content -->
      <div class="relative z-10 flex flex-col justify-between p-12 text-white w-full">
        <div>
          <div class="w-14 h-14 rounded-2xl bg-white/15 backdrop-blur-md flex items-center justify-center text-white font-black text-2xl border border-white/20 shadow-lg shadow-white/5">
            S
          </div>
        </div>

        <div class="space-y-8">
          <div>
            <p class="text-xs font-black tracking-[0.3em] uppercase text-[#3aada4]">Pemerintah Kota Tegal</p>
            <h2 class="text-4xl font-black tracking-tight leading-[1.1] mt-3">
              Sistem Informasi<br/>Laporan Perkembangan<br/>Pembangunan
            </h2>
          </div>

          <div class="flex items-center space-x-4">
            <div class="w-16 h-1 rounded-full bg-gradient-to-r from-[#f39159] to-[#f8b088]"></div>
            <p class="text-sm text-white/70 font-semibold">SIMLABA — Monev Realtime</p>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-4 pt-2">
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/15 hover:bg-white/15 transition-colors">
              <p class="text-3xl font-black text-[#3aada4]">94</p>
              <p class="text-xs text-white/60 font-bold mt-1">OPD Aktif</p>
            </div>
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/15 hover:bg-white/15 transition-colors">
              <p class="text-3xl font-black text-[#f39159]">323</p>
              <p class="text-xs text-white/60 font-bold mt-1">Personel</p>
            </div>
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/15 hover:bg-white/15 transition-colors">
              <p class="text-3xl font-black text-emerald-400">75%</p>
              <p class="text-xs text-white/60 font-bold mt-1">Realisasi</p>
            </div>
          </div>
        </div>

        <div class="flex items-center space-x-3">
          <div class="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50"></div>
          <p class="text-xs text-white/40 font-semibold">&copy; 2026 Bapperida Kota Tegal • SIMLABA v1.0</p>
        </div>
      </div>
    </div>

    <!-- Right Form Panel -->
    <div class="flex-1 flex items-center justify-center p-6 sm:p-12 relative">
      <div class="absolute top-0 right-0 w-80 h-80 bg-[#308e87]/10 rounded-full blur-[130px]"></div>
      <div class="absolute bottom-0 left-0 w-80 h-80 bg-[#f39159]/8 rounded-full blur-[130px]"></div>

      <div class="w-full max-w-md relative z-10">
        
        <!-- Mobile Logo -->
        <div class="lg:hidden text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-[#308e87] via-[#3aada4] to-[#245f5a] text-white font-black text-3xl shadow-xl shadow-[#308e87]/25 mb-4">
            S
          </div>
          <h1 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">SIMLABA</h1>
          <p class="text-xs text-[#308e87] dark:text-[#3aada4] mt-1 font-bold">Kota Tegal • 2026</p>
        </div>

        <!-- Card -->
        <div class="bg-white dark:bg-[#141d30] rounded-3xl shadow-2xl shadow-slate-300/50 dark:shadow-black/40 border border-slate-200 dark:border-slate-700/50 p-8">
          
          <div class="mb-7">
            <h2 class="text-xl font-black text-slate-900 dark:text-white tracking-tight">Masuk ke SIMLABA</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium">Gunakan akun SSO Pemerintah Kota Tegal</p>
          </div>

          <!-- Error -->
          <div v-if="authStore.error" class="mb-5 p-3.5 rounded-xl bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 text-xs font-semibold flex items-center space-x-2">
            <AlertCircle class="w-4 h-4 shrink-0" />
            <span>{{ authStore.error }}</span>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider">Username SSO</label>
              <div class="relative">
                <User class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-3" />
                <input 
                  v-model="username"
                  @input="username = username.replace(/\s+/g, '')"
                  @keydown.space.prevent
                  type="text" 
                  required
                  placeholder="Masukkan username (tanpa spasi)"
                  class="w-full pl-10 pr-4 py-2.5 bg-[#308e87]/5 dark:bg-[#308e87]/10 border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 text-sm focus:outline-none focus:border-[#308e87] focus:ring-3 focus:ring-[#308e87]/15 transition-all"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider">Password</label>
              <div class="relative">
                <Lock class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-3" />
                <input 
                  v-model="password"
                  type="password" 
                  required
                  placeholder="Masukkan password"
                  class="w-full pl-10 pr-4 py-2.5 bg-[#308e87]/5 dark:bg-[#308e87]/10 border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 text-sm focus:outline-none focus:border-[#308e87] focus:ring-3 focus:ring-[#308e87]/15 transition-all"
                />
              </div>
            </div>

            <!-- Kode Keamanan / Captcha Field -->
            <div class="pt-1">
              <label class="block text-xs font-bold text-[#308e87] dark:text-[#3aada4] mb-1.5 uppercase tracking-wider">
                Kode Keamanan (Captcha)
              </label>
              
              <div class="flex items-center space-x-2.5 mb-2">
                <!-- Visual Stylized Captcha Canvas Box -->
                <div class="flex-1 bg-gradient-to-r from-slate-900 via-[#141d30] to-slate-900 border-2 border-[#308e87]/30 rounded-xl py-2 px-4 flex items-center justify-between select-none relative overflow-hidden shadow-inner">
                  <!-- Background noise lines -->
                  <div class="absolute inset-0 opacity-20 pointer-events-none" style="background-image: repeating-linear-gradient(45deg, #308e87 0, #308e87 2px, transparent 0, transparent 8px)"></div>
                  
                  <!-- Captcha Characters with random colors & rotations -->
                  <div class="flex items-center justify-around w-full relative z-10 font-mono tracking-widest text-lg font-black italic">
                    <span 
                      v-for="(char, idx) in captchaCode.split('')" 
                      :key="idx"
                      class="inline-block transform drop-shadow-md transition-transform"
                      :style="{
                        transform: `rotate(${(idx % 2 === 0 ? 1 : -1) * (10 + (idx * 5))}deg) translateY(${(idx % 2 === 0 ? -2 : 2)}px)`,
                        color: ['#308e87', '#3aada4', '#f39159', '#38bdf8', '#a78bfa', '#f43f5e'][idx % 6]
                      }"
                    >
                      {{ char }}
                    </span>
                  </div>
                </div>

                <!-- Refresh Captcha Button -->
                <button 
                  type="button"
                  @click="generateCaptcha"
                  class="p-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-[#308e87]/15 text-slate-600 dark:text-slate-300 hover:text-[#308e87] dark:hover:text-[#3aada4] rounded-xl border border-slate-200 dark:border-slate-700 transition-colors cursor-pointer"
                  title="Acak Kode Captcha Baru"
                >
                  <RotateCw class="w-4 h-4" />
                </button>
              </div>

              <!-- Captcha Input -->
              <div class="relative">
                <ShieldCheck class="w-4 h-4 text-[#308e87]/40 absolute left-3.5 top-3" />
                <input 
                  v-model="captchaInput"
                  type="text" 
                  required
                  placeholder="Ketik 5 karakter captcha"
                  class="w-full pl-10 pr-4 py-2.5 bg-[#308e87]/5 dark:bg-[#308e87]/10 border-2 border-[#308e87]/15 dark:border-[#308e87]/20 rounded-xl text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 text-sm font-mono uppercase tracking-widest focus:outline-none focus:border-[#308e87] focus:ring-3 focus:ring-[#308e87]/15 transition-all"
                />
              </div>

              <p v-if="captchaError" class="text-xs text-rose-500 font-bold mt-1.5 flex items-center space-x-1">
                <AlertCircle class="w-3.5 h-3.5 shrink-0" />
                <span>{{ captchaError }}</span>
              </p>
            </div>

            <button 
              type="submit"
              :disabled="authStore.loading"
              class="w-full py-3 bg-gradient-to-r from-[#308e87] via-[#3aada4] to-[#308e87] hover:from-[#267a74] hover:via-[#308e87] hover:to-[#267a74] text-white font-black text-sm rounded-xl shadow-lg shadow-[#308e87]/30 hover:shadow-xl hover:shadow-[#308e87]/40 transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 active:scale-[0.98] mt-2"
            >
              <Loader2 v-if="authStore.loading" class="w-4 h-4 animate-spin" />
              <span>{{ authStore.loading ? 'Memproses...' : 'Masuk Aplikasi' }}</span>
              <ArrowRight v-if="!authStore.loading" class="w-4 h-4" />
            </button>
          </form>
        </div>

        <p class="text-center text-xs text-slate-400 dark:text-slate-500 mt-6 font-medium">Pemerintah Kota Tegal &copy; 2026</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { User, Lock, AlertCircle, Loader2, ArrowRight, ShieldCheck, RotateCw } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const captchaCode = ref('')
const captchaInput = ref('')
const captchaError = ref('')

const generateCaptcha = () => {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let result = ''
  for (let i = 0; i < 5; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  captchaCode.value = result
  captchaInput.value = ''
  captchaError.value = ''
}

const handleLogin = async () => {
  if (!captchaInput.value.trim()) {
    captchaError.value = 'Silakan masukkan kode captcha.'
    return
  }
  if (captchaInput.value.trim().toUpperCase() !== captchaCode.value.toUpperCase()) {
    captchaError.value = 'Kode Captcha tidak sesuai. Silakan coba lagi.'
    generateCaptcha()
    return
  }

  captchaError.value = ''
  const success = await authStore.login(username.value, password.value)
  if (!success) {
    generateCaptcha()
  } else {
    router.push('/')
  }
}

onMounted(() => {
  generateCaptcha()
})
</script>
