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
    userFullName: (state) => state.user?.nama || state.user?.username || 'Administrator',
    userRole: (state) => state.user?.role_id === 1 ? 'Super Admin' : (state.user?.role || 'Pengguna')
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
      this.error = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      const storedToken = localStorage.getItem('token')
      const storedUser = localStorage.getItem('user')
      if (storedToken) {
        this.token = storedToken
        try {
          this.user = JSON.parse(storedUser)
        } catch (e) {
          this.user = null
        }
        axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
      }
    }
  }
})
