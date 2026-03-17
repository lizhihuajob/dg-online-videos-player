<template>
  <div class="play-history">
    <!-- Tabs -->
    <div class="tabs">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'online' }"
        @click="activeTab = 'online'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
          <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
        </svg>
        <span>在线视频</span>
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'local' }"
        @click="activeTab = 'local'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span>本地视频</span>
      </button>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="history-stats">
        共 <strong>{{ activeTab === 'online' ? onlineHistory.length : localHistory.length }}</strong> 条记录
      </div>
      <button
        v-if="(activeTab === 'online' && onlineHistory.length > 0) || (activeTab === 'local' && localHistory.length > 0)"
        class="clear-btn"
        @click="confirmClear"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"/>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        </svg>
        <span>清空记录</span>
      </button>
    </div>

    <!-- Online History List -->
    <div v-if="activeTab === 'online'" class="history-list">
      <div
        v-for="item in onlineHistory"
        :key="item.id"
        class="history-item"
      >
        <div class="item-icon online">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
          </svg>
        </div>
        <div class="item-content">
          <h4 class="item-title" :title="item.video_name">{{ item.video_name }}</h4>
          <div class="item-meta">
            <span class="item-format">{{ item.video_format.toUpperCase() }}</span>
            <span class="item-time">{{ formatTime(item.created_at) }}</span>
          </div>
          <p class="item-url" :title="item.video_url">{{ item.video_url }}</p>
        </div>
        <div class="item-actions">
          <button class="action-btn play" @click="playOnlineVideo(item)" title="播放">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
          </button>
          <button class="action-btn delete" @click="confirmDelete(item)" title="删除">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>

      <div v-if="onlineHistory.length === 0 && !isLoading" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <h3>暂无在线视频记录</h3>
        <p>您还没有播放过任何在线视频</p>
      </div>
    </div>

    <!-- Local History List -->
    <div v-else class="history-list">
      <div
        v-for="item in localHistory"
        :key="item.id"
        class="history-item"
      >
        <div class="item-icon local">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <div class="item-content">
          <h4 class="item-title" :title="item.video_name">{{ item.video_name }}</h4>
          <div class="item-meta">
            <span class="item-format">{{ item.video_format.toUpperCase() }}</span>
            <span class="item-time">{{ formatTime(item.created_at) }}</span>
          </div>
          <p class="item-file-info">{{ formatFileInfo(item.file_info) }}</p>
        </div>
        <div class="item-actions">
          <button class="action-btn delete" @click="confirmDelete(item)" title="删除">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>

      <div v-if="localHistory.length === 0 && !isLoading" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <h3>暂无本地视频记录</h3>
        <p>您还没有播放过任何本地视频</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Clear All Modal -->
    <div v-if="showClearModal" class="modal-overlay" @click.self="closeClearModal">
      <div class="modal-card">
        <div class="modal-header">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <h3>确认清空</h3>
        </div>
        <div class="modal-body">
          <p>确定要清空所有{{ activeTab === 'online' ? '在线' : '本地' }}视频播放记录吗？</p>
          <p class="warning-text">此操作不可恢复。</p>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="closeClearModal">取消</button>
          <button class="btn danger" :disabled="isClearing" @click="clearHistory">
            <span v-if="isClearing" class="btn-spinner"></span>
            <span v-else>确认清空</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Single Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal-card">
        <div class="modal-header">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <h3>确认删除</h3>
        </div>
        <div class="modal-body">
          <p>确定要删除这条播放记录吗？</p>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="closeDeleteModal">取消</button>
          <button class="btn danger" :disabled="isDeleting" @click="deleteHistory">
            <span v-if="isDeleting" class="btn-spinner"></span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Video Player Modal -->
    <div v-if="showPlayerModal" class="modal-overlay player-overlay" @click.self="closePlayer">
      <div class="player-modal">
        <div class="player-header">
          <h3>{{ currentVideo?.video_name }}</h3>
          <button class="close-btn" @click="closePlayer">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="player-body">
          <VideoPlayer
            v-if="currentVideo"
            :url="currentVideo.video_url"
            :format="currentVideo.video_format"
          />
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toastMessage" class="toast" :class="toastType">
      <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import VideoPlayer from '@/components/VideoPlayer.vue'

