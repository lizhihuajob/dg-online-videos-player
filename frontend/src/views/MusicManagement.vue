<template>
  <div class="music-management">
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
          placeholder="搜索音乐..."
        >
      </div>
      <div class="toolbar-actions">
        <button class="view-toggle-btn" @click="viewMode = viewMode === 'card' ? 'list' : 'card'" :title="viewMode === 'card' ? '切换到列表视图' : '切换到卡片视图'">
          <svg v-if="viewMode === 'card'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"/>
            <line x1="8" y1="12" x2="21" y2="12"/>
            <line x1="8" y1="18" x2="21" y2="18"/>
            <line x1="3" y1="6" x2="3.01" y2="6"/>
            <line x1="3" y1="12" x2="3.01" y2="12"/>
            <line x1="3" y1="18" x2="3.01" y2="18"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
        </button>
        <select v-model="selectedGroupId" class="filter-select" @change="loadMusic">
          <option :value="null">全部分组</option>
          <option v-for="group in musicGroups" :key="group.id" :value="group.id">
            {{ group.name }}
          </option>
        </select>
        <button class="upload-btn" @click="showUploadModal = true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18V5l12-2v13"/>
            <circle cx="6" cy="18" r="3"/>
            <circle cx="18" cy="16" r="3"/>
          </svg>
          <span>上传音乐</span>
        </button>
      </div>
    </div>

    <!-- Music Grid -->
    <div v-if="filteredMusic.length > 0 && viewMode === 'card'" class="music-grid">
      <div
        v-for="music in filteredMusic"
        :key="music.id"
        class="music-card"
      >
        <div class="music-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 18V5l12-2v13"/>
            <circle cx="6" cy="18" r="3"/>
            <circle cx="18" cy="16" r="3"/>
          </svg>
        </div>

        <div class="music-content">
          <div class="music-info">
            <h3 class="music-name" :title="music.original_name">{{ music.original_name }}</h3>
            <div class="music-meta">
              <span class="music-size">{{ formatSize(music.size) }}</span>
              <span class="music-date">{{ formatDate(music.created_at) }}</span>
            </div>
            <div v-if="music.group_id" class="music-group">
              <span class="group-badge">{{ getGroupName(music.group_id) }}</span>
            </div>
          </div>

          <div class="music-actions">
            <button class="action-btn edit" @click="editMusic(music)" title="修改名称">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="action-btn group" @click="showChangeGroup(music)" title="切换分组">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
            </button>
            <button class="action-btn play" @click="playMusic(music)" title="播放">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5 3 19 12 5 21 5 3"/>
              </svg>
            </button>
            <button class="action-btn delete" @click="confirmDelete(music)" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Music List -->
    <div v-if="filteredMusic.length > 0 && viewMode === 'list'" class="music-list">
      <div
        v-for="music in filteredMusic"
        :key="music.id"
        class="music-list-item"
      >
        <div class="list-item-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 18V5l12-2v13"/>
            <circle cx="6" cy="18" r="3"/>
            <circle cx="18" cy="16" r="3"/>
          </svg>
        </div>
        <div class="list-item-info">
          <h3 class="list-item-name" :title="music.original_name">{{ music.original_name }}</h3>
          <div class="list-item-meta">
            <span class="list-item-format">{{ music.format?.toUpperCase() || 'AUDIO' }}</span>
            <span class="list-item-size">{{ formatSize(music.size) }}</span>
            <span class="list-item-date">{{ formatDate(music.created_at) }}</span>
            <span v-if="music.group_id" class="list-item-group">{{ getGroupName(music.group_id) }}</span>
          </div>
        </div>
        <div class="list-item-actions">
          <button class="action-btn edit" @click="editMusic(music)" title="修改名称">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="action-btn group" @click="showChangeGroup(music)" title="切换分组">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
          </button>
          <button class="action-btn play" @click="playMusic(music)" title="播放">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
          </button>
          <button class="action-btn delete" @click="confirmDelete(music)" title="删除">
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
          <path d="M9 18V5l12-2v13"/>
          <circle cx="6" cy="18" r="3"/>
          <circle cx="18" cy="16" r="3"/>
        </svg>
      </div>
      <h3>暂无音乐</h3>
      <p>点击上方"上传音乐"按钮添加您的第一个音乐</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Modals -->
    <MusicUploadModal
      :show="showUploadModal"
      :groups="musicGroups"
      @close="showUploadModal = false"
      @upload="handleUpload"
    />

    <MusicEditModal
      :show="showEditModal"
      :music="musicToEdit"
      @close="closeEditModal"
      @save="handleEditSave"
    />

    <MusicChangeGroupModal
      :show="showChangeGroupModal"
      :music="musicToChangeGroup"
      :groups="musicGroups"
      @close="closeChangeGroupModal"
      @save="handleChangeGroupSave"
    />

    <MusicDeleteModal
      :show="showDeleteModal"
      :music="musicToDelete"
      @close="closeDeleteModal"
      @confirm="handleDeleteConfirm"
    />

    <MusicPlayerModal
      :show="showPlayerModal"
      :music="currentMusic"
      :api-base="API_BASE"
      @close="closePlayer"
    />

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
import MusicUploadModal from '@/components/MusicUploadModal.vue'
import MusicEditModal from '@/components/MusicEditModal.vue'
import MusicChangeGroupModal from '@/components/MusicChangeGroupModal.vue'
import MusicDeleteModal from '@/components/MusicDeleteModal.vue'
import MusicPlayerModal from '@/components/MusicPlayerModal.vue'

