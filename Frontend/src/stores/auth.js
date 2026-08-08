import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || '',
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userFullName: (state) => state.user?.nama || state.user?.username || 'Pengguna'
  },

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('/api/v1/auth/login', { username, password })
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify(user))
        
        // Setup axios header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Gagal login. Periksa username dan password.'
        return false
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      }
    }
  }
})
