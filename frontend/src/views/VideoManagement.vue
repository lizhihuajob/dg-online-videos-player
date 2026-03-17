<template>
  <div class="video-management">
    <div class="toolbar">
      <div class="toolbar-left">
        <div class="media-tabs">
          <button
            class="tab-btn"
            :class="{ active: currentMediaType === 'video' }"
            @click="switchMediaType('video')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
              <line x1="7" y1="2" x2="7" y2="22"/>
              <line x1="17" y1="2" x2="17" y2="22"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
            </svg>
            <span>视频</span>
          </button>
          <button
            class="tab-btn"
            :class="{ active: currentMediaType === 'music' }"
            @click="switchMediaType('music')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18V5l12-2v13"/>
              <circle cx="6" cy="18" r="3"/>
              <circle cx="18" cy="16" r="3"/>
            </svg>
            <span>音乐</span>
          </button>
        </div>
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            type="text"
            v-model="searchQuery"
            :placeholder="currentMediaType === 'video' ? '搜索视频...' : '搜索音乐...'"
          >
        </div>
      </div>
      <div class="toolbar-right">
        <div class="group-filter">
          <select v-model="selectedGroupId" @change="loadMedia">
            <option :value="null">全部分组</option>
            <option v-for="group in groups" :key="group.id" :value="group.id">
              {{ group.name }}
            </option>
          </select>
        </div>
        <button class="upload-btn" @click="openUploadModal">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <span>上传{{ currentMediaType === 'video' ? '视频' : '音乐' }}</span>
        </button>
      </div>
    </div>

    <div v-if="filteredMedia.length > 0" class="media-grid">
      <div
        v-for="item in filteredMedia"
        :key="item.id"
        class="media-card"
      >
        <div class="media-thumbnail" @click="playMedia(item)">
          <div class="thumbnail-placeholder">
            <svg v-if="item.media_type === 'video'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
              <line x1="7" y1="2" x2="7" y2="22"/>
              <line x1="17" y1="2" x2="17" y2="22"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 18V5l12-2v13"/>
              <circle cx="6" cy="18" r="3"/>
              <circle cx="18" cy="16" r="3"/>
            </svg>
          </div>
          <div class="play-overlay">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </div>
          <span class="media-format">{{ item.format.toUpperCase() }}</span>
          <span v-if="item.group_name" class="media-group-badge">{{ item.group_name }}</span>
        </div>

        <div class="media-info">
          <h3 class="media-name" :title="item.original_name">{{ item.original_name }}</h3>
          <div class="media-meta">
            <span class="media-size">{{ formatSize(item.size) }}</span>
            <span class="media-date">{{ formatDate(item.created_at) }}</span>
          </div>
        </div>

        <div class="media-actions">
          <button class="action-btn group" @click="openGroupModal(item)" title="切换分组">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
          </button>
          <button class="action-btn edit" @click="editMedia(item)" title="修改名称">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="action-btn play" @click="playMedia(item)" title="播放">
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
    </div>

    <div v-else-if="!isLoading" class="empty-state">
      <div class="empty-icon">
        <svg v-if="currentMediaType === 'video'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
          <line x1="7" y1="2" x2="7" y2="22"/>
          <line x1="17" y1="2" x2="17" y2="22"/>
          <line x1="2" y1="12" x2="22" y2="12"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 18V5l12-2v13"/>
          <circle cx="6" cy="18" r="3"/>
          <circle cx="18" cy="16" r="3"/>
        </svg>
      </div>
      <h3>暂无{{ currentMediaType === 'video' ? '视频' : '音乐' }}</h3>
      <p>点击上方"上传{{ currentMediaType === 'video' ? '视频' : '音乐' }}"按钮添加您的第一个{{ currentMediaType === 'video' ? '视频' : '音乐' }}</p>
    </div>

    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-if="showUploadModal" class="modal-overlay" @click.self="closeUploadModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>上传{{ currentMediaType === 'video' ? '视频' : '音乐' }}</h3>
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
              :accept="currentMediaType === 'video' ? 'video/*' : 'audio/*'"
              hidden
              @change="handleFileSelect"
            >
            <div v-if="!selectedFile" class="upload-placeholder">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <p>点击或拖拽{{ currentMediaType === 'video' ? '视频' : '音乐' }}文件到此处</p>
              <span>{{ currentMediaType === 'video' ? '支持 MP4, WebM, AVI 等格式' : '支持 MP3, WAV, FLAC 等格式' }}</span>
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

          <div class="form-group">
            <label>选择分组</label>
            <select v-model="uploadGroupId">
              <option :value="null">不选择分组</option>
              <option v-for="group in groups" :key="group.id" :value="group.id">
                {{ group.name }}
              </option>
            </select>
          </div>

          <div v-if="uploadError" class="upload-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>{{ uploadError }}</span>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn secondary" @click="closeUploadModal">取消</button>
          <button
            class="btn primary"
            :disabled="!selectedFile || isUploading"
            @click="uploadMedia"
          >
            <span v-if="isUploading" class="btn-spinner"></span>
            <span v-else>开始上传</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>修改名称</h3>
          <button class="close-btn" @click="closeEditModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>{{ currentMediaType === 'video' ? '视频' : '音乐' }}名称</label>
            <input
              type="text"
              v-model="editForm.name"
              placeholder="请输入名称"
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

    <div v-if="showGroupModal" class="modal-overlay" @click.self="closeGroupModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>切换分组</h3>
          <button class="close-btn" @click="closeGroupModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <p class="modal-hint">为 "<strong>{{ mediaToChangeGroup?.original_name }}</strong>" 选择分组：</p>
          <div class="group-list">
            <div
              class="group-option"
              :class="{ selected: changeGroupId === null }"
              @click="changeGroupId = null"
            >
              <div class="group-option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="8" y1="12" x2="16" y2="12"/>
                </svg>
              </div>
              <span>不选择分组</span>
            </div>
            <div
              v-for="group in groups"
              :key="group.id"
              class="group-option"
              :class="{ selected: changeGroupId === group.id }"
              @click="changeGroupId = group.id"
            >
              <div class="group-option-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
              </div>
              <span>{{ group.name }}</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn secondary" @click="closeGroupModal">取消</button>
          <button
            class="btn primary"
            :disabled="isChangingGroup"
            @click="saveGroupChange"
          >
            <span v-if="isChangingGroup" class="btn-spinner"></span>
            <span v-else>确认</span>
          </button>
        </div>
      </div>
    </div>

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
          <p>确定要删除{{ currentMediaType === 'video' ? '视频' : '音乐' }} "<strong>{{ mediaToDelete?.original_name }}</strong>" 吗？</p>
          <p class="warning-text">此操作不可恢复，文件将被永久删除。</p>
        </div>

        <div class="modal-footer">
          <button class="btn secondary" @click="closeDeleteModal">取消</button>
          <button
            class="btn danger"
            :disabled="isDeleting"
            @click="deleteMedia"
          >
            <span v-if="isDeleting" class="btn-spinner"></span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showPlayerModal" class="modal-overlay player-overlay" @click.self="closePlayer">
      <div class="player-modal">
        <div class="player-header">
          <h3>{{ currentMedia?.original_name }}</h3>
          <button class="close-btn" @click="closePlayer">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="player-body">
          <VideoPlayer
            v-if="currentMedia"
            :url="getMediaUrl(currentMedia)"
            :format="currentMedia.format"
          />
        </div>
      </div>
    </div>

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

