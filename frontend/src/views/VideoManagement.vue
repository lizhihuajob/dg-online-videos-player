<template>
  <div class="video-management">
    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="M21 21l-4.35-4.35"/>
        </svg>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索视频..."
        >
      </div>
      <button class="upload-btn" @click="showUploadModal = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span>上传视频</span>
      </button>
    </div>

    <!-- Video Grid -->
    <div v-if="filteredVideos.length > 0" class="video-grid">
      <div
        v-for="video in filteredVideos"
        :key="video.id"
        class="video-card"
      >
        <div class="video-thumbnail" @click="playVideo(video)">
          <div class="thumbnail-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
              <line x1="7" y1="2" x2="7" y2="22"/>
              <line x1="17" y1="2" x2="17" y2="22"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
            </svg>
          </div>
          <div class="play-overlay">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </div>
          <span class="video-format">{{ video.format.toUpperCase() }}</span>
        </div>

        <div class="video-info">
          <h3 class="video-name" :title="video.original_name">{{ video.original_name }}</h3>
          <div class="video-meta">
            <span class="video-size">{{ formatSize(video.size) }}</span>
            <span class="video-date">{{ formatDate(video.created_at) }}</span>
          </div>
        </div>

        <div class="video-actions">
          <button class="action-btn edit" @click="editVideo(video)" title="修改名称">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="action-btn play" @click="playVideo(video)" title="播放">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
          </button>
          <button class="action-btn delete" @click="confirmDelete(video)" title="删除">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoading" class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
          <line x1="7" y1="2" x2="7" y2="22"/>
          <line x1="17" y1="2" x2="17" y2="22"/>
          <line x1="2" y1="12" x2="22" y2="12"/>
        </svg>
      </div>
      <h3>暂无视频</h3>
      <p>点击上方"上传视频"按钮添加您的第一个视频</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="modal-overlay" @click.self="closeUploadModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>上传视频</h3>
          <button class="close-btn" @click="closeUploadModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div
            class="upload-area"
            :class="{ 'drag-over': isDragOver }"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleFileDrop"
            @click="fileInput?.click()"
          >
            <input
              ref="fileInput"
              type="file"
              accept="video/*"
              hidden
              @change="handleFileSelect"
            >
            <div v-if="!selectedFile" class="upload-placeholder">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <p>点击或拖拽视频文件到此处</p>
              <span>支持 MP4, WebM, AVI 等格式</span>
            </div>
            <div v-else class="selected-file">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              <div class="file-info">
                <span class="file-name">{{ selectedFile.name }}</span>
                <span class="file-size">{{ formatSize(selectedFile.size) }}</span>
              </div>
              <button class="clear-file" @click.stop="selectedFile = null">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
          </div>

          <div v-if="uploadError" class="upload-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>{{ uploadError }}</span>
          </div>

          <div v-if="groups.length > 0" class="group-select">
            <label>选择分组</label>
            <select v-model="selectedGroupId" class="form-select">
              <option :value="null">不选择分组</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
            </select>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn secondary" @click="closeUploadModal">取消</button>
          <button
            class="btn primary"
            :disabled="!selectedFile || isUploading"
            @click="uploadVideo"
          >
            <span v-if="isUploading" class="btn-spinner"></span>
            <span v-else>开始上传</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>修改视频名称</h3>
          <button class="close-btn" @click="closeEditModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>视频名称</label>
            <input
              type="text"
              v-model="editForm.name"
              placeholder="请输入视频名称"
            >
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn secondary" @click="closeEditModal">取消</button>
          <button
            class="btn primary"
            :disabled="!editForm.name.trim() || isEditing"
            @click="saveEdit"
          >
            <span v-if="isEditing" class="btn-spinner"></span>
            <span v-else>保存</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
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
          <p>确定要删除视频 "<strong>{{ videoToDelete?.original_name }}</strong>" 吗？</p>
          <p class="warning-text">此操作不可恢复，视频文件将被永久删除。</p>
        </div>

        <div class="modal-footer">
          <button class="btn secondary" @click="closeDeleteModal">取消</button>
          <button
            class="btn danger"
            :disabled="isDeleting"
            @click="deleteVideo"
          >
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
          <h3>{{ currentVideo?.original_name }}</h3>
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
            :url="getVideoUrl(currentVideo)"
            :format="currentVideo.format"
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import VideoPlayer from '@/components/VideoPlayer.vue'

const API_BASE = 'http://localhost:8000'
const authStore = useAuthStore()

