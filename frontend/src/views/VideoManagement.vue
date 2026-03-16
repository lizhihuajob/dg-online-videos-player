<template>
  <div class="video-management">
    <div class="page-header">
      <h1>视频管理</h1>
      <button class="add-video-btn" @click="showAddModal = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="16"/>
          <line x1="8" y1="12" x2="16" y2="12"/>
        </svg>
        <span>上传视频</span>
      </button>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="videos.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
        <line x1="7" y1="2" x2="7" y2="22"/>
        <line x1="17" y1="2" x2="17" y2="22"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
      </svg>
      <h3>暂无视频</h3>
      <p>点击上方按钮上传第一个视频</p>
    </div>

    <div v-else class="videos-grid">
      <div v-for="video in videos" :key="video.id" class="video-card glass">
        <div class="video-thumbnail">
          <div class="thumbnail-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20.2 6H3.8C2.8 6 2 6.8 2 7.8V16.2C2 17.2 2.8 18 3.8 18H20.2C21.2 18 22 17.2 22 16.2V7.8C22 6.8 21.2 6 20.2 6Z" />
              <path d="M2 11H22" />
              <path d="M7 6L10 11" />
              <path d="M12 6L15 11" />
              <path d="M17 6L20 11" />
              <path d="M10 8l6 4-6 4V8z" fill="currentColor" opacity="0.3"/>
            </svg>
          </div>
          <div class="video-format">{{ video.format?.toUpperCase() || '视频' }}</div>
        </div>
        <div class="video-info">
          <div class="video-name" @dblclick="startEditing(video)">
            <input 
              v-if="editingVideo?.id === video.id"
              v-model="editName"
              @blur="saveEdit"
              @keyup.enter="saveEdit"
              @keyup.esc="cancelEdit"
              type="text"
              class="edit-input"
              autofocus
            >
            <span v-else>{{ video.name }}</span>
          </div>
          <div class="video-meta">
            <span class="video-size">{{ formatSize(video.size) }}</span>
            <span class="video-date">{{ formatDate(video.created_at) }}</span>
          </div>
        </div>
        <div class="video-actions">
          <button class="action-btn edit-btn" @click="startEditing(video)" title="重命名">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 3 21l.5-4.5L17 3z"/>
            </svg>
          </button>
          <button class="action-btn delete-btn" @click="confirmDelete(video)" title="删除">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <h3>上传视频</h3>
        </div>
        <form class="upload-form" @submit.prevent="handleUpload">
          <div class="form-group">
            <label>选择视频文件</label>
            <div class="upload-area" @click="fileInput.click()" :class="{ 'has-file': selectedFile }">
              <input 
                type="file" 
                ref="fileInput" 
                @change="handleFileSelect" 
                accept="video/*" 
                hidden
              >
              <div v-if="!selectedFile" class="upload-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <p>点击选择视频文件</p>
                <span class="upload-hint">支持 MP4, WebM 等格式</span>
              </div>
              <div v-else class="selected-file-info">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
                <div class="file-details">
                  <span class="file-name">{{ selectedFile.name }}</span>
                  <span class="file-size">{{ formatSize(selectedFile.size) }}</span>
                </div>
                <button type="button" class="clear-file" @click.stop="clearFileSelection">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="form-group">
            <label>视频名称</label>
            <input 
              type="text" 
              v-model="uploadForm.name" 
              placeholder="请输入视频名称（留空将使用文件名）"
            >
          </div>
          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="showAddModal = false">取消</button>
            <button 
              type="submit" 
              class="upload-btn" 
              :disabled="!selectedFile || isUploading"
            >
              <span v-if="isUploading" class="btn-spinner"></span>
              <span v-else>上传视频</span>
            </button>
          </div>
        </form>
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
        <p>确定要删除视频 "{{ videoToDelete?.name }}" 吗？此操作无法撤销。</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showDeleteConfirm = false">取消</button>
          <button class="delete-confirm-btn" @click="deleteVideo">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://localhost:8000'

const videos = ref([])
const loading = ref(true)
const showAddModal = ref(false)
const showDeleteConfirm = ref(false)
const videoToDelete = ref(null)
const selectedFile = ref(null)
const fileInput = ref(null)
const isUploading = ref(false)
const editingVideo = ref(null)
const editName = ref('')

const uploadForm = ref({
  name: ''
})

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

