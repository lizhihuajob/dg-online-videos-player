import { defineStore } from 'pinia'
import { api } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    isLoggedIn: false
  }),

  actions: {
    async login(username, password) {
      const data = await api.login(username, password)
      this.token = data.access_token
      localStorage.setItem('token', data.access_token)
      await this.fetchUser()
      return true
    },

    async register(username, email, password) {
      await api.register(username, email, password)
      return await this.login(username, password)
    },

    async fetchUser() {
      if (!this.token) return
      try {
        this.user = await api.getCurrentUser(this.token)
        this.isLoggedIn = true
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.isLoggedIn = false
      localStorage.removeItem('token')
    },

    init() {
      if (this.token) {
        this.fetchUser().catch(() => {
          this.logout()
        })
      }
    }
  }
})
