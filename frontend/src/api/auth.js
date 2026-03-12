import { API_CONFIG, getAuthHeaders, setToken, clearToken } from './config'

const API_URL = `${API_CONFIG.baseURL}/api/auth`

export const authApi = {
  // 用户注册
  async register(username, password) {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.detail || '注册失败')
    }
    
    // 保存token
    setToken(data.access_token)
    return data
  },

  // 用户登录
  async login(username, password) {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.detail || '登录失败')
    }
    
    // 保存token
    setToken(data.access_token)
    return data
  },

  // 获取当前用户信息
  async getCurrentUser() {
    const response = await fetch(`${API_URL}/me`, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    if (response.status === 401) {
      clearToken()
      return null
    }
    
    if (!response.ok) {
      return null
    }
    
    return await response.json()
  },

  // 登出
  logout() {
    clearToken()
  }
}