const currentMediaType = ref('video')
const mediaList = ref([])
const groups = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const selectedGroupId = ref(null)

const showUploadModal = ref(false)
const fileInput = ref(null)
const selectedFile = ref(null)
const isDragOver = ref(false)
const isUploading = ref(false)
const uploadError = ref('')
const uploadGroupId = ref(null)

const showEditModal = ref(false)
const mediaToEdit = ref(null)
const editForm = ref({ name: '' })
const isEditing = ref(false)

const showGroupModal = ref(false)
const mediaToChangeGroup = ref(null)
const changeGroupId = ref(null)
const isChangingGroup = ref(false)

const showDeleteModal = ref(false)
const mediaToDelete = ref(null)
const isDeleting = ref(false)

const showPlayerModal = ref(false)
const currentMedia = ref(null)

const toastMessage = ref('')
const toastType = ref('success')

const filteredMedia = computed(() => {
  if (!searchQuery.value.trim()) return mediaList.value
  const query = searchQuery.value.toLowerCase()
  return mediaList.value.filter(m => m.original_name.toLowerCase().includes(query))
})

onMounted(() => {
  loadGroups()
  loadMedia()
})

function switchMediaType(type) {
  currentMediaType.value = type
  selectedGroupId.value = null
  loadMedia()
}