const loadVideos = async () => {
  loading.value = true
  try {
    const response = await apiRequest('/videos')
    if (response.ok) {
      videos.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load videos:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadVideos()
})

const formatSize = (bytes) => {
  if (!bytes) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const handleFileSelect = (e) => {
  if (e.target.files.length > 0) {
    selectedFile.value = e.target.files[0]
    if (!uploadForm.value.name) {
      uploadForm.value.name = selectedFile.value.name.replace(/\.[^/.]+$/, "")
    }
  }
}

const clearFileSelection = () => {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const response = await apiRequest('/upload', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const result = await response.json()
      if (uploadForm.value.name && uploadForm.value.name !== result.name) {
        await apiRequest(`/videos/${result.id}`, {
          method: 'PUT',
          body: JSON.stringify({ name: uploadForm.value.name })
        })
      }
      showAddModal.value = false
      selectedFile.value = null
      uploadForm.value.name = ''
      loadVideos()
    } else {
      const error = await response.json()
      alert(error.detail || '上传失败')
    }
  } catch (err) {
    alert('网络错误，请稍后重试')
  } finally {
    isUploading.value = false
  }
}

const startEditing = (video) => {
  editingVideo.value = video
  editName.value = video.name
}

const cancelEdit = () => {
  editingVideo.value = null
  editName.value = ''
}

const saveEdit = async () => {
  if (!editingVideo.value || !editName.value.trim()) {
    cancelEdit()
    return
  }
  
  try {
    const response = await apiRequest(`/videos/${editingVideo.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ name: editName.value.trim() })
    })
    
    if (response.ok) {
      const updatedVideo = await response.json()
      const index = videos.value.findIndex(v => v.id === updatedVideo.id)
      if (index !== -1) {
        videos.value[index] = updatedVideo
      }
    }
  } catch (err) {
    console.error('Failed to update video:', err)
  } finally {
    cancelEdit()
  }
}

const confirmDelete = (video) => {
  videoToDelete.value = video
  showDeleteConfirm.value = true
}

const deleteVideo = async () => {
  if (!videoToDelete.value) return
  
  try {
    const response = await apiRequest(`/videos/${videoToDelete.value.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      videos.value = videos.value.filter(v => v.id !== videoToDelete.value.id)
      showDeleteConfirm.value = false
      videoToDelete.value = null
    }
  } catch (err) {
    console.error('Failed to delete video:', err)
  }
}
</script>

<style lang="scss" scoped>
.video-management {
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

  .add-video-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
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

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.video-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.2s ease;

  &:hover {
    border-color: rgba(99, 102, 241, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
  }
}

.video-thumbnail {
  position: relative;
  height: 160px;
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;

  .thumbnail-placeholder {
    svg {
      width: 64px;
      height: 64px;
      color: #6366f1;
      opacity: 0.5;
    }
  }

  .video-format {
    position: absolute;
    bottom: 8px;
    right: 8px;
    padding: 4px 8px;
    background: rgba(0, 0, 0, 0.6);
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #f8fafc;
  }
}

.video-info {
  padding: 16px;

  .video-name {
    font-weight: 500;
    margin-bottom: 8px;
    cursor: text;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    .edit-input {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(99, 102, 241, 0.5);
      border-radius: 4px;
      color: #f8fafc;
      padding: 2px 4px;
      outline: none;
    }
  }

  .video-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #94a3b8;
  }
}

.video-actions {
  display: flex;
  justify-content: flex-end;
  padding: 0 16px 16px;
  gap: 8px;

  .action-btn {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    border: none;
    background: rgba(99, 102, 241, 0.1);
    color: #94a3b8;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;

    svg {
      width: 16px;
      height: 16px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.2);
      color: #f8fafc;
    }

    &.delete-btn:hover {
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
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

.upload-form {
  .form-group {
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #94a3b8;
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

      &::placeholder {
        color: #475569;
      }

      &:focus {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(15, 23, 42, 0.8);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
      }
    }
  }
}

.upload-area {
  border: 2px dashed rgba(99, 102, 241, 0.2);
  border-radius: 10px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover, &.has-file {
    border-color: rgba(99, 102, 241, 0.4);
    background: rgba(99, 102, 241, 0.05);
  }

  .upload-placeholder {
    svg {
      width: 48px;
      height: 48px;
      margin: 0 auto 12px;
      color: #6366f1;
      opacity: 0.5;
    }

    p {
      margin: 0 0 8px;
      color: #f8fafc;
    }

    .upload-hint {
      font-size: 0.85rem;
      color: #94a3b8;
    }
  }

  .selected-file-info {
    display: flex;
    align-items: center;
    gap: 12px;

    svg {
      width: 40px;
      height: 40px;
      color: #6366f1;
    }

    .file-details {
      flex: 1;
      text-align: left;

      .file-name {
        display: block;
        color: #f8fafc;
        font-weight: 500;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .file-size {
        font-size: 0.85rem;
        color: #94a3b8;
      }
    }

    .clear-file {
      width: 32px;
      height: 32px;
      border-radius: 6px;
      border: none;
      background: rgba(99, 102, 241, 0.1);
      color: #94a3b8;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;

      &:hover {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
      }
    }
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

  .upload-btn, .delete-confirm-btn {
    flex: 1;
    padding: 12px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    border-radius: 10px;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
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

  .delete-confirm-btn {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
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
