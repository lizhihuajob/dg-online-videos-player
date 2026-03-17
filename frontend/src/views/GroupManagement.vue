<template>
  <div class="group-management">
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="M21 21l-4.35-4.35"/>
        </svg>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索分组..."
        >
      </div>
      <button class="create-btn" @click="showCreateModal = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>新建分组</span>
      </button>
    </div>

    <div v-if="filteredGroups.length > 0" class="group-grid">
      <div
        v-for="group in filteredGroups"
        :key="group.id"
        class="group-card"
      >
        <div class="group-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <div class="group-info">
          <h3 class="group-name">{{ group.name }}</h3>
          <p class="group-desc" v-if="group.description">{{ group.description }}</p>
          <span class="group-date">{{ formatDate(group.created_at) }}</span>
        </div>
        <div class="group-actions">
          <button class="action-btn edit" @click="editGroup(group)" title="编辑">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button class="action-btn delete" @click="confirmDelete(group)" title="删除">
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
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
        </svg>
      </div>
      <h3>暂无分组</h3>
      <p>点击上方"新建分组"按钮创建您的第一个分组</p>
    </div>

    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeCreateModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>新建分组</h3>
          <button class="close-btn" @click="closeCreateModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>分组名称 <span class="required">*</span></label>
            <input
              type="text"
              v-model="createForm.name"
              placeholder="请输入分组名称"
            >
          </div>
          <div class="form-group">
            <label>分组描述</label>
            <textarea
              v-model="createForm.description"
              placeholder="请输入分组描述（可选）"
              rows="3"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="closeCreateModal">取消</button>
          <button
            class="btn primary"
            :disabled="!createForm.name.trim() || isCreating"
            @click="createGroup"
          >
            <span v-if="isCreating" class="btn-spinner"></span>
            <span v-else>创建</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>编辑分组</h3>
          <button class="close-btn" @click="closeEditModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>分组名称 <span class="required">*</span></label>
            <input
              type="text"
              v-model="editForm.name"
              placeholder="请输入分组名称"
            >
          </div>
          <div class="form-group">
            <label>分组描述</label>
            <textarea
              v-model="editForm.description"
              placeholder="请输入分组描述（可选）"
              rows="3"
            ></textarea>
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
          <p>确定要删除分组 "<strong>{{ groupToDelete?.name }}</strong>" 吗？</p>
          <p class="warning-text">该分组下的媒体文件将移至"未分组"状态。</p>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="closeDeleteModal">取消</button>
          <button
            class="btn danger"
            :disabled="isDeleting"
            @click="deleteGroup"
          >
            <span v-if="isDeleting" class="btn-spinner"></span>
            <span v-else>确认删除</span>
          </button>
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

const authStore = useAuthStore()

const groups = ref([])
const isLoading = ref(false)
const searchQuery = ref('')

const showCreateModal = ref(false)
const createForm = ref({ name: '', description: '' })
const isCreating = ref(false)

const showEditModal = ref(false)
const groupToEdit = ref(null)
const editForm = ref({ name: '', description: '' })
const isEditing = ref(false)

const showDeleteModal = ref(false)
const groupToDelete = ref(null)
const isDeleting = ref(false)

const toastMessage = ref('')
const toastType = ref('success')

const filteredGroups = computed(() => {
  if (!searchQuery.value.trim()) return groups.value
  const query = searchQuery.value.toLowerCase()
  return groups.value.filter(g => g.name.toLowerCase().includes(query))
})

onMounted(() => {
  loadGroups()
})

async function loadGroups() {
  isLoading.value = true
  try {
    const response = await authStore.apiRequest('/groups')
    if (response.ok) {
      groups.value = await response.json()
    } else {
      showToast('加载分组失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isLoading.value = false
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

async function createGroup() {
  if (!createForm.value.name.trim()) return

  isCreating.value = true
  try {
    const response = await authStore.apiRequest('/groups', {
      method: 'POST',
      body: JSON.stringify({
        name: createForm.value.name.trim(),
        description: createForm.value.description.trim() || null
      })
    })

    if (response.ok) {
      const newGroup = await response.json()
      groups.value.unshift(newGroup)
      closeCreateModal()
      showToast('创建成功', 'success')
    } else {
      const error = await response.json()
      showToast(error.detail || '创建失败', 'error')
    }
  } catch (err) {
    showToast('网络错误', 'error')
  } finally {
    isCreating.value = false
  }
}

function closeCreateModal() {
  showCreateModal.value = false
  createForm.value = { name: '', description: '' }
}

function editGroup(group) {
  groupToEdit.value = group
  editForm.value = { name: group.name, description: group.description || '' }
  showEditModal.value = true
}

async function saveEdit() {
  if (!editForm.value.name.trim() || !groupToEdit.value) return

  isEditing.value = true
  try {
    const response = await authStore.apiRequest(`/groups/${groupToEdit.value.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        name: editForm.value.name.trim(),
        description: editForm.value.description.trim() || null
      })
    })

    if (response.ok) {
      const updatedGroup = await response.json()
      const index = groups.value.findIndex(g => g.id === updatedGroup.id)
      if (index !== -1) {
        groups.value[index] = updatedGroup
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
  groupToEdit.value = null
  editForm.value = { name: '', description: '' }
}

function confirmDelete(group) {
  groupToDelete.value = group
  showDeleteModal.value = true
}

async function deleteGroup() {
  if (!groupToDelete.value) return

  isDeleting.value = true
  try {
    const response = await authStore.apiRequest(`/groups/${groupToDelete.value.id}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      groups.value = groups.value.filter(g => g.id !== groupToDelete.value.id)
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
  groupToDelete.value = null
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
.group-management {
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

.create-btn {
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

.group-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.group-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 12px 40px -10px rgba(99, 102, 241, 0.2);
  }
}

.group-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  svg {
    width: 24px;
    height: 24px;
    color: #a5b4fc;
  }
}

.group-info {
  flex: 1;
  min-width: 0;

  .group-name {
    font-size: 1rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .group-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .group-date {
    font-size: 0.75rem;
    color: #64748b;
  }
}

.group-actions {
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
      width: 16px;
      height: 16px;
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

      .required {
        color: #ef4444;
      }
    }

    input,
    textarea {
      width: 100%;
      padding: 12px 16px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 10px;
      color: #f8fafc;
      font-size: 0.95rem;
      outline: none;
      transition: all 0.25s ease;
      resize: none;

      &::placeholder {
        color: #64748b;
      }

      &:focus {
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
      }
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
