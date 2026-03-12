import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import { getToken } from '@/api/config'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // Getters
  const isLoggedIn = computed(() => !!user.value)
  const username = computed(() => user.value?.username || '')
  const hasToken = computed(() => !!getToken())

  // Actions
  // 初始化 - 检查本地token并获取用户信息
  async function init() {
    if (!hasToken.value) {
      return
    }

    isLoading.value = true
    try {
      const userData = await authApi.getCurrentUser()
      if (userData) {
        user.value = userData
      }
    } catch (err) {
      console.error('初始化用户失败:', err)
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  async function register(username, password) {
    isLoading.value = true
    error.value = null

    try {
      const data = await authApi.register(username, password)
      user.value = data.user
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 登录
  async function login(username, password) {
    isLoading.value = true
    error.value = null

    try {
      const data = await authApi.login(username, password)
      user.value = data.user
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  function logout() {
    authApi.logout()
    user.value = null
    error.value = null
  }

  // 清除错误
  function clearError() {
    error.value = null
  }

  return {
    user,
    isLoading,
    error,
    isLoggedIn,
    username,
    hasToken,
    init,
    register,
    login,
    logout,
    clearError
  }
})
