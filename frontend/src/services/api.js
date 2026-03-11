const API_BASE_URL = 'http://localhost:5000/api'

class ApiService {
  async getHistory() {
    try {
      const response = await fetch(`${API_BASE_URL}/history`)
      const result = await response.json()
      if (result.success) {
        return result.data
      }
      throw new Error(result.message)
    } catch (error) {
      console.error('获取播放记录失败:', error)
      throw error
    }
  }

  async addHistory(item) {
    try {
      const response = await fetch(`${API_BASE_URL}/history`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
      })
      const result = await response.json()
      if (!result.success) {
        throw new Error(result.message)
      }
      return result
    } catch (error) {
      console.error('保存播放记录失败:', error)
      throw error
    }
  }

  async deleteHistoryItem(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/history/${id}`, {
        method: 'DELETE'
      })
      const result = await response.json()
      if (!result.success) {
        throw new Error(result.message)
      }
      return result
    } catch (error) {
      console.error('删除播放记录失败:', error)
      throw error
    }
  }

  async clearHistory() {
    try {
      const response = await fetch(`${API_BASE_URL}/history/clear`, {
        method: 'DELETE'
      })
      const result = await response.json()
      if (!result.success) {
        throw new Error(result.message)
      }
      return result
    } catch (error) {
      console.error('清除播放记录失败:', error)
      throw error
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      const result = await response.json()
      return result.success
    } catch (error) {
      return false
    }
  }
}

export const apiService = new ApiService()
