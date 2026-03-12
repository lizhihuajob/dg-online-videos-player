const API_BASE_URL = '/api'

const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '请求失败' }))
    throw new Error(error.detail || '请求失败')
  }
  return response.json()
}

export const api = {
  async register(username, email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    })
    return handleResponse(response)
  },

  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    })
    return handleResponse(response)
  },

  async getCurrentUser(token) {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return handleResponse(response)
  },

  async getPlayHistory(token) {
    const response = await fetch(`${API_BASE_URL}/history/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return handleResponse(response)
  },

  async addPlayHistory(token, data) {
    const response = await fetch(`${API_BASE_URL}/history/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },

  async deletePlayHistory(token, historyId) {
    const response = await fetch(`${API_BASE_URL}/history/${historyId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return handleResponse(response)
  },

  async clearPlayHistory(token) {
    const response = await fetch(`${API_BASE_URL}/history/`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return handleResponse(response)
  }
}
