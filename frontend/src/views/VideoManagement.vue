<template>
  <div class="video-management">
    <div class="page-header">
      <h1>视频管理</h1>
      <button class="upload-btn" @click="showUploadModal = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        上传视频
      </button>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="videos.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
        <line x1="7" y1="2" x2="7" y2="22"/>
        <line x1="17" y1="2" x2="17" y2="22"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <line x1="2" y1="7" x2="7" y2="7"/>
        <line x1="2" y1="17" x2="7" y2="17"/>
        <line x1="17" y1="17" x2="22" y2="17"/>
        <line x1="17" y1="7" x2="22" y2="7"/>
      </svg>
      <h3>暂无视频</h3>
      <p>点击上方按钮上传您的第一个视频</p>
    </div>
    
    <div v-else class="video-grid">
      <div v-for="video in videos" :key="video.id" class="video-card glass">
        <div class="video-thumbnail">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
          <span class="video-format">{{ video.format.toUpperCase() }}</span>
        </div>
        <div class="video-info">
          <h3 class="video-name" :title="video.name">{{ video.name }}</h3>
          <div class="video-meta">
            <span class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              {{ formatDate(video.created_at) }}
            </span>
            <span class="meta-item" v-if="video.size">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              {{ formatSize(video.size) }}
            </span>
          </div>
        </div>
        <div class="video-actions">
          <button class="action-btn play-btn" @click="playVideo(video)" title="播放">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>
          <button class="action-btn edit-btn" @click="openEditModal(video)" title="编辑">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="action-btn delete-btn" @click="confirmDelete(video)" title="删除">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/>
              <line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="modal-overlay" @click="showUploadModal = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <h3>上传视频</h3>
          <button class="close-btn" @click="showUploadModal = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div 
            class="upload-area"
            :class="{ 'drag-over': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            @click="fileInput.click()"
          >
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileSelect" 
              accept="video/*" 
              hidden
            >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <p>点击或拖拽视频文件到此处</p>
            <span class="upload-hint">支持 MP4, WebM, MOV 等格式</span>
          </div>
          
          <div v-if="selectedFile" class="selected-file">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="23 7 16 12 23 17 23 7"/>
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
            </svg>
            <div class="file-info">
              <span class="file-name">{{ selectedFile.name }}</span>
              <span class="file-size">{{ formatSize(selectedFile.size) }}</span>
            </div>
            <button class="clear-file" @click="selectedFile = null">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <div v-if="uploadProgress > 0" class="upload-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span>{{ uploadProgress }}%</span>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn secondary" @click="showUploadModal = false">取消</button>
          <button class="btn primary" @click="uploadVideo" :disabled="!selectedFile || uploading">
            <span v-if="uploading" class="btn-spinner"></span>
            <span v-else>上传</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <h3>编辑视频名称</h3>
          <button class="close-btn" @click="showEditModal = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>视频名称</label>
            <input type="text" v-model="editForm.name" placeholder="请输入视频名称">
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn secondary" @click="showEditModal = false">取消</button>
          <button class="btn primary" @click="updateVideoName" :disabled="!editForm.name.trim() || updating">
            <span v-if="updating" class="btn-spinner"></span>
            <span v-else>保存</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          <h3>确认删除</h3>
        </div>
        
        <div class="modal-body">
          <p>确定要删除视频 "{{ videoToDelete?.name }}" 吗？此操作不可恢复。</p>
        </div>
        
        <div class="modal-footer">
          <button class="btn secondary" @click="showDeleteModal = false">取消</button>
          <button class="btn danger" @click="deleteVideo" :disabled="deleting">
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
          <h3>{{ playingVideo?.name }}</h3>
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
            :url="API_BASE + playingVideo.url" 
            :format="playingVideo.format"
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

const videos = ref([])
const loading = ref(true)
const accessToken = ref('')

const showUploadModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showPlayerModal = ref(false)

const selectedFile = ref(null)
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const fileInput = ref(null)

const editForm = ref({ id: null, name: '' })
const updating = ref(false)

const videoToDelete = ref(null)
const deleting = ref(false)

const playingVideo = ref(null)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    accessToken.value = token
    loadVideos()
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

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file && file.type.startsWith('video/')) {
    selectedFile.value = file
  }
}

const handleDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file && file.type.startsWith('video/')) {
    selectedFile.value = file
  }
}

const uploadVideo = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  uploadProgress.value = 0
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const xhr = new XMLHttpRequest()
    
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        uploadProgress.value = Math.round((e.loaded / e.total) * 100)
      }
    })
    
    xhr.open('POST', `${API_BASE}/upload`)
    xhr.setRequestHeader('Authorization', `Bearer ${accessToken.value}`)
    
    xhr.onload = () => {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText)
        videos.value.unshift(data)
        showUploadModal.value = false
        selectedFile.value = null
        uploadProgress.value = 0
      } else {
        alert('上传失败')
      }
      uploading.value = false
    }
    
    xhr.onerror = () => {
      alert('上传失败')
      uploading.value = false
    }
    
    xhr.send(formData)
  } catch (err) {
    console.error('Upload error:', err)
    uploading.value = false
  }
}