const API_BASE = 'http://localhost:8000'
const authStore = useAuthStore()

const musicList = ref([])
const musicGroups = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const selectedGroupId = ref(null)
const viewMode = ref('card')

const showUploadModal = ref(false)
const showEditModal = ref(false)
const musicToEdit = ref(null)
const showChangeGroupModal = ref(false)
const musicToChangeGroup = ref(null)
const showDeleteModal = ref(false)
const musicToDelete = ref(null)
const showPlayerModal = ref(false)
const currentMusic = ref(null)

const toastMessage = ref('')
const toastType = ref('success')

const filteredMusic = computed(() => {
  if (!searchQuery.value.trim()) return musicList.value
  const query = searchQuery.value.toLowerCase()
  return musicList.value.filter(m => m.original_name.toLowerCase().includes(query))
})

onMounted(() => {
  loadMusic()
  loadGroups()
})

async function loadMusic() {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    params.append('file_type', 'music')
    if (selectedGroupId.value) {
      params.append('group_id', selectedGroupId.value)
    }
    const response = await authStore.apiRequest(`/videos?${params.toString()}`)
    if (response.ok) {
      musicList.value = await response.json()
    } else {
      showToast('加载音乐失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isLoading.value = false
  }
}

async function loadGroups() {
  try {
    const response = await authStore.apiRequest('/groups?group_type=music')
    if (response.ok) {
      musicGroups.value = await response.json()
    }
  } catch (err) {
    console.error('加载分组失败', err)
  }
}

function getGroupName(groupId) {
  const group = musicGroups.value.find(g => g.id === groupId)
  return group ? group.name : ''
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

async function handleUpload({ file, groupId, onSuccess, onError, onFinally }) {
  try {
    const formData = new FormData()
    formData.append('file', file)
    if (groupId) {
      formData.append('group_id', groupId)
    }

    const response = await authStore.apiRequest('/videos', {
      method: 'POST',
      body: formData,
      headers: {}
    })

    if (response.ok) {
      const newMusic = await response.json()
      musicList.value.unshift(newMusic)
      showToast('上传成功', 'success')
      onSuccess()
    } else {
      const error = await response.json()
      onError(error.detail || '上传失败')
    }
  } catch (err) {
    onError('网络错误')
  } finally {
    onFinally()
  }
}

function editMusic(music) {
  musicToEdit.value = music
  showEditModal.value = true
}

async function handleEditSave({ name, onFinally }) {
  if (!musicToEdit.value) return

  try {
    const response = await authStore.apiRequest(`/videos/${musicToEdit.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ name })
    })

    if (response.ok) {
      const updatedMusic = await response.json()
      const index = musicList.value.findIndex(m => m.id === updatedMusic.id)
      if (index !== -1) {
        musicList.value[index] = updatedMusic
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
    onFinally()
  }
}

function closeEditModal() {
  showEditModal.value = false
  musicToEdit.value = null
}

function showChangeGroup(music) {
  musicToChangeGroup.value = music
  showChangeGroupModal.value = true
}

async function handleChangeGroupSave({ groupId, onFinally }) {
  if (!musicToChangeGroup.value) return

  try {
    const response = await authStore.apiRequest(`/videos/${musicToChangeGroup.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ group_id: groupId })
    })

    if (response.ok) {
      const updatedMusic = await response.json()
      const index = musicList.value.findIndex(m => m.id === updatedMusic.id)
      if (index !== -1) {
        musicList.value[index] = updatedMusic
      }
      closeChangeGroupModal()
      showToast('分组切换成功', 'success')
    } else {
      const error = await response.json()
      showToast(error.detail || '切换分组失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    onFinally()
  }
}

function closeChangeGroupModal() {
  showChangeGroupModal.value = false
  musicToChangeGroup.value = null
}

function confirmDelete(music) {
  musicToDelete.value = music
  showDeleteModal.value = true
}

async function handleDeleteConfirm({ onFinally }) {
  if (!musicToDelete.value) return

  try {
    const response = await authStore.apiRequest(`/videos/${musicToDelete.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      musicList.value = musicList.value.filter(m => m.id !== musicToDelete.value.id)
      closeDeleteModal()
      showToast('删除成功', 'success')
    } else {
      const error = await response.json()
      showToast(error.detail || '删除失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    onFinally()
  }
}

function closeDeleteModal() {
  showDeleteModal.value = false
  musicToDelete.value = null
}

function playMusic(music) {
  currentMusic.value = music
  showPlayerModal.value = true
}

function closePlayer() {
  showPlayerModal.value = false
  currentMusic.value = null
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
.music-management {
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

.toolbar-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.view-toggle-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.3);
    color: #f8fafc;
  }

  svg {
    width: 20px;
    height: 20px;
  }
}

.filter-select {
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  color: #f8fafc;
  font-size: 0.95rem;
  outline: none;
  cursor: pointer;

  &:focus {
    border-color: rgba(99, 102, 241, 0.5);
  }

  option {
    background: #1e293b;
    color: #f8fafc;
  }
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 15px -3px rgba(16, 185, 129, 0.4);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px -5px rgba(16, 185, 129, 0.5);
  }

  svg {
    width: 18px;
    height: 18px;
  }
}

.music-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.music-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 12px 40px -10px rgba(99, 102, 241, 0.2);
  }
}

.music-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;

  svg {
    width: 28px;
    height: 28px;
  }
}

.music-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.music-info {
  .music-name {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .music-meta {
    display: flex;
    gap: 12px;
    font-size: 0.8rem;
    color: #64748b;
  }

  .music-group {
    margin-top: 4px;

    .group-badge {
      padding: 2px 8px;
      background: rgba(16, 185, 129, 0.1);
      border-radius: 4px;
      color: #34d399;
      font-size: 0.75rem;
    }
  }
}

.music-actions {
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
    border-radius: 10px;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;

    svg {
      width: 16px;
      height: 16px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
    }

    &.edit:hover {
      color: #6366f1;
    }

    &.group:hover {
      color: #8b5cf6;
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

.music-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.music-list-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  transition: all 0.3s ease;

  &:hover {
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 4px 20px -5px rgba(99, 102, 241, 0.15);
  }

  .list-item-icon {
    width: 48px;
    height: 48px;
    background: rgba(16, 185, 129, 0.15);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    svg {
      width: 24px;
      height: 24px;
      color: #10b981;
    }
  }

  .list-item-info {
    flex: 1;
    min-width: 0;

    .list-item-name {
      font-size: 0.95rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .list-item-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.8rem;
      color: #64748b;

      .list-item-format {
        padding: 2px 8px;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 4px;
        color: #34d399;
      }

      .list-item-group {
        padding: 2px 8px;
        background: rgba(99, 102, 241, 0.1);
        border-radius: 4px;
        color: #a5b4fc;
      }
    }
  }

  .list-item-actions {
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
        border-color: rgba(99, 102, 241, 0.3);
      }

      &.edit:hover {
        color: #6366f1;
      }

      &.group:hover {
        color: #8b5cf6;
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
}

.empty-state {
  text-align: center;
  padding: 80px 20px;

  .empty-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    background: rgba(16, 185, 129, 0.1);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      width: 40px;
      height: 40px;
      color: #10b981;
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
</style>