// State
const videos = ref([])
const isLoading = ref(false)
const searchQuery = ref('')

// Upload modal state
const showUploadModal = ref(false)
const fileInput = ref(null)
const selectedFile = ref(null)
const isDragOver = ref(false)
const isUploading = ref(false)
const uploadError = ref('')
const groups = ref([])
const selectedGroupId = ref(null)

// Edit modal state
const showEditModal = ref(false)
const videoToEdit = ref(null)
const editForm = ref({ name: '' })
const isEditing = ref(false)

// Delete modal state
const showDeleteModal = ref(false)
const videoToDelete = ref(null)
const isDeleting = ref(false)

// Player modal state
const showPlayerModal = ref(false)
const currentVideo = ref(null)

// Toast state
const toastMessage = ref('')
const toastType = ref('success')

// Computed
const filteredVideos = computed(() => {
  if (!searchQuery.value.trim()) return videos.value
  const query = searchQuery.value.toLowerCase()
  return videos.value.filter(v => v.original_name.toLowerCase().includes(query))
})

// Lifecycle
onMounted(() => {
  loadVideos()
  loadGroups()
})

// Methods
async function loadVideos() {
  isLoading.value = true
  try {
    const response = await authStore.apiRequest('/videos')
    if (response.ok) {
      videos.value = await response.json()
    } else {
      showToast('加载视频失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isLoading.value = false
  }
}

async function loadGroups() {
  try {
    const response = await authStore.apiRequest('/groups')
    if (response.ok) {
      groups.value = await response.json()
    }
  } catch (err) {
    console.error('加载分组失败:', err)
  }
}

function formatSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

function getVideoUrl(video) {
  return `${API_BASE}${video.url}`
}

// Upload handlers
function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) {
    if (!file.type.startsWith('video/')) {
      uploadError.value = '请选择视频文件'
      return
    }
    selectedFile.value = file
    uploadError.value = ''
  }
}

function handleFileDrop(e) {
  isDragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) {
    if (!file.type.startsWith('video/')) {
      uploadError.value = '请拖拽视频文件'
      return
    }
    selectedFile.value = file
    uploadError.value = ''
  }
}

async function uploadVideo() {
  if (!selectedFile.value) return

  isUploading.value = true
  uploadError.value = ''

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    if (selectedGroupId.value) {
      formData.append('group_id', selectedGroupId.value)
    }

    const response = await authStore.apiRequest('/videos', {
      method: 'POST',
      body: formData,
      headers: {}
    })

    if (response.ok) {
      const newVideo = await response.json()
      videos.value.unshift(newVideo)
      closeUploadModal()
      showToast('上传成功', 'success')
    } else {
      const error = await response.json()
      uploadError.value = error.detail || '上传失败'
    }
  } catch (err) {
    uploadError.value = '网络错误'
  } finally {
    isUploading.value = false
  }
}

function closeUploadModal() {
  showUploadModal.value = false
  selectedFile.value = null
  uploadError.value = ''
  selectedGroupId.value = null
}

// Edit handlers
function editVideo(video) {
  videoToEdit.value = video
  editForm.value.name = video.original_name
  showEditModal.value = true
}

async function saveEdit() {
  if (!editForm.value.name.trim() || !videoToEdit.value) return

  isEditing.value = true
  try {
    const response = await authStore.apiRequest(`/videos/${videoToEdit.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ name: editForm.value.name.trim() })
    })

    if (response.ok) {
      const updatedVideo = await response.json()
      const index = videos.value.findIndex(v => v.id === updatedVideo.id)
      if (index !== -1) {
        videos.value[index] = updatedVideo
      }
      closeEditModal()
      showToast('修改成功', 'success')
    } else {
      const error = await response.json()
      showToast(error.detail || '修改失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isEditing.value = false
  }
}

function closeEditModal() {
  showEditModal.value = false
  videoToEdit.value = null
  editForm.value.name = ''
}

// Delete handlers
function confirmDelete(video) {
  videoToDelete.value = video
  showDeleteModal.value = true
}

async function deleteVideo() {
  if (!videoToDelete.value) return

  isDeleting.value = true
  try {
    const response = await authStore.apiRequest(`/videos/${videoToDelete.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      videos.value = videos.value.filter(v => v.id !== videoToDelete.value.id)
      closeDeleteModal()
      showToast('删除成功', 'success')
    } else {
      const error = await response.json()
      showToast(error.detail || '删除失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isDeleting.value = false
  }
}

function closeDeleteModal() {
  showDeleteModal.value = false
  videoToDelete.value = null
}

// Player handlers
function playVideo(video) {
  currentVideo.value = video
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
.video-management {
  min-height: 100%;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 200px;
  max-width: 400px;

  svg {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    width: 18px;
    height: 18px;
    color: #64748b;
  }

  input {
    width: 100%;
    padding: 12px 16px 12px 44px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.25s ease;

    &::placeholder {
      color: #64748b;
    }

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
      background: rgba(15, 23, 42, 0.8);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
  }
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px -5px rgba(99, 102, 241, 0.5);
  }

  svg {
    width: 18px;
    height: 18px;
  }
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.video-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 12px 40px -10px rgba(99, 102, 241, 0.2);

    .play-overlay {
      opacity: 1;
    }
  }
}

.video-thumbnail {
  position: relative;
  aspect-ratio: 16 / 9;
  background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
  cursor: pointer;
  overflow: hidden;

  .thumbnail-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      width: 48px;
      height: 48px;
      color: #475569;
    }
  }

  .play-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;

    svg {
      width: 56px;
      height: 56px;
      color: white;
      filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
    }
  }

  .video-format {
    position: absolute;
    bottom: 8px;
    right: 8px;
    padding: 4px 8px;
    background: rgba(0, 0, 0, 0.7);
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    color: #a5b4fc;
  }
}