async function loadGroups() {
  try {
    const response = await authStore.apiRequest('/groups')
    if (response.ok) {
      groups.value = await response.json()
    }
  } catch (err) {
    console.error('加载分组失败', err)
  }
}

async function loadMedia() {
  isLoading.value = true
  try {
    let url = `/videos?media_type=${currentMediaType.value}`
    if (selectedGroupId.value) {
      url += `&group_id=${selectedGroupId.value}`
    }
    const response = await authStore.apiRequest(url)
    if (response.ok) {
      mediaList.value = await response.json()
    } else {
      showToast('加载失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isLoading.value = false
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

function getMediaUrl(media) {
  return `${API_BASE}${media.url}`
}

function openUploadModal() {
  uploadGroupId.value = selectedGroupId.value
  showUploadModal.value = true
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) {
    validateFile(file)
  }
}

function handleFileDrop(e) {
  isDragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) {
    validateFile(file)
  }
}

function validateFile(file) {
  const expectedType = currentMediaType.value === 'video' ? 'video/' : 'audio/'
  if (!file.type.startsWith(expectedType)) {
    uploadError.value = currentMediaType.value === 'video' ? '请选择视频文件' : '请选择音乐文件'
    return
  }
  selectedFile.value = file
  uploadError.value = ''
}

async function uploadMedia() {
  if (!selectedFile.value) return

  isUploading.value = true
  uploadError.value = ''

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    if (uploadGroupId.value) {
      formData.append('group_id', uploadGroupId.value)
    }

    const response = await authStore.apiRequest('/videos', {
      method: 'POST',
      body: formData,
      headers: {}
    })

    if (response.ok) {
      const newMedia = await response.json()
      if (!selectedGroupId.value || selectedGroupId.value === uploadGroupId.value) {
        mediaList.value.unshift(newMedia)
      }
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
  uploadGroupId.value = null
}

function editMedia(media) {
  mediaToEdit.value = media
  editForm.value.name = media.original_name
  showEditModal.value = true
}

async function saveEdit() {
  if (!editForm.value.name.trim() || !mediaToEdit.value) return

  isEditing.value = true
  try {
    const response = await authStore.apiRequest(`/videos/${mediaToEdit.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ name: editForm.value.name.trim() })
    })

    if (response.ok) {
      const updated = await response.json()
      const index = mediaList.value.findIndex(m => m.id === updated.id)
      if (index !== -1) {
        mediaList.value[index] = updated
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
  mediaToEdit.value = null
  editForm.value.name = ''
}

function openGroupModal(media) {
  mediaToChangeGroup.value = media
  changeGroupId.value = media.group_id
  showGroupModal.value = true
}

async function saveGroupChange() {
  if (!mediaToChangeGroup.value) return

  isChangingGroup.value = true
  try {
    const url = `/videos/${mediaToChangeGroup.value.id}/group${changeGroupId.value ? `?group_id=${changeGroupId.value}` : ''}`
    const response = await authStore.apiRequest(url, {
      method: 'PUT'
    })

    if (response.ok) {
      const updated = await response.json()
      const index = mediaList.value.findIndex(m => m.id === updated.id)
      if (index !== -1) {
        mediaList.value[index] = updated
      }
      closeGroupModal()
      showToast('分组已更改', 'success')
    } else {
      const error = await response.json()
      showToast(error.detail || '操作失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isChangingGroup.value = false
  }
}

function closeGroupModal() {
  showGroupModal.value = false
  mediaToChangeGroup.value = null
  changeGroupId.value = null
}

function confirmDelete(media) {
  mediaToDelete.value = media
  showDeleteModal.value = true
}

async function deleteMedia() {
  if (!mediaToDelete.value) return

  isDeleting.value = true
  try {
    const response = await authStore.apiRequest(`/videos/${mediaToDelete.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      mediaList.value = mediaList.value.filter(m => m.id !== mediaToDelete.value.id)
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
  mediaToDelete.value = null
}

function playMedia(media) {
  currentMedia.value = media
  showPlayerModal.value = true
}

function closePlayer() {
  showPlayerModal.value = false
  currentMedia.value = null
}

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

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.media-tabs {
  display: flex;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  padding: 4px;

  .tab-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 16px;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: #94a3b8;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.25s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      color: #c7d2fe;
    }

    &.active {
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      color: white;
    }
  }
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 200px;
  max-width: 300px;

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

.group-filter {
  select {
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    cursor: pointer;
    transition: all 0.25s ease;

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
    }

    option {
      background: #1e293b;
      color: #f8fafc;
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

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.media-card {
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

.media-thumbnail {
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

  .media-format {
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

  .media-group-badge {
    position: absolute;
    top: 8px;
    left: 8px;
    padding: 4px 10px;
    background: rgba(99, 102, 241, 0.8);
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 500;
    color: white;
  }
}

.media-info {
  padding: 16px;

  .media-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .media-meta {
    display: flex;
    gap: 12px;
    font-size: 0.8rem;
    color: #64748b;
  }
}

.media-actions {
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
    transition: all 0.25s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #c7d2fe;
    }

    &.delete:hover {
      background: rgba(239, 68, 68, 0.1);
      color: #ef4444;
      border-color: rgba(239, 68, 68, 0.3);
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;

  .empty-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 20px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 50%;
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
  padding: 60px 20px;

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }

  p {
    color: #64748b;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-card {
  background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  width: 90%;
  max-width: 480px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
  }

  .close-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    color: #64748b;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.25s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #f8fafc;
    }

    svg {
      width: 20px;
      height: 20px;
    }
  }

  .warning-icon {
    width: 40px;
    height: 40px;
    background: rgba(239, 68, 68, 0.15);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;

    svg {
      width: 22px;
      height: 22px;
      color: #ef4444;
    }
  }
}

.modal-body {
  padding: 24px;

  .form-group {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }

    label {
      display: block;
      font-size: 0.9rem;
      font-weight: 500;
      color: #c7d2fe;
      margin-bottom: 8px;
    }

    input,
    select {
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
        color: #64748b;
      }

      &:focus {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
      }
    }

    select option {
      background: #1e293b;
      color: #f8fafc;
    }
  }

  .modal-hint {
    color: #94a3b8;
    margin-bottom: 16px;

    strong {
      color: #f8fafc;
    }
  }

  .group-list {
    max-height: 300px;
    overflow-y: auto;
  }

  .group-option {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(99, 102, 241, 0.1);
    border-radius: 10px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.25s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
    }

    &.selected {
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.5);
    }

    .group-option-icon {
      width: 32px;
      height: 32px;
      background: rgba(99, 102, 241, 0.15);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;

      svg {
        width: 18px;
        height: 18px;
        color: #a5b4fc;
      }
    }

    span {
      color: #f8fafc;
      font-size: 0.95rem;
    }
  }

  p {
    color: #94a3b8;
    line-height: 1.6;

    strong {
      color: #f8fafc;
    }
  }

  .warning-text {
    color: #f87171;
    font-size: 0.9rem;
    margin-top: 8px;
  }
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 12px;

  .btn {
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    &.secondary {
      background: transparent;
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #94a3b8;

      &:hover {
        background: rgba(99, 102, 241, 0.1);
        color: #f8fafc;
      }
    }

    &.primary {
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      border: none;
      color: white;

      &:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }

    &.danger {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      border: none;
      color: white;

      &:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }

    .btn-spinner {
      width: 16px;
      height: 16px;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-top-color: white;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
  }
}

.upload-area {
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease;
  margin-bottom: 20px;

  &:hover,
  &.drag-over {
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
      color: #f8fafc;
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
    gap: 16px;
    text-align: left;

    svg {
      width: 40px;
      height: 40px;
      color: #6366f1;
      flex-shrink: 0;
    }

    .file-info {
      flex: 1;
      min-width: 0;

      .file-name {
        display: block;
        color: #f8fafc;
        font-size: 0.95rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
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
      background: transparent;
      border: none;
      color: #64748b;
      cursor: pointer;
      border-radius: 6px;
      transition: all 0.25s ease;

      &:hover {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
      }

      svg {
        width: 18px;
        height: 18px;
      }
    }
  }
}

.upload-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;
  color: #f87171;
  font-size: 0.9rem;

  svg {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
  }
}

.player-overlay {
  background: rgba(0, 0, 0, 0.9);
}

.player-modal {
  background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  width: 90%;
  max-width: 900px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.player-header {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;

  h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #f8fafc;
  }
}

.player-body {
  padding: 0;
}

.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 14px 20px;
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #f8fafc;
  font-size: 0.95rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
  z-index: 1001;

  &.success {
    border-color: rgba(34, 197, 94, 0.3);

    svg {
      color: #22c55e;
    }
  }

  &.error {
    border-color: rgba(239, 68, 68, 0.3);

    svg {
      color: #ef4444;
    }
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
</style>
