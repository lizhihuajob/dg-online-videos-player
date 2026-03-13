import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  const accessToken = ref(null)

  const isLoggedIn = computed(() => !!currentUser.value)

  const initFromStorage = () => {
    const token = localStorage.getItem('access_token')
    const user = localStorage.getItem('current_user')
    if (token && user) {
      accessToken.value = token
      currentUser.value = JSON.parse(user)
    }
  }

  const setUser = (user, token) => {
    currentUser.value = user
    accessToken.value = token
    localStorage.setItem('access_token', token)
    localStorage.setItem('current_user', JSON.stringify(user))
  }

  const logout = () => {
    currentUser.value = null
    accessToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('current_user')
  }

  const updateUserInfo = (userInfo) => {
    currentUser.value = { ...currentUser.value, ...userInfo }
    localStorage.setItem('current_user', JSON.stringify(currentUser.value))
  }

  return {
    currentUser,
    accessToken,
    isLoggedIn,
    initFromStorage,
    setUser,
    logout,
    updateUserInfo
  }
})
