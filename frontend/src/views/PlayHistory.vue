<template>
  <div class="play-history">
    <div class="page-header">
      <h1>播放历史</h1>
      <button v-if="historyList.length > 0" class="clear-all-btn" @click="confirmClearAll">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        </svg>
        <span>清空全部</span>
      </button>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="historyList.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <h3>暂无播放历史</h3>
      <p>您还没有播放过任何视频</p>
    </div>

    <div v-else class="history-list">
      <div v-for="item in historyList" :key="item.id" class="history-item glass">
        <div class="history-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20.2 6H3.8C2.8 6 2 6.8 2 7.8V16.2C2 17.2 2.8 18 3.8 18H20.2C21.2 18 22 17.2 22 16.2V7.8C22 6.8 21.2 6 20.2 6Z" />
            <path d="M10 8l6 4-6 4V8z" fill="currentColor" opacity="0.3"/>
          </svg>
        </div>
        <div class="history-info">
          <div class="video-name">{{ item.video_name }}</div>
          <div class="video-meta">
            <span class="video-format">{{ item.video_format?.toUpperCase() || '视频' }}</span>
            <span class="play-time">{{ formatDate(item.created_at) }}</span>
          </div>
        </div>
        <button class="delete-btn" @click="confirmDelete(item)" title="删除记录">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="showDeleteConfirm" class="modal-overlay" @click="showDeleteConfirm = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <h3>确认删除</h3>
        </div>
        <p>确定要删除这条播放记录吗？</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showDeleteConfirm = false">取消</button>
          <button class="delete-confirm-btn" @click="deleteHistoryItem">确认删除</button>
        </div>
      </div>
    </div>

    <div v-if="showClearAllConfirm" class="modal-overlay" @click="showClearAllConfirm = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <h3>确认清空</h3>
        </div>
        <p>确定要清空所有播放历史吗？此操作无法撤销。</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showClearAllConfirm = false">取消</button>
          <button class="delete-confirm-btn" @click="clearAllHistory">确认清空</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://localhost:8000'

const historyList = ref([])
const loading = ref(true)
const showDeleteConfirm = ref(false)
const showClearAllConfirm = ref(false)
const itemToDelete = ref(null)

const apiRequest = async (endpoint, options = {}) => {
  const headers = {
    ...options.headers
  }
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }
  const token = localStorage.getItem('access_token')
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  })
  return response
}

const loadHistory = async () => {
  loading.value = true
  try {
    const response = await apiRequest('/history')
    if (response.ok) {
      historyList.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load history:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadHistory()
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteConfirm.value = true
}

const deleteHistoryItem = async () => {
  if (!itemToDelete.value) return
  
  try {
    const response = await apiRequest(`/history/${itemToDelete.value.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      historyList.value = historyList.value.filter(item => item.id !== itemToDelete.value.id)
      showDeleteConfirm.value = false
      itemToDelete.value = null
    }
  } catch (err) {
    console.error('Failed to delete history item:', err)
  }
}

const confirmClearAll = () => {
  showClearAllConfirm.value = true
}

const clearAllHistory = async () => {
  try {
    const response = await apiRequest('/history', {
      method: 'DELETE'
    })
    
    if (response.ok) {
      historyList.value = []
      showClearAllConfirm.value = false
    }
  } catch (err) {
    console.error('Failed to clear history:', err)
  }
}
</script>

<style lang="scss" scoped>
.play-history {
  color: #f8fafc;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  h1 {
    font-size: 1.5rem;
    font-weight: 600;
    background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
  }

  .clear-all-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px -3px rgba(239, 68, 68, 0.4);

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 20px -4px rgba(239, 68, 68, 0.5);
    }
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 0;
  color: #94a3b8;

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 16px;
  }
}

.empty-state {
  text-align: center;
  padding: 64px 24px;
  color: #94a3b8;

  svg {
    width: 64px;
    height: 64px;
    margin-bottom: 16px;
    opacity: 0.3;
  }

  h3 {
    font-size: 1.25rem;
    margin-bottom: 8px;
    color: #f8fafc;
  }

  p {
    max-width: 400px;
    margin: 0 auto;
  }
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-1px);
    box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.2);
  }
}

.history-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6366f1;

  svg {
    width: 24px;
    height: 24px;
  }
}

.history-info {
  flex: 1;
  min-width: 0;

  .video-name {
    font-weight: 500;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .video-meta {
    display: flex;
    gap: 12px;
    font-size: 0.85rem;
    color: #94a3b8;

    .video-format {
      padding: 2px 6px;
      background: rgba(99, 102, 241, 0.15);
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      color: #6366f1;
    }
  }
}

.delete-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: rgba(239, 68, 68, 0.1);
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  svg {
    width: 18px;
    height: 18px;
  }

  &:hover {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.modal-card {
  width: 90%;
  max-width: 450px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  padding: 28px;
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
}

.modal-header {
  margin-bottom: 24px;
  text-align: center;

  h3 {
    font-size: 1.25rem;
    margin: 0;
    font-weight: 600;
    color: #f8fafc;
  }

  .warning-icon {
    width: 48px;
    height: 48px;
    color: #f59e0b;
    margin: 0 auto 15px;
    filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.3));
  }
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;

  .cancel-btn {
    flex: 1;
    padding: 12px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    color: #f8fafc;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .delete-confirm-btn {
    flex: 1;
    padding: 12px;
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px -3px rgba(239, 68, 68, 0.4);

    &:hover {
      background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
      box-shadow: 0 6px 20px -4px rgba(239, 68, 68, 0.5);
    }
  }
}

.glass {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
