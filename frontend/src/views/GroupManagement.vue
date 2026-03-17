<template>
  <div class="group-management">
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
          placeholder="搜索分组..."
        >
      </div>
      <div class="toolbar-actions">
        <select v-model="filterType" class="filter-select">
          <option value="">全部分组</option>
          <option value="video">视频分组</option>
          <option value="music">音乐分组</option>
        </select>
        <button class="upload-btn" @click="showCreateModal = true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            <line x1="12" y1="11" x2="12" y2="17"/>
            <line x1="9" y1="14" x2="15" y2="14"/>
          </svg>
          <span>创建分组</span>
        </button>
      </div>
    </div>

    <!-- Group Table -->
    <div v-if="filteredGroups.length > 0" class="group-table-container">
      <table class="group-table">
        <thead>
          <tr>
            <th>分组名称</th>
            <th>类型</th>
            <th>描述</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="group in filteredGroups"
            :key="group.id"
            class="group-row"
          >
            <td class="group-name-cell">
              <div class="group-icon-wrapper">
                <div class="group-icon" :class="group.group_type">
                  <svg v-if="group.group_type === 'video'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
                    <line x1="7" y1="2" x2="7" y2="22"/>
                    <line x1="17" y1="2" x2="17" y2="22"/>
                    <line x1="2" y1="12" x2="22" y2="12"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 18V5l12-2v13"/>
                    <circle cx="6" cy="18" r="3"/>
                    <circle cx="18" cy="16" r="3"/>
                  </svg>
                </div>
                <span class="group-name" :title="group.name">{{ group.name }}</span>
              </div>
            </td>
            <td>
              <span class="group-type-badge" :class="group.group_type">{{ group.group_type === 'video' ? '视频' : '音乐' }}</span>
            </td>
            <td class="group-description-cell">
              <span :title="group.description">{{ group.description || '-' }}</span>
            </td>
            <td class="group-date-cell">{{ formatDate(group.created_at) }}</td>
            <td class="group-actions-cell">
              <button class="action-btn edit" @click="editGroup(group)" title="修改">
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
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoading" class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
        </svg>
      </div>
      <h3>暂无分组</h3>
      <p>点击上方"创建分组"按钮添加您的第一个分组</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeCreateModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>创建分组</h3>
          <button class="close-btn" @click="closeCreateModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>分组名称 *</label>
            <input
              type="text"
              v-model="createForm.name"
              placeholder="请输入分组名称"
            >
          </div>
          <div class="form-group">
            <label>分组类型 *</label>
            <select v-model="createForm.group_type">
              <option value="video">视频分组</option>
              <option value="music">音乐分组</option>
            </select>
          </div>
          <div class="form-group">
            <label>分组描述</label>
            <textarea
              v-model="createForm.description"
              placeholder="请输入分组描述（可选）"
              rows="3"
            ></textarea>
          </div>
          <div v-if="formError" class="form-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>{{ formError }}</span>
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

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>修改分组</h3>
          <button class="close-btn" @click="closeEditModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>分组名称 *</label>
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
          <div v-if="formError" class="form-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>{{ formError }}</span>
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
          <p>确定要删除分组 "<strong>{{ groupToDelete?.name }}</strong>" 吗？</p>
          <p class="warning-text">该分组内的视频/音乐将变为未分组状态。</p>
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

const authStore = useAuthStore()

// State
const groups = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const filterType = ref('')

// Create modal state
const showCreateModal = ref(false)
const createForm = ref({ name: '', description: '', group_type: 'video' })
const isCreating = ref(false)
const formError = ref('')

// Edit modal state
const showEditModal = ref(false)
const groupToEdit = ref(null)
const editForm = ref({ name: '', description: '' })
const isEditing = ref(false)

// Delete modal state
const showDeleteModal = ref(false)
const groupToDelete = ref(null)
const isDeleting = ref(false)

// Toast state
const toastMessage = ref('')
const toastType = ref('success')

