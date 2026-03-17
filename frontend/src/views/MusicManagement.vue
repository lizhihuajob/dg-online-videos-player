<template>
  <div class="music-management">
    <!-- Toast Notification -->
    <Transition name="toast">
      <div v-if="toastMessage" :class="['toast', toastType]">
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
    </Transition>

    <!-- Header -->
    <div class="page-header">
      <h1 class="page-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 18V5l12-2v13"/>
          <circle cx="6" cy="18" r="3"/>
          <circle cx="18" cy="16" r="3"/>
        </svg>
        音乐管理
      </h1>
      <p class="page-subtitle">管理您的音乐文件</p>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索音乐..."
          @input="handleSearch"
        >
      </div>

      <div class="toolbar-actions">
        <select v-model="selectedGroupId" class="filter-select" @change="loadMusic">
          <option :value="null">全部分组</option>
          <option v-for="group in musicGroups" :key="group.id" :value="group.id">
            {{ group.name }}
          </option>
        </select>
        <button class="view-toggle-btn" @click="toggleViewMode" :title="viewMode === 'card' ? '切换列表视图' : '切换卡片视图'">
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

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Music Grid (Card View) -->
    <div v-else-if="filteredMusic.length > 0 && viewMode === 'card'" class="music-grid">
      <MusicCard
        v-for="music in filteredMusic"
        :key="music.id"
        :music="music"
        :group-name="getGroupName(music.group_id)"
        @edit="editMusic"
        @change-group="showChangeGroup"
        @play="playMusic"
        @delete="confirmDelete"
      />
    </div>

    <!-- Music List (List View) -->
    <MusicList
      v-else-if="filteredMusic.length > 0 && viewMode === 'list'"
      :music-list="filteredMusic"
      :get-group-name="getGroupName"
      @edit="editMusic"
      @change-group="showChangeGroup"
      @play="playMusic"
      @delete="confirmDelete"
    />

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 18V5l12-2v13"/>
          <circle cx="6" cy="18" r="3"/>
          <circle cx="18" cy="16" r="3"/>
        </svg>
      </div>
      <h3>暂无音乐</h3>
      <p>{{ searchQuery ? '没有找到匹配的音乐' : '还没有上传任何音乐文件' }}</p>
      <button v-if="!searchQuery" class="empty-action" @click="showUploadModal = true">
        上传音乐
      </button>
    </div>

    <!-- Upload Modal -->
    <UploadModal
      v-if="showUploadModal"
      :groups="musicGroups"
      :is-uploading="isUploading"
      @close="showUploadModal = false"
      @upload="handleUpload"
    />

    <!-- Edit Modal -->
    <EditModal
      v-if="showEditModal"
      :music="selectedMusic"
      :is-saving="isSaving"
      @close="showEditModal = false"
      @save="handleEdit"
    />

    <!-- Group Modal -->
    <GroupModal
      v-if="showGroupModal"
      :music="selectedMusic"
      :groups="musicGroups"
      :is-saving="isSaving"
      @close="showGroupModal = false"
      @save="handleChangeGroup"
    />

    <!-- Delete Modal -->
    <DeleteModal
      v-if="showDeleteModal"
      :music="selectedMusic"
      :is-deleting="isDeleting"
      @close="showDeleteModal = false"
      @confirm="handleDelete"
    />

    <!-- Music Player -->
    <MusicPlayer
      v-if="showPlayerModal"
      :music="selectedMusic"
      @close="showPlayerModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import MusicCard from '@/components/music/MusicCard.vue'
import MusicList from '@/components/music/MusicList.vue'
import UploadModal from '@/components/music/UploadModal.vue'
import EditModal from '@/components/music/EditModal.vue'
import GroupModal from '@/components/music/GroupModal.vue'
import DeleteModal from '@/components/music/DeleteModal.vue'
import MusicPlayer from '@/components/music/MusicPlayer.vue'

const authStore = useAuthStore()

// State
const musicList = ref([])
const musicGroups = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const selectedGroupId = ref(null)
const viewMode = ref('card')

// Modal states
const showUploadModal = ref(false)
const isUploading = ref(false)
const showEditModal = ref(false)
const showGroupModal = ref(false)
const showDeleteModal = ref(false)
const showPlayerModal = ref(false)
const selectedMusic = ref(null)
const isSaving = ref(false)
const isDeleting = ref(false)

// Toast
const toastMessage = ref('')
const toastType = ref('success')

// Computed
const filteredMusic = computed(() => {
  if (!searchQuery.value) return musicList.value
  const query = searchQuery.value.toLowerCase()
  return musicList.value.filter(music =>
    music.original_name.toLowerCase().includes(query)
  )
})

// Lifecycle
onMounted(() => {
  loadMusic()
  loadGroups()
})