const openEditModal = (video) => {
  editForm.value = { id: video.id, name: video.name }
  showEditModal.value = true
}

const updateVideoName = async () => {
  if (!editForm.value.name.trim()) return
  
  updating.value = true
  try {
    const response = await apiRequest(`/videos/${editForm.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ name: editForm.value.name })
    })
    
    if (response.ok) {
      const updated = await response.json()
      const index = videos.value.findIndex(v => v.id === updated.id)
      if (index !== -1) {
        videos.value[index] = updated
      }
      showEditModal.value = false
    } else {
      alert('更新失败')
    }
  } catch (err) {
    console.error('Update error:', err)
    alert('更新失败')
  } finally {
    updating.value = false
  }
}

const confirmDelete = (video) => {
  videoToDelete.value = video
  showDeleteModal.value = true
}

const deleteVideo = async () => {
  if (!videoToDelete.value) return
  
  deleting.value = true
  try {
    const response = await apiRequest(`/videos/${videoToDelete.value.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      videos.value = videos.value.filter(v => v.id !== videoToDelete.value.id)
      showDeleteModal.value = false
      videoToDelete.value = null
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

const playVideo = (video) => {
  playingVideo.value = video
  showPlayerModal.value = true
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

const formatSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style lang="scss" scoped>
.video-management {
  max-width: 1400px;
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
  
  .upload-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 24px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);
    
    svg {
      width: 20px;
      height: 20px;
    }
    
    &:hover {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
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
    box-shadow: 0 12px 40px -12px rgba(99, 102, 241, 0.3);
    
    .video-actions {
      opacity: 1;
    }
  }
  
  .video-thumbnail {
    position: relative;
    height: 160px;
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    
    svg {
      width: 48px;
      height: 48px;
      color: #6366f1;
      opacity: 0.6;
    }
    
    .video-format {
      position: absolute;
      top: 12px;
      right: 12px;
      padding: 4px 10px;
      background: rgba(99, 102, 241, 0.8);
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      color: white;
    }
  }
  
  .video-info {
    padding: 16px;
    
    .video-name {
      font-size: 1rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 8px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    
    .video-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      
      .meta-item {
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
  
  .video-actions {
    display: flex;
    gap: 8px;
    padding: 12px 16px;
    border-top: 1px solid rgba(99, 102, 241, 0.1);
    opacity: 0;
    transition: opacity 0.3s ease;
    
    .action-btn {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 10px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
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
      
      &.edit-btn {
        background: rgba(59, 130, 246, 0.2);
        color: #93c5fd;
        
        &:hover {
          background: rgba(59, 130, 246, 0.3);
          color: #bfdbfe;
        }
      }
      
      &.delete-btn {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        
        &:hover {
          background: rgba(239, 68, 68, 0.3);
          color: #fca5a5;
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
  max-width: 480px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  
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
      transition: all 0.2s ease;
      
      svg {
        width: 18px;
        height: 18px;
      }
      
      &:hover {
        background: rgba(99, 102, 241, 0.2);
        color: #f8fafc;
      }
    }
    
    .warning-icon {
      width: 48px;
      height: 48px;
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

.upload-area {
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 16px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover, &.drag-over {
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(99, 102, 241, 0.05);
  }
  
  svg {
    width: 48px;
    height: 48px;
    color: #6366f1;
    margin-bottom: 16px;
  }
  
  p {
    color: #94a3b8;
    margin-bottom: 8px;
  }
  
  .upload-hint {
    font-size: 0.85rem;
    color: #64748b;
  }
}

.selected-file {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 12px;
  margin-top: 16px;
  
  svg {
    width: 32px;
    height: 32px;
    color: #6366f1;
  }
  
  .file-info {
    flex: 1;
    
    .file-name {
      display: block;
      color: #f8fafc;
      font-weight: 500;
      margin-bottom: 4px;
    }
    
    .file-size {
      font-size: 0.8rem;
      color: #64748b;
    }
  }
  
  .clear-file {
    width: 32px;
    height: 32px;
    border: none;
    background: rgba(239, 68, 68, 0.2);
    border-radius: 8px;
    color: #fca5a5;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    
    svg {
      width: 16px;
      height: 16px;
    }
  }
}

.upload-progress {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  
  .progress-bar {
    flex: 1;
    height: 8px;
    background: rgba(99, 102, 241, 0.2);
    border-radius: 4px;
    overflow: hidden;
    
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #6366f1, #8b5cf6);
      border-radius: 4px;
      transition: width 0.3s ease;
    }
  }
  
  span {
    font-size: 0.9rem;
    color: #a5b4fc;
    font-weight: 500;
  }
}

.form-group {
  margin-bottom: 16px;
  
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
    
    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
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
  
  &.primary {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    color: white;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);
    
    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
    }
  }
  
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
    
    .upload-btn {
      justify-content: center;
    }
  }
  
  .video-grid {
    grid-template-columns: 1fr;
  }
}
</style>