// Computed
const filteredGroups = computed(() => {
  let result = groups.value

  if (filterType.value) {
    result = result.filter(g => g.group_type === filterType.value)
  }

  if (!searchQuery.value.trim()) return result
  const query = searchQuery.value.toLowerCase()
  return result.filter(g => g.name.toLowerCase().includes(query))
})

// Lifecycle
onMounted(() => {
  loadGroups()
})

// Methods
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

// Create handlers
async function createGroup() {
  if (!createForm.value.name.trim()) return

  isCreating.value = true
  formError.value = ''

  try {
    const response = await authStore.apiRequest('/groups', {
      method: 'POST',
      body: JSON.stringify({
        name: createForm.value.name.trim(),
        description: createForm.value.description.trim() || null,
        group_type: createForm.value.group_type
      })
    })

    if (response.ok) {
      const newGroup = await response.json()
      groups.value.unshift(newGroup)
      closeCreateModal()
      showToast('创建成功', 'success')
    } else {
      const error = await response.json()
      formError.value = error.detail || '创建失败'
    }
  } catch (err) {
    formError.value = '网络错误'
  } finally {
    isCreating.value = false
  }
}

function closeCreateModal() {
  showCreateModal.value = false
  createForm.value = { name: '', description: '', group_type: 'video' }
  formError.value = ''
}

// Edit handlers
function editGroup(group) {
  groupToEdit.value = group
  editForm.value.name = group.name
  editForm.value.description = group.description || ''
  showEditModal.value = true
}

async function saveEdit() {
  if (!editForm.value.name.trim() || !groupToEdit.value) return

  isEditing.value = true
  formError.value = ''

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
      formError.value = error.detail || '修改失败'
    }
  } catch (err) {
    formError.value = '网络错误'
  } finally {
    isEditing.value = false
  }
}

function closeEditModal() {
  showEditModal.value = false
  groupToEdit.value = null
  editForm.value = { name: '', description: '' }
  formError.value = ''
}

// Delete handlers
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

.group-table-container {
  overflow-x: auto;
  border-radius: 12px;
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(99, 102, 241, 0.1);
}

.group-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;

  th {
    background: rgba(30, 41, 59, 0.6);
    padding: 16px 20px;
    text-align: left;
    font-weight: 600;
    color: #f8fafc;
    font-size: 0.9rem;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);
    white-space: nowrap;

    &:first-child {
      border-top-left-radius: 12px;
    }

    &:last-child {
      border-top-right-radius: 12px;
    }
  }

  td {
    padding: 16px 20px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.05);
    vertical-align: middle;
  }

  .group-row {
    transition: all 0.2s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.05);
    }

    &:last-child td {
      border-bottom: none;
    }
  }
}

.group-name-cell {
  .group-icon-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .group-name {
    font-weight: 600;
    color: #f8fafc;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.group-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &.video {
    background: rgba(99, 102, 241, 0.15);
    color: #6366f1;
  }

  &.music {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
  }

  svg {
    width: 20px;
    height: 20px;
  }
}

.group-type-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;

  &.video {
    background: rgba(99, 102, 241, 0.1);
    color: #a5b4fc;
  }

  &.music {
    background: rgba(16, 185, 129, 0.1);
    color: #34d399;
  }
}

.group-description-cell {
  max-width: 300px;
  color: #94a3b8;
  font-size: 0.9rem;

  span {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.group-date-cell {
  color: #64748b;
  font-size: 0.9rem;
  white-space: nowrap;
}

.group-actions-cell {
  .action-btn {
    width: 36px;
    height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 10px;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-right: 8px;

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
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #e2e8f0;
    }

    input,
    select,
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

      &:focus {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(15, 23, 42, 0.8);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
      }

      &::placeholder {
        color: #64748b;
      }
    }

    select {
      cursor: pointer;

      option {
        background: #1e293b;
        color: #f8fafc;
      }
    }

    textarea {
      resize: vertical;
      min-height: 80px;
    }
  }

  .form-error {
    display: flex;
    align-items: center;
    gap: 8px;
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
  .group-grid {
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
