// API 基础配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const API_CONFIG = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
}

// 获取存储的token
export const getToken = () => {
  return localStorage.getItem('access_token')
}

// 设置token
export const setToken = (token) => {
  localStorage.setItem('access_token', token)
}

// 清除token
export const clearToken = () => {
  localStorage.removeItem('access_token')
}

// 获取请求头
export const getAuthHeaders = () => {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  }
}
