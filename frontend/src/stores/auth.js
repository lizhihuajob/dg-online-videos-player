import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = 'http://localhost:8000'

export const useAuthStore = defineStore('auth', () => {
  // State
  const currentUser = ref(null)
  const accessToken = ref(null)
  const isLoading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!accessToken.value && !!currentUser.value)
  const userInitial = computed(() => {
    return currentUser.value?.username?.charAt(0).toUpperCase() || '?'
  })
  const avatarUrl = computed(() => {
    if (currentUser.value?.avatar_url) {
      return `${API_BASE}${currentUser.value.avatar_url}`
    }
    return null
  })

  // Actions
  function init() {
    const token = localStorage.getItem('access_token')
    const user = localStorage.getItem('current_user')
    if (token && user) {
      accessToken.value = token
      try {
        currentUser.value = JSON.parse(user)
      } catch (e) {
        logout()
      }
    }
  }

  async function login(username, password) {
    isLoading.value = true
    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)

      const response = await fetch(`${API_BASE}/token`, {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const data = await response.json()
        accessToken.value = data.access_token
        currentUser.value = data.user
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('current_user', JSON.stringify(data.user))
        return { success: true }
      } else {
        const error = await response.json()
        return { success: false, error: error.detail || '登录失败' }
      }
    } catch (err) {
      return { success: false, error: '网络错误' }
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    currentUser.value = null
    accessToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('current_user')
  }

  async function apiRequest(endpoint, options = {}) {
    const headers = {
      ...options.headers
    }
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
    }
    if (accessToken.value) {
      headers['Authorization'] = `Bearer ${accessToken.value}`
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    })
    return response
  }

  async function updateAvatar(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await apiRequest('/users/me/avatar', {
        method: 'POST',
        body: formData,
        headers: {}
      })

      if (response.ok) {
        const data = await response.json()
        currentUser.value.avatar_url = data.avatar_url
        localStorage.setItem('current_user', JSON.stringify(currentUser.value))
        return { success: true }
      } else {
        const error = await response.json()
        return { success: false, error: error.detail || '上传失败' }
      }
    } catch (err) {
      return { success: false, error: '网络错误' }
    }
  }

  async function updatePassword(currentPassword, newPassword) {
    try {
      const response = await apiRequest('/users/me/password', {
        method: 'PUT',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword
        })
      })

      if (response.ok) {
        return { success: true }
      } else {
        const error = await response.json()
        return { success: false, error: error.detail || '修改失败' }
      }
    } catch (err) {
      return { success: false, error: '网络错误' }
    }
  }

  return {
    currentUser,
    accessToken,
    isLoading,
    isLoggedIn,
    userInitial,
    avatarUrl,
    init,
    login,
    logout,
    apiRequest,
    updateAvatar,
    updatePassword
  }
})
