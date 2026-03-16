<template>
  <div class="play-history">
    <div class="page-header">
      <h1>播放记录</h1>
      <div class="header-actions">
        <button class="clear-btn" @click="showClearModal = true" v-if="history.length > 0">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
          清空记录
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="history.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
      </svg>
      <h3>暂无播放记录</h3>
      <p>您还没有观看过任何视频</p>
    </div>
    
    <div v-else class="history-list">
      <div v-for="item in history" :key="item.id" class="history-item glass">
        <div class="item-thumbnail">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
        </div>
        <div class="item-info">
          <h3 class="item-name">{{ item.video_name }}</h3>
          <div class="item-meta">
            <span class="meta-tag format">{{ item.video_format?.toUpperCase() || 'MP4' }}</span>
            <span class="meta-tag type" :class="item.video_url?.startsWith('/uploads') ? 'server' : 'online'">
              {{ item.video_url?.startsWith('/uploads') ? '服务器视频' : '在线视频' }}
            </span>
            <span class="meta-time">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              {{ formatDate(item.created_at) }}
            </span>
          </div>
        </div>
        <div class="item-actions">
          <button class="action-btn play-btn" @click="playVideo(item)" title="播放">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>
          <button class="action-btn delete-btn" @click="confirmDelete(item)" title="删除">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Clear Confirm Modal -->
    <div v-if="showClearModal" class="modal-overlay" @click="showClearModal = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <h3>清空播放记录</h3>
        </div>
        <div class="modal-body">
          <p>确定要清空所有播放记录吗？此操作不可恢复。</p>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="showClearModal = false">取消</button>
          <button class="btn danger" @click="clearAllHistory" :disabled="clearing">
            <span v-if="clearing" class="btn-spinner"></span>
            <span v-else>清空</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <h3>删除记录</h3>
        </div>
        <div class="modal-body">
          <p>确定要删除此播放记录吗？</p>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="showDeleteModal = false">取消</button>
          <button class="btn danger" @click="deleteHistoryItem" :disabled="deleting">
            <span v-if="deleting" class="btn-spinner"></span>
            <span v-else>删除</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Video Player Modal -->
    <div v-if="showPlayerModal" class="modal-overlay" @click="showPlayerModal = false">
      <div class="player-modal" @click.stop>
        <div class="player-header">
          <h3>{{ playingVideo?.video_name }}</h3>
          <button class="close-btn" @click="showPlayerModal = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="player-container">
          <VideoPlayer 
            v-if="playingVideo" 
            :url="getVideoUrl(playingVideo.video_url)" 
            :format="playingVideo.video_format || 'mp4'"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import VideoPlayer from '@/components/VideoPlayer.vue'

const API_BASE = 'http://localhost:8000'

const history = ref([])
const loading = ref(true)
const accessToken = ref('')

const showClearModal = ref(false)
const showDeleteModal = ref(false)
const showPlayerModal = ref(false)

const itemToDelete = ref(null)
const deleting = ref(false)
const clearing = ref(false)

const playingVideo = ref(null)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    accessToken.value = token
    loadHistory()
  }
})