const authStore = useAuthStore()

// State
const activeTab = ref('online')
const onlineHistory = ref([])
const localHistory = ref([])
const isLoading = ref(false)

// Modal state
const showClearModal = ref(false)
const isClearing = ref(false)
const showDeleteModal = ref(false)
const itemToDelete = ref(null)
const isDeleting = ref(false)

// Player state
const showPlayerModal = ref(false)
const currentVideo = ref(null)

// Toast state
const toastMessage = ref('')
const toastType = ref('success')

// Lifecycle
onMounted(() => {
  loadHistory()
})

watch(activeTab, () => {
  loadHistory()
})

// Methods
async function loadHistory() {
  isLoading.value = true
  try {
    if (activeTab.value === 'online') {
      const response = await authStore.apiRequest('/history')
      if (response.ok) {
        onlineHistory.value = await response.json()
      }
    } else {
      const response = await authStore.apiRequest('/local-history')
      if (response.ok) {
        localHistory.value = await response.json()
      }
    }
  } catch (err) {
    showToast('加载失败', 'error')
  } finally {
    isLoading.value = false
  }
}

function formatTime(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`

  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

function formatFileInfo(fileInfoStr) {
  try {
    const info = JSON.parse(fileInfoStr)
    if (info.name && info.size) {
      const size = formatSize(info.size)
      return `${info.name} (${size})`
    }
    return fileInfoStr
  } catch {
    return fileInfoStr
  }
}

function formatSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Clear handlers
function confirmClear() {
  showClearModal.value = true
}

async function clearHistory() {
  isClearing.value = true
  try {
    const endpoint = activeTab.value === 'online' ? '/history' : '/local-history'
    const response = await authStore.apiRequest(endpoint, { method: 'DELETE' })

    if (response.ok) {
      if (activeTab.value === 'online') {
        onlineHistory.value = []
      } else {
        localHistory.value = []
      }
      closeClearModal()
      showToast('清空成功', 'success')
    } else {
      showToast('清空失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isClearing.value = false
  }
}

function closeClearModal() {
  showClearModal.value = false
}

// Delete handlers
function confirmDelete(item) {
  itemToDelete.value = item
  showDeleteModal.value = true
}

async function deleteHistory() {
  if (!itemToDelete.value) return

  isDeleting.value = true
  try {
    const endpoint = activeTab.value === 'online'
      ? `/history/${itemToDelete.value.id}`
      : `/local-history/${itemToDelete.value.id}`

    const response = await authStore.apiRequest(endpoint, { method: 'DELETE' })

    if (response.ok) {
      if (activeTab.value === 'online') {
        onlineHistory.value = onlineHistory.value.filter(h => h.id !== itemToDelete.value.id)
      } else {
        localHistory.value = localHistory.value.filter(h => h.id !== itemToDelete.value.id)
      }
      closeDeleteModal()
      showToast('删除成功', 'success')
    } else {
      showToast('删除失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isDeleting.value = false
  }
}

function closeDeleteModal() {
  showDeleteModal.value = false
  itemToDelete.value = null
}

// Player handlers
function playOnlineVideo(item) {
  currentVideo.value = item
  showPlayerModal.value = true
}

function closePlayer() {
  showPlayerModal.value = false
  currentVideo.value = null
}

// Toast
function showToast(message, type = 'success') {
  toastMessage.value = message
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3000)
}
</script>

<style lang="scss" scoped>
.play-history {
  min-height: 100%;
}

.tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;

  .tab-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
      color: #c7d2fe;
    }

    &.active {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
      border-color: rgba(99, 102, 241, 0.4);
      color: #f8fafc;
    }
  }
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: rgba(30, 41, 59, 0.4);
  border-radius: 12px;

  .history-stats {
    color: #94a3b8;
    font-size: 0.9rem;

    strong {
      color: #f8fafc;
    }
  }

  .clear-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 8px;
    color: #ef4444;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(239, 68, 68, 0.2);
      border-color: rgba(239, 68, 68, 0.4);
    }

    svg {
      width: 16px;
      height: 16px;
    }
  }
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.1);
  border-radius: 12px;
  transition: all 0.25s ease;

  &:hover {
    border-color: rgba(99, 102, 241, 0.2);
    background: rgba(30, 41, 59, 0.8);
  }

  .item-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &.online {
      background: rgba(99, 102, 241, 0.15);
      color: #6366f1;
    }

    &.local {
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
    }

    svg {
      width: 24px;
      height: 24px;
    }
  }

  .item-content {
    flex: 1;
    min-width: 0;

    .item-title {
      font-size: 0.95rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .item-meta {
      display: flex;
      gap: 12px;
      margin-bottom: 4px;

      .item-format {
        padding: 2px 8px;
        background: rgba(99, 102, 241, 0.15);
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        color: #a5b4fc;
      }

      .item-time {
        font-size: 0.8rem;
        color: #64748b;
      }
    }

    .item-url,
    .item-file-info {
      font-size: 0.8rem;
      color: #64748b;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  .item-actions {
    display: flex;
    gap: 8px;

    .action-btn {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(99, 102, 241, 0.15);
      border-radius: 8px;
      color: #94a3b8;
      cursor: pointer;
      transition: all 0.2s ease;

      svg {
        width: 16px;
        height: 16px;
      }

      &:hover {
        background: rgba(99, 102, 241, 0.1);
      }

      &.play:hover {
        color: #10b981;
        border-color: rgba(16, 185, 129, 0.3);
      }

      &.delete:hover {
        color: #ef4444;
        border-color: rgba(239, 68, 68, 0.3);
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;

  .empty-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      width: 40px;
      height: 40px;
      color: #6366f1;
    }
  }

  h3 {
    font-size: 1.25rem;
    color: #f8fafc;
    margin-bottom: 8px;
  }

  p {
    color: #64748b;
    font-size: 0.95rem;
  }
}

.loading-state {
  text-align: center;
  padding: 80px 20px;

  .spinner {
    width: 48px;
    height: 48px;
    border: 3px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
  }

  p {
    color: #64748b;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

// Modal styles
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.modal-card {
  width: 100%;
  max-width: 400px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  text-align: center;
  padding: 24px 24px 0;

  .warning-icon {
    width: 48px;
    height: 48px;
    margin: 0 auto 12px;
    background: rgba(239, 68, 68, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      width: 24px;
      height: 24px;
      color: #ef4444;
    }
  }

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
  }
}

.modal-body {
  padding: 20px 24px;

  p {
    color: #94a3b8;
    text-align: center;
    margin-bottom: 8px;

    &.warning-text {
      font-size: 0.85rem;
      color: #ef4444;
    }
  }
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;

  .btn {
    flex: 1;
    padding: 12px 20px;
    border: none;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    &.secondary {
      background: rgba(51, 65, 85, 0.6);
      color: #94a3b8;

      &:hover:not(:disabled) {
        background: rgba(71, 85, 105, 0.8);
      }
    }

    &.danger {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      color: white;
      box-shadow: 0 4px 15px -3px rgba(239, 68, 68, 0.4);

      &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -5px rgba(239, 68, 68, 0.5);
      }
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
}

// Player modal
.player-overlay {
  padding: 40px;
}

.player-modal {
  width: 100%;
  max-width: 1000px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.98) 0%, rgba(15, 23, 42, 0.99) 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 20px;
  }

  .close-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #f8fafc;
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.player-body {
  aspect-ratio: 16 / 9;
  background: #000;
}

// Toast
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  animation: slideIn 0.3s ease;
  z-index: 3000;

  &.success {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
  }

  &.error {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #f87171;
  }

  svg {
    width: 20px;
    height: 20px;
  }
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;

    .tab-btn {
      justify-content: center;
    }
  }

  .history-item {
    flex-wrap: wrap;

    .item-content {
      width: calc(100% - 64px);
    }

    .item-actions {
      width: 100%;
      justify-content: flex-end;
      margin-top: 8px;
      padding-top: 12px;
      border-top: 1px solid rgba(99, 102, 241, 0.1);
    }
  }

  .player-overlay {
    padding: 0;
  }

  .player-modal {
    border-radius: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .player-body {
    flex: 1;
  }
}
</style>
