import { API_CONFIG, getAuthHeaders } from './config'

const API_URL = `${API_CONFIG.baseURL}/api/history`

export const historyApi = {
  // 获取播放记录列表
  async getList(skip = 0, limit = 50) {
    const response = await fetch(`${API_URL}/list?skip=${skip}&limit=${limit}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '获取播放记录失败')
    }

    return await response.json()
  },

  // 保存播放记录
  async save(historyData) {
    const response = await fetch(`${API_URL}/save`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(historyData)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '保存播放记录失败')
    }

    return await response.json()
  },

  // 更新播放进度
  async update(historyId, currentTime, duration = null) {
    const body = { current_time: currentTime }
    if (duration !== null) {
      body.duration = duration
    }

    const response = await fetch(`${API_URL}/update/${historyId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '更新播放进度失败')
    }

    return await response.json()
  },

  // 删除单条播放记录
  async delete(historyId) {
    const response = await fetch(`${API_URL}/delete/${historyId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '删除播放记录失败')
    }

    return await response.json()
  },

  // 清空播放记录
  async clear() {
    const response = await fetch(`${API_URL}/clear`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || '清空播放记录失败')
    }

    return await response.json()
  },

  // 检查视频是否有播放记录
  async check(videoUrl) {
    const response = await fetch(`${API_URL}/check?video_url=${encodeURIComponent(videoUrl)}`, {
      method: 'GET',
      headers: getAuthHeaders()
    })

    if (!response.ok) {
      return null
    }

    return await response.json()
  }
}