.video-info {
  padding: 16px;

  .video-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .video-meta {
    display: flex;
    gap: 12px;
    font-size: 0.8rem;
    color: #64748b;
  }
}

.video-actions {
  display: flex;
  padding: 0 16px 16px;
  gap: 8px;

  .action-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 10px;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
    }

    &.edit:hover {
      color: #6366f1;
    }

    &.play:hover {
      color: #10b981;
    }

    &.delete:hover {
      color: #ef4444;
      border-color: rgba(239, 68, 68, 0.3);
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
  max-width: 480px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
  }

  .close-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #f8fafc;
    }

    svg {
      width: 16px;
      height: 16px;
    }
  }

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
}

.modal-body {
  padding: 24px;

  .form-group {
    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #e2e8f0;
    }

    input {
      width: 100%;
      padding: 12px 16px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 10px;
      color: #f8fafc;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.25s ease;

      &:focus {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(15, 23, 42, 0.8);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
      }
    }
  }

  .group-select {
    margin-top: 16px;

    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #e2e8f0;
    }

    .form-select {
      width: 100%;
      padding: 12px 16px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 10px;
      color: #f8fafc;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.25s ease;

      &:focus {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(15, 23, 42, 0.8);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
      }
    }
  }

  p {
    color: #94a3b8;
    text-align: center;
    margin-bottom: 8px;

    strong {
      color: #f8fafc;
    }
  }

  .warning-text {
    font-size: 0.85rem;
    color: #ef4444;
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

    &.primary {
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      color: white;
      box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

      &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px -5px rgba(99, 102, 241, 0.5);
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

// Upload area
.upload-area {
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 16px;
  padding: 40px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover, &.drag-over {
    border-color: rgba(99, 102, 241, 0.6);
    background: rgba(99, 102, 241, 0.05);
  }

  .upload-placeholder {
    svg {
      width: 48px;
      height: 48px;
      color: #6366f1;
      margin-bottom: 16px;
    }

    p {
      color: #e2e8f0;
      font-size: 1rem;
      margin-bottom: 8px;
    }

    span {
      color: #64748b;
      font-size: 0.85rem;
    }
  }

  .selected-file {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 12px;

    svg {
      width: 40px;
      height: 40px;
      color: #6366f1;
      flex-shrink: 0;
    }

    .file-info {
      flex: 1;
      text-align: left;

      .file-name {
        display: block;
        color: #f8fafc;
        font-weight: 500;
        margin-bottom: 4px;
        word-break: break-all;
      }

      .file-size {
        color: #64748b;
        font-size: 0.85rem;
      }
    }

    .clear-file {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(239, 68, 68, 0.1);
      border: none;
      border-radius: 8px;
      color: #ef4444;
      cursor: pointer;
      transition: all 0.2s ease;

      &:hover {
        background: rgba(239, 68, 68, 0.2);
      }

      svg {
        width: 16px;
        height: 16px;
      }
    }
  }
}

.upload-error {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;

  svg {
    width: 18px;
    height: 18px;
    color: #ef4444;
    flex-shrink: 0;
  }

  span {
    color: #fca5a5;
    font-size: 0.9rem;
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
  .video-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: none;
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
