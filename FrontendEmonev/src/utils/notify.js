import Swal from 'sweetalert2'

// Configured SweetAlert2 Toast Mixin with modern Tailwind Dark Mode aesthetics
const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 4000,
  timerProgressBar: true,
  customClass: {
    popup: 'rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-[#141d30]/95 backdrop-blur-md text-slate-900 dark:text-white font-sans text-xs',
    title: 'font-bold text-xs text-slate-800 dark:text-slate-100'
  },
  didOpen: (toast) => {
    toast.onmouseenter = Swal.stopTimer
    toast.onmouseleave = Swal.resumeTimer
  }
})

export const notifySuccess = (title, message = '') => {
  Toast.fire({
    icon: 'success',
    title: title,
    text: message,
    iconColor: '#10b981'
  })
}

export const notifyError = (title, message = '') => {
  Toast.fire({
    icon: 'error',
    title: title,
    text: message,
    iconColor: '#f43f5e'
  })
}

export const notifyWarning = (title, message = '') => {
  Toast.fire({
    icon: 'warning',
    title: title,
    text: message,
    iconColor: '#f59e0b'
  })
}

export const notifyInfo = (title, message = '') => {
  Toast.fire({
    icon: 'info',
    title: title,
    text: message,
    iconColor: '#3b82f6'
  })
}

// Modern Modal Confirm Dialog
export const confirmDialog = async ({
  title = 'Apakah Anda Yakin?',
  text = 'Tindakan ini tidak dapat dibatalkan.',
  confirmButtonText = 'Ya, Lanjutkan',
  cancelButtonText = 'Batal',
  icon = 'warning'
}) => {
  const result = await Swal.fire({
    title,
    text,
    icon,
    showCancelButton: true,
    confirmButtonText,
    cancelButtonText,
    buttonsStyling: false,
    customClass: {
      popup: 'rounded-3xl shadow-2xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-[#141d30] text-slate-900 dark:text-white p-6 font-sans',
      title: 'text-base font-black text-slate-900 dark:text-white',
      htmlContainer: 'text-xs text-slate-600 dark:text-slate-300 font-semibold mt-2',
      confirmButton: 'px-5 py-2.5 rounded-xl font-black text-xs text-white bg-[#308e87] hover:bg-[#25736d] shadow-md shadow-[#308e87]/30 transition-all cursor-pointer mr-2',
      cancelButton: 'px-4 py-2.5 rounded-xl font-bold text-xs text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer'
    }
  })
  return result.isConfirmed
}

// Modern Modal Prompt Dialog
export const promptDialog = async ({
  title = 'Masukkan Catatan',
  inputPlaceholder = 'Catatan...',
  defaultValue = '',
  confirmButtonText = 'Simpan',
  cancelButtonText = 'Batal'
}) => {
  const result = await Swal.fire({
    title,
    input: 'textarea',
    inputValue: defaultValue,
    inputPlaceholder,
    showCancelButton: true,
    confirmButtonText,
    cancelButtonText,
    buttonsStyling: false,
    customClass: {
      popup: 'rounded-3xl shadow-2xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-[#141d30] text-slate-900 dark:text-white p-6 font-sans',
      title: 'text-base font-black text-slate-900 dark:text-white',
      input: 'w-full px-3.5 py-2.5 rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-xs font-semibold text-slate-900 dark:text-white focus:outline-none focus:border-[#308e87] my-3',
      confirmButton: 'px-5 py-2.5 rounded-xl font-black text-xs text-white bg-[#308e87] hover:bg-[#25736d] shadow-md shadow-[#308e87]/30 transition-all cursor-pointer mr-2',
      cancelButton: 'px-4 py-2.5 rounded-xl font-bold text-xs text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer'
    }
  })
  return result.isConfirmed ? (result.value || '') : null
}