const apiRequest = async (endpoint, options = {}) => {
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

const loadHistory = async () => {
  loading.value = true
  try {
    const response = await apiRequest('/history')
    if (response.ok) {
      history.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load history:', err)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteModal.value = true
}

const deleteHistoryItem = async () => {
  if (!itemToDelete.value) return
  
  deleting.value = true
  try {
    const response = await apiRequest(`/history/${itemToDelete.value.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      history.value = history.value.filter(h => h.id !== itemToDelete.value.id)
      showDeleteModal.value = false
      itemToDelete.value = null
    } else {
      alert('删除失败')
    }
  } catch (err) {
    console.error('Delete error:', err)
    alert('删除失败')
  } finally {
    deleting.value = false
  }
}

const clearAllHistory = async () => {
  clearing.value = true
  try {
    const response = await apiRequest('/history', {
      method: 'DELETE'
    })
    
    if (response.ok) {
      history.value = []
      showClearModal.value = false
    } else {
      alert('清空失败')
    }
  } catch (err) {
    console.error('Clear error:', err)
    alert('清空失败')
  } finally {
    clearing.value = false
  }
}

const playVideo = (item) => {
  playingVideo.value = item
  showPlayerModal.value = true
}

const getVideoUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${API_BASE}${url}`
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style lang="scss" scoped>
.play-history {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  
  h1 {
    font-size: 1.75rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .clear-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 10px;
    color: #fca5a5;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    
    svg {
      width: 18px;
      height: 18px;
    }
    
    &:hover {
      background: rgba(239, 68, 68, 0.2);
      border-color: rgba(239, 68, 68, 0.4);
    }
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #94a3b8;
  
  .spinner {
    width: 48px;
    height: 48px;
    border: 3px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: rgba(30, 41, 59, 0.4);
  border: 1px dashed rgba(99, 102, 241, 0.3);
  border-radius: 20px;
  
  svg {
    width: 80px;
    height: 80px;
    color: #475569;
    margin-bottom: 24px;
  }
  
  h3 {
    font-size: 1.25rem;
    color: #94a3b8;
    margin-bottom: 8px;
  }
  
  p {
    color: #64748b;
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
  gap: 20px;
  padding: 20px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateX(4px);
    
    .item-actions {
      opacity: 1;
    }
  }
  
  .item-thumbnail {
    width: 80px;
    height: 60px;
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    
    svg {
      width: 28px;
      height: 28px;
      color: #6366f1;
      opacity: 0.6;
    }
  }
  
  .item-info {
    flex: 1;
    min-width: 0;
    
    .item-name {
      font-size: 1rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 8px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    
    .item-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      
      .meta-tag {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        
        &.format {
          background: rgba(99, 102, 241, 0.2);
          color: #a5b4fc;
        }
        
        &.type {
          &.server {
            background: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
          }
          
          &.online {
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
          }
        }
      }
      
      .meta-time {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 0.8rem;
        color: #64748b;
        
        svg {
          width: 14px;
          height: 14px;
        }
      }
    }
  }
  
  .item-actions {
    display: flex;
    gap: 8px;
    opacity: 0;
    transition: opacity 0.3s ease;
    
    .action-btn {
      width: 40px;
      height: 40px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      
      svg {
        width: 18px;
        height: 18px;
      }
      
      &.play-btn {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        
        &:hover {
          background: rgba(99, 102, 241, 0.3);
          color: #c7d2fe;
        }
      }
      
      &.delete-btn {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        
        &:hover {
          background: rgba(239, 68, 68, 0.3);
        }
      }
    }
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
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-card {
  width: 90%;
  max-width: 400px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  
  .modal-header {
    display: flex;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);
    
    h3 {
      font-size: 1.1rem;
      font-weight: 600;
      color: #f8fafc;
    }
    
    .warning-icon {
      width: 40px;
      height: 40px;
      color: #f59e0b;
      margin-right: 12px;
    }
  }
  
  .modal-body {
    padding: 24px;
    
    p {
      color: #94a3b8;
      line-height: 1.6;
    }
  }
  
  .modal-footer {
    display: flex;
    gap: 12px;
    padding: 16px 24px 24px;
    justify-content: flex-end;
  }
}

.btn {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  
  &.secondary {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #a5b4fc;
    
    &:hover {
      background: rgba(99, 102, 241, 0.2);
    }
  }
  
  &.danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border: none;
    color: white;
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .btn-spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
}

.player-modal {
  width: 90%;
  max-width: 900px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  overflow: hidden;
  
  .player-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);
    
    h3 {
      font-size: 1rem;
      color: #f8fafc;
    }
    
    .close-btn {
      width: 32px;
      height: 32px;
      border: none;
      background: rgba(99, 102, 241, 0.1);
      border-radius: 8px;
      color: #94a3b8;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      
      svg {
        width: 18px;
        height: 18px;
      }
    }
  }
  
  .player-container {
    aspect-ratio: 16/9;
    background: #000;
  }
}

.glass {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .history-item {
    flex-direction: column;
    align-items: stretch;
    
    .item-thumbnail {
      width: 100%;
      height: 120px;
    }
    
    .item-actions {
      opacity: 1;
      margin-top: 12px;
    }
  }
}
</style>
