<template>
  <div class="music-management">
    <div class="toolbar">
      <div class="view-toggle">
        <button class="toggle-btn" :class="{ active: viewMode === 'card' }" @click="viewMode = 'card'" title="卡片视图">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
          </svg>
        </button>
        <button class="toggle-btn" :class="{ active: viewMode === 'list' }" @click="viewMode = 'list'" title="列表视图">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
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
          placeholder="搜索音乐..."
        >
      </div>
      <div class="toolbar-actions">
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

    <div v-if="filteredMusic.length > 0 && viewMode === 'list'" class="music-list">
      <div class="list-header">
        <div class="header-icon"></div>
        <div class="header-name">名称</div>
        <div class="header-meta">大小</div>
        <div class="header-date">创建时间</div>
        <div class="header-group">分组</div>
        <div class="header-actions">操作</div>
      </div>
      <div
        v-for="music in filteredMusic"
        :key="music.id"
        class="list-row"
      >
        <div class="row-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 18V5l12-2v13"/>
            <circle cx="6" cy="18" r="3"/>
            <circle cx="18" cy="16" r="3"/>
          </svg>
        </div>
        <div class="row-name" :title="music.original_name">{{ music.original_name }}</div>
        <div class="row-meta">{{ formatSize(music.size) }}</div>
        <div class="row-date">{{ formatDate(music.created_at) }}</div>
        <div class="row-group">
          <span v-if="music.group_id" class="group-badge">{{ getGroupName(music.group_id) }}</span>
          <span v-else class="no-group">未分组</span>
        </div>
        <div class="row-actions">
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

    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <MusicUploadModal
      :show="showUploadModal"
      :music-groups="musicGroups"
      :is-uploading="isUploading"
      @close="closeUploadModal"
      @upload="({ file, groupId }) => uploadMusic(file, groupId)"
    />

    <MusicEditModal
      :show="showEditModal"
      :music="musicToEdit"
      :is-loading="isEditing"
      @close="closeEditModal"
      @save="saveEdit"
    />

    <MusicChangeGroupModal
      :show="showChangeGroupModal"
      :music="musicToChangeGroup"
      :groups="musicGroups"
      :is-loading="isChangingGroup"
      @close="closeChangeGroupModal"
      @save="saveChangeGroup"
    />

    <MusicDeleteModal
      :show="showDeleteModal"
      :music="musicToDelete"
      :is-loading="isDeleting"
      @close="closeDeleteModal"
      @confirm="deleteMusic"
    />

    <MusicPlayerModal
      :show="showPlayerModal"
      :music="currentMusic"
      :get-music-url="getMusicUrl"
      @close="closePlayer"
    />

    <div v-if="toastMessage" class="toast" :class="toastType">
      <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="17" x2="12.01" y2="17"/>
      </svg>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { useMusicManagement } from '@/composables/useMusicManagement.js'
import { formatSize, formatDate } from '@/utils/format.js'
import MusicUploadModal from '@/components/music/MusicUploadModal.vue'
import MusicEditModal from '@/components/music/MusicEditModal.vue'
import MusicChangeGroupModal from '@/components/music/MusicChangeGroupModal.vue'
import MusicDeleteModal from '@/components/music/MusicDeleteModal.vue'
import MusicPlayerModal from '@/components/music/MusicPlayerModal.vue'

const {
  musicList,
  musicGroups,
  isLoading,
  selectedGroupId,
  searchQuery,
  viewMode,
  filteredMusic,
  toastMessage,
  toastType,
  showUploadModal,
  showEditModal,
  showChangeGroupModal,
  showDeleteModal,
  showPlayerModal,
  isUploading,
  musicToEdit,
  isEditing,
  musicToChangeGroup,
  isChangingGroup,
  musicToDelete,
  isDeleting,
  currentMusic,
  loadMusic,
  getGroupName,
  getMusicUrl,
  editMusic,
  saveEdit,
  closeEditModal,
  showChangeGroup,
  saveChangeGroup,
  closeChangeGroupModal,
  confirmDelete,
  deleteMusic,
  closeDeleteModal,
  playMusic,
  closePlayer,
  uploadMusic,
  closeUploadModal
} = useMusicManagement()
</script>

<style lang="scss" scoped>
.music-management {
  min-height: 100%;
}

.view-toggle {
  display: flex;
  gap: 8px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  padding: 4px;

  .toggle-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #f8fafc;
    }

    &.active {
      background: rgba(99, 102, 241, 0.2);
      color: #f8fafc;
    }
  }
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
  padding: 20px;
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
  width: 64px;
  height: 64px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  svg {
    width: 32px;
    height: 32px;
    color: #10b981;
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
    font-size: 0.95rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .music-meta {
    display: flex;
    gap: 12px;
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 6px;
  }

  .music-group {
    .group-badge {
      display: inline-block;
      padding: 2px 8px;
      background: rgba(16, 185, 129, 0.15);
      border-radius: 4px;
      font-size: 0.75rem;
      color: #34d399;
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
  background: rgba(30, 41, 59, 0.4);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(99, 102, 241, 0.1);
}

.list-header {
  display: grid;
  grid-template-columns: 64px 1fr 100px 150px 120px 160px;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.6);
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 500;
}

.list-row {
  display: grid;
  grid-template-columns: 64px 1fr 100px 150px 120px 160px;
  gap: 16px;
  padding: 16px 20px;
  align-items: center;
  border-bottom: 1px solid rgba(99, 102, 241, 0.05);
  transition: background 0.2s ease;

  &:hover {
    background: rgba(99, 102, 241, 0.05);
  }

  &:last-child {
    border-bottom: none;
  }
}

.row-icon {
  width: 40px;
  height: 40px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 20px;
    height: 20px;
    color: #10b981;
  }
}

.row-name {
  color: #f8fafc;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-meta {
  color: #64748b;
  font-size: 0.9rem;
}

.row-date {
  color: #64748b;
  font-size: 0.9rem;
}

.row-group {
  .group-badge {
    display: inline-block;
    padding: 2px 8px;
    background: rgba(16, 185, 129, 0.15);
    border-radius: 4px;
    font-size: 0.75rem;
    color: #34d399;
  }

  .no-group {
    color: #64748b;
    font-size: 0.85rem;
  }
}

.row-actions {
  display: flex;
  gap: 8px;

  .action-btn {
    width: 32px;
    height: 32px;
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
      width: 14px;
      height: 14px;
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

@media (max-width: 768px) {
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

  .list-header, .list-row {
    grid-template-columns: 40px 1fr 80px 1fr;
    .header-meta, .header-group, .row-meta, .row-group {
      display: none;
    }
  }
}
</style>