// Methods
async function loadMusic() {
  isLoading.value = true
  try {
    const params = new URLSearchParams()
    if (selectedGroupId.value) {
      params.append('group_id', selectedGroupId.value)
    }
    const response = await authStore.apiRequest(`/music?${params}`)
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
    const response = await authStore.apiRequest('/groups?type=music')
    if (response.ok) {
      musicGroups.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load groups:', err)
  }
}

function getGroupName(groupId) {
  if (!groupId) return null
  const group = musicGroups.value.find(g => g.id === groupId)
  return group ? group.name : null
}

function handleSearch() {
  // Search is handled by computed property
}

function toggleViewMode() {
  viewMode.value = viewMode.value === 'card' ? 'list' : 'card'
}

async function handleUpload({ file, groupId }) {
  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    if (groupId) {
      formData.append('group_id', groupId)
    }

    const response = await authStore.apiRequest('/music', {
      method: 'POST',
      body: formData,
      headers: {}
    })

    if (response.ok) {
      showUploadModal.value = false
      showToast('上传成功')
      loadMusic()
    } else {
      const error = await response.json()
      showToast(error.detail || '上传失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isUploading.value = false
  }
}

function editMusic(music) {
  selectedMusic.value = music
  showEditModal.value = true
}

async function handleEdit(newName) {
  if (!selectedMusic.value) return

  isSaving.value = true
  try {
    const response = await authStore.apiRequest(`/music/${selectedMusic.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({ original_name: newName })
    })

    if (response.ok) {
      showEditModal.value = false
      showToast('修改成功')
      loadMusic()
    } else {
      const error = await response.json()
      showToast(error.detail || '修改失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isSaving.value = false
  }
}

function showChangeGroup(music) {
  selectedMusic.value = music
  showGroupModal.value = true
}

async function handleChangeGroup(groupId) {
  if (!selectedMusic.value) return

  isSaving.value = true
  try {
    const response = await authStore.apiRequest(`/music/${selectedMusic.value.id}/group`, {
      method: 'PUT',
      body: JSON.stringify({ group_id: groupId })
    })

    if (response.ok) {
      showGroupModal.value = false
      showToast('分组切换成功')
      loadMusic()
    } else {
      const error = await response.json()
      showToast(error.detail || '切换分组失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isSaving.value = false
  }
}

function playMusic(music) {
  selectedMusic.value = music
  showPlayerModal.value = true
}

function confirmDelete(music) {
  selectedMusic.value = music
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!selectedMusic.value) return

  isDeleting.value = true
  try {
    const response = await authStore.apiRequest(`/music/${selectedMusic.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      showDeleteModal.value = false
      showToast('删除成功')
      loadMusic()
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
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

// Toast
.toast {
  position: fixed;
  top: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  color: #f8fafc;
  font-weight: 500;
  z-index: 2000;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);

  svg {
    width: 20px;
    height: 20px;
  }

  &.success {
    border-color: rgba(16, 185, 129, 0.3);
    svg { color: #10b981; }
  }

  &.error {
    border-color: rgba(239, 68, 68, 0.3);
    svg { color: #ef4444; }
  }
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

// Header
.page-header {
  margin-bottom: 32px;

  .page-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.75rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;

    svg {
      width: 32px;
      height: 32px;
      color: #10b981;
    }
  }

  .page-subtitle {
    color: #64748b;
    font-size: 0.95rem;
  }
}

// Toolbar
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
  max-width: 400px;

  .search-icon {
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
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.25s ease;

    &::placeholder {
      color: #475569;
    }

    &:focus {
      border-color: rgba(99, 102, 241, 0.4);
      background: rgba(30, 41, 59, 0.8);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
  }
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-select {
  padding: 12px 36px 12px 16px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  color: #f8fafc;
  font-size: 0.9rem;
  outline: none;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  transition: all 0.25s ease;

  &:focus {
    border-color: rgba(99, 102, 241, 0.4);
  }
}

.view-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.4);
    color: #f8fafc;
  }

  svg {
    width: 20px;
    height: 20px;
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

// Loading State
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: #64748b;

  .spinner {
    width: 48px;
    height: 48px;
    border: 3px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 16px;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

// Music Grid
.music-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

// Empty State
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;

  .empty-icon {
    width: 80px;
    height: 80px;
    background: rgba(16, 185, 129, 0.1);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;

    svg {
      width: 40px;
      height: 40px;
      color: #10b981;
      opacity: 0.6;
    }
  }

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
  }

  p {
    color: #64748b;
    margin-bottom: 24px;
  }

  .empty-action {
    padding: 12px 24px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border: none;
    border-radius: 10px;
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
  }
}

@media (max-width: 768px) {
  .music-management {
    padding: 16px;
  }

  .music-grid {
    grid-template-columns: 1fr;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: none;
  }

  .toolbar-actions {
    justify-content: space-between;
  }
}
</style>
