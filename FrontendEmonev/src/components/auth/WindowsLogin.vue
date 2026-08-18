<template>
  <div class="fixed inset-0 z-[5000] overflow-hidden select-none bg-[#071322] text-white font-sans">
    
    <!-- Dynamic Windows 10 Wallpaper Background with Acrylic Blur -->
    <div 
      class="absolute inset-0 bg-cover bg-center transition-all duration-700 transform"
      :class="isEnteringPassword ? 'scale-105 blur-lg brightness-50' : 'scale-100 blur-0 brightness-90'"
      style="background-image: linear-gradient(135deg, rgba(7,19,34,0.8) 0%, rgba(11,31,58,0.85) 100%), url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?q=80&w=1920&auto=format&fit=crop');"
    ></div>

    <!-- Background Accent Glows -->
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-[#308e87]/20 rounded-full blur-[140px] pointer-events-none"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[#38bdf8]/15 rounded-full blur-[140px] pointer-events-none"></div>

    <!-- ==================== STAGE 1: WINDOWS 10 LOCK SCREEN ==================== -->
    <div 
      v-if="!isEnteringPassword"
      @click="showSignInForm"
      class="relative z-10 w-full h-full flex flex-col justify-between p-8 sm:p-12 cursor-pointer animate-in fade-in duration-300"
    >
      <!-- Top Status Header -->
      <div class="flex justify-between items-center text-xs font-semibold text-white/80">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-[#308e87] to-[#1e5955] text-white font-black text-xs flex items-center justify-center shadow-md">
            E
          </div>
          <div>
            <span class="font-black text-sm tracking-wide text-white">EMONEV OS</span>
            <span class="text-[11px] text-slate-300 ml-2 font-medium">Pemerintah Kota Tegal</span>
          </div>
        </div>
        <div class="flex items-center space-x-3 text-slate-300">
          <Wifi class="w-4 h-4 text-emerald-400" />
          <BatteryCharging class="w-4 h-4 text-emerald-400" />
        </div>
      </div>

      <!-- Center / Lower Left: Big Windows 10 Digital Clock -->
      <div class="mb-12 space-y-1">
        <h1 class="text-7xl sm:text-8xl font-thin tracking-tighter text-white drop-shadow-lg">
          {{ currentTime }}
        </h1>
        <p class="text-xl sm:text-2xl font-light text-slate-200 drop-shadow">
          {{ currentDateLong }}
        </p>
      </div>

      <!-- Bottom Prompt -->
      <div class="flex items-center justify-between text-xs text-white/70">
        <div class="flex items-center space-x-2 animate-bounce">
          <ChevronUp class="w-4 h-4 text-[#38bdf8]" />
          <span class="font-bold text-slate-200">Klik di mana saja atau tekan sembarang tombol untuk masuk</span>
        </div>
        <span class="text-[11px] text-white/40">SIMLABA &amp; EMONEV Kota Tegal &copy; 2026</span>
      </div>
    </div>

    <!-- ==================== STAGE 2: WINDOWS 10 SIGN-IN FORM (SAMA PERSIS METODE SIMLABA) ==================== -->
    <div 
      v-else
      class="relative z-10 w-full h-full flex flex-col items-center justify-center p-4 sm:p-6 animate-in fade-in zoom-in-95 duration-300 overflow-y-auto"
    >
      <!-- Back to Lock Screen button -->
      <button 
        @click="isEnteringPassword = false"
        class="absolute top-6 left-6 p-2.5 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
        title="Kembali ke layar kunci"
      >
        <ArrowLeft class="w-5 h-5" />
      </button>

      <!-- Center Sign-In Card (Windows 10 Acrylic Form) -->
      <div class="w-full max-w-md bg-[#0c192c]/90 dark:bg-[#09111e]/95 backdrop-blur-2xl rounded-3xl border border-slate-700/80 shadow-2xl p-7 sm:p-8 space-y-5">
        
        <!-- Header & Avatar -->
        <div class="flex items-center space-x-4 pb-2 border-b border-slate-700/60">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#308e87] via-[#3aada4] to-[#1e5955] p-0.5 shadow-lg flex items-center justify-center shrink-0">
            <div class="w-full h-full rounded-2xl bg-[#0f172a] flex items-center justify-center text-white">
              <User class="w-7 h-7 text-[#38bdf8]" />
            </div>
          </div>
          <div>
            <h2 class="text-base font-black text-white tracking-tight">Masuk ke EMONEV OS</h2>
            <p class="text-xs text-slate-400 font-medium">Gunakan akun SSO Pemerintah Kota Tegal</p>
          </div>
        </div>

        <!-- Error Banner (Jika ada kegagalan otentikasi) -->
        <div v-if="authStore.error" class="p-3 rounded-xl bg-red-500/15 border border-red-500/30 text-red-300 text-xs font-semibold flex items-center space-x-2">
          <AlertCircle class="w-4 h-4 shrink-0 text-red-400" />
          <span>{{ authStore.error }}</span>
        </div>

        <!-- Form Login (Metode Sama dengan Frontend Simlaba) -->
        <form @submit.prevent="handleLogin" class="space-y-3.5">
          
          <!-- Field 1: Username SSO -->
          <div>
            <label class="block text-xs font-bold text-[#38bdf8] mb-1 uppercase tracking-wider">Username SSO</label>
            <div class="relative">
              <User class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="username"
                @input="username = username.replace(/\s+/g, '')"
                @keydown.space.prevent
                type="text" 
                required
                placeholder="Masukkan username (tanpa spasi)"
                class="w-full pl-10 pr-4 py-2.5 bg-white/10 border border-white/20 rounded-xl text-white placeholder-slate-400 text-xs focus:outline-none focus:border-[#38bdf8] focus:ring-2 focus:ring-[#38bdf8]/30 transition-all font-medium"
              />
            </div>
          </div>

          <!-- Field 2: Password -->
          <div>
            <label class="block text-xs font-bold text-[#38bdf8] mb-1 uppercase tracking-wider">Password</label>
            <div class="relative">
              <Lock class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="Masukkan password"
                class="w-full pl-10 pr-10 py-2.5 bg-white/10 border border-white/20 rounded-xl text-white placeholder-slate-400 text-xs focus:outline-none focus:border-[#38bdf8] focus:ring-2 focus:ring-[#38bdf8]/30 transition-all font-medium"
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-2.5 text-slate-400 hover:text-white"
                tabindex="-1"
              >
                <Eye v-if="!showPassword" class="w-4 h-4" />
                <EyeOff v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Field 3: Kode Keamanan (Captcha) Sesuai Standar SIMLABA -->
          <div class="pt-0.5">
            <label class="block text-xs font-bold text-[#38bdf8] mb-1 uppercase tracking-wider">
              Kode Keamanan (Captcha)
            </label>
            
            <div class="flex items-center space-x-2 mb-2">
              <!-- Visual Stylized Captcha Canvas Box (Sama dengan Simlaba) -->
              <div class="flex-1 bg-gradient-to-r from-slate-900 via-[#101b30] to-slate-900 border border-[#308e87]/40 rounded-xl py-2 px-3 flex items-center justify-between select-none relative overflow-hidden shadow-inner">
                <!-- Background noise lines -->
                <div class="absolute inset-0 opacity-25 pointer-events-none" style="background-image: repeating-linear-gradient(45deg, #308e87 0, #308e87 2px, transparent 0, transparent 8px)"></div>
                
                <!-- Captcha Characters with random colors & rotations -->
                <div class="flex items-center justify-around w-full relative z-10 font-mono tracking-widest text-base font-black italic">
                  <span 
                    v-for="(char, idx) in captchaCode.split('')" 
                    :key="idx"
                    class="inline-block transform drop-shadow-md transition-transform"
                    :style="{
                      transform: `rotate(${(idx % 2 === 0 ? 1 : -1) * (8 + (idx * 4))}deg) translateY(${(idx % 2 === 0 ? -2 : 2)}px)`,
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
                class="p-2.5 bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white rounded-xl border border-white/20 transition-colors cursor-pointer"
                title="Acak Kode Captcha Baru"
              >
                <RotateCw class="w-4 h-4" />
              </button>
            </div>

            <!-- Captcha Input -->
            <div class="relative">
              <ShieldCheck class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="captchaInput"
                type="text" 
                required
                placeholder="Ketik 5 karakter captcha di atas"
                class="w-full pl-10 pr-4 py-2.5 bg-white/10 border border-white/20 rounded-xl text-white placeholder-slate-400 text-xs font-mono uppercase tracking-widest focus:outline-none focus:border-[#38bdf8] focus:ring-2 focus:ring-[#38bdf8]/30 transition-all"
              />
            </div>

            <p v-if="captchaError" class="text-xs text-rose-400 font-bold mt-1.5 flex items-center space-x-1">
              <AlertCircle class="w-3.5 h-3.5 shrink-0" />
              <span>{{ captchaError }}</span>
            </p>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            :disabled="authStore.loading"
            class="w-full py-3 bg-gradient-to-r from-[#308e87] via-[#3aada4] to-[#308e87] hover:from-[#267a74] hover:via-[#308e87] hover:to-[#267a74] text-white font-black text-xs rounded-xl shadow-lg shadow-[#308e87]/30 hover:shadow-xl hover:shadow-[#308e87]/40 transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 active:scale-[0.98] mt-2"
          >
            <Loader2 v-if="authStore.loading" class="w-4 h-4 animate-spin" />
            <span>{{ authStore.loading ? 'Memproses Masuk...' : 'Masuk ke Sistem' }}</span>
            <ArrowRight v-if="!authStore.loading" class="w-4 h-4" />
          </button>

          <!-- Quick Demo Logins Bar -->
          <div class="pt-2 border-t border-slate-700/60 flex items-center justify-between text-[11px] text-slate-400">
            <span>Login Cepat:</span>
            <div class="flex items-center space-x-1.5">
              <button 
                type="button" 
                @click="fillCredentials('admin', 'admin123')"
                class="px-2 py-0.5 rounded bg-white/10 hover:bg-white/20 text-slate-200 font-bold"
              >
                Admin
              </button>
              <button 
                type="button" 
                @click="fillCredentials('bapperida', 'bapperida123')"
                class="px-2 py-0.5 rounded bg-white/10 hover:bg-white/20 text-slate-200 font-bold"
              >
                Bapperida
              </button>
              <button 
                type="button" 
                @click="fillCredentials('dpupr', 'dpupr123')"
                class="px-2 py-0.5 rounded bg-white/10 hover:bg-white/20 text-slate-200 font-bold"
              >
                DPUPR
              </button>
            </div>
          </div>

        </form>

        <p class="text-center text-[10px] text-slate-400 font-medium">Pemerintah Kota Tegal &copy; 2026</p>

      </div>

      <!-- Bottom Right Power & System Controls -->
      <div class="absolute bottom-6 right-6 flex items-center space-x-3 text-slate-300">
        <button class="p-2 rounded-full hover:bg-white/10" title="Jaringan Internet"><Wifi class="w-4 h-4 text-emerald-400" /></button>
        <button class="p-2 rounded-full hover:bg-white/10" title="Kemudahan Akses"><Accessibility class="w-4 h-4" /></button>
        <button @click="showShutdownDialog" class="p-2 rounded-full hover:bg-white/10 text-red-400" title="Daya"><Power class="w-4 h-4" /></button>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/auth'
import { 
  Wifi, BatteryCharging, ChevronUp, User, Lock, ArrowRight, 
  ArrowLeft, Eye, EyeOff, Loader2, RotateCw, ShieldCheck, 
  AlertCircle, Power, Accessibility 
} from 'lucide-vue-next'

const emit = defineEmits(['login-success'])

const authStore = useAuthStore()

const isEnteringPassword = ref(true)
const username = ref('admin')
const password = ref('')
const showPassword = ref(false)
const captchaCode = ref('')
const captchaInput = ref('')
const captchaError = ref('')

// REALTIME CLOCK FOR LOCK SCREEN
const currentTime = ref('')
const currentDateLong = ref('')
let timer = null

function updateClock() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', hour12: false })
  currentDateLong.value = now.toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
}

// CAPTCHA GENERATION (PERSIS METODE SIMLABA)
function generateCaptcha() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let result = ''
  for (let i = 0; i < 5; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  captchaCode.value = result
  captchaInput.value = ''
  captchaError.value = ''
}

function showSignInForm() {
  isEnteringPassword.value = true
  generateCaptcha()
}

function fillCredentials(u, p) {
  username.value = u
  password.value = p
  captchaInput.value = captchaCode.value
}

onMounted(() => {
  updateClock()
  timer = setInterval(updateClock, 1000)
  generateCaptcha()

  window.addEventListener('keydown', handleGlobalKey)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  window.removeEventListener('keydown', handleGlobalKey)
})

function handleGlobalKey(e) {
  if (!isEnteringPassword.value) {
    showSignInForm()
  }
}

// HANDLE LOGIN (METODE SAMA PERSIS DENGAN SIMLABA MENGGUNAKAN BACKEND API)
async function handleLogin() {
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
  
  // Real login API via Backend PostgreSQL /api/v1/auth/login
  const success = await authStore.login(username.value, password.value)
  if (!success) {
    generateCaptcha()
  } else {
    emit('login-success')
  }
}

function showShutdownDialog() {
  Swal.fire({
    title: 'Matikan Sistem?',
    text: 'Apakah Anda ingin menutup sesi EMONEV OS?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Ya, Tutup',
    cancelButtonText: 'Batal',
    confirmButtonColor: '#ef4444'
  })
}
</script>
