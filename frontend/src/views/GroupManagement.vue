<template>
  <div class="group-management">
    <div class="page-actions">
      <button class="btn btn-primary" @click="showCreateDialog = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        创建分组
      </button>
    </div>

    <div v-if="groups.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
        <circle cx="9" cy="7" r="4"></circle>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
      </svg>
      <h3>暂无分组</h3>
      <p>点击上方按钮创建您的第一个分组</p>
    </div>

    <div v-else class="groups-grid">
      <div v-for="group in groups" :key="group.id" class="group-card">
        <div class="group-card-header">
          <h3>{{ group.name }}</h3>
          <div class="group-actions">
            <button class="btn-icon" @click="editGroup(group)" title="编辑">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button class="btn-icon delete" @click="deleteGroup(group)" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
        <p class="group-description">{{ group.description || '暂无描述' }}</p>
        <div class="group-meta">
          <span class="group-type" :class="group.type">{{ group.type === 'video' ? '视频' : '音乐' }}</span>
          <span class="group-date">{{ formatDate(group.created_at) }}</span>
        </div>
      </div>
    </div>

    <div v-if="showCreateDialog || showEditDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <h3>{{ showCreateDialog ? '创建分组' : '编辑分组' }}</h3>
        <form @submit.prevent="showCreateDialog ? createGroup() : updateGroup()">
          <div class="form-group">
            <label>分组名称</label>
            <input type="text" v-model="formData.name" placeholder="请输入分组名称" required>
          </div>
          <div class="form-group">
            <label>分组描述</label>
            <textarea v-model="formData.description" placeholder="请输入分组描述（可选）"></textarea>
          </div>
          <div class="form-group">
            <label>分组类型</label>
            <select v-model="formData.type">
              <option value="video">视频</option>
              <option value="music">音乐</option>
            </select>
          </div>
          <div class="dialog-actions">
            <button type="button" class="btn btn-secondary" @click="closeDialog">取消</button>
            <button type="submit" class="btn btn-primary">{{ showCreateDialog ? '创建' : '保存' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const groups = ref([])
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const editingGroup = ref(null)
const formData = ref({
  name: '',
  description: '',
  type: 'video'
})

async function fetchGroups() {
  try {
    const response = await fetch('/api/groups', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (response.ok) {
      groups.value = await response.json()
    }
  } catch (error) {
    console.error('获取分组失败:', error)
  }
}

function resetForm() {
  formData.value = {
    name: '',
    description: '',
    type: 'video'
  }
}

function closeDialog() {
  showCreateDialog.value = false
  showEditDialog.value = false
  editingGroup.value = null
  resetForm()
}

function editGroup(group) {
  editingGroup.value = group
  formData.value = {
    name: group.name,
    description: group.description || '',
    type: group.type
  }
  showEditDialog.value = true
}

async function createGroup() {
  try {
    const response = await fetch('/api/groups', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(formData.value)
    })
    if (response.ok) {
      fetchGroups()
      closeDialog()
    }
  } catch (error) {
    console.error('创建分组失败:', error)
  }
}

async function updateGroup() {
  try {
    const response = await fetch(`/api/groups/${editingGroup.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(formData.value)
    })
    if (response.ok) {
      fetchGroups()
      closeDialog()
    }
  } catch (error) {
    console.error('更新分组失败:', error)
  }
}

async function deleteGroup(group) {
  if (!confirm(`确定要删除分组 "${group.name}" 吗？`)) return
  try {
    const response = await fetch(`/api/groups/${group.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (response.ok) {
      fetchGroups()
    }
  } catch (error) {
    console.error('删除分组失败:', error)
  }
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString()
}

onMounted(() => {
  fetchGroups()
})
</script>

<style lang="scss" scoped>
.group-management {
  .page-actions {
    margin-bottom: 24px;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s;

    &.btn-primary {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: white;

      &:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
      }
    }

    &.btn-secondary {
      background: rgba(148, 163, 184, 0.1);
      color: #f8fafc;

      &:hover {
        background: rgba(148, 163, 184, 0.2);
      }
    }
  }

  .btn-icon {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 6px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #6366f1;
    }

    &.delete:hover {
      background: rgba(239, 68, 68, 0.1);
      color: #ef4444;
    }
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: #94a3b8;
    text-align: center;

    svg {
      width: 64px;
      height: 64px;
      margin-bottom: 16px;
      opacity: 0.3;
    }

    h3 {
      margin: 0 0 8px 0;
      color: #f8fafc;
    }

    p {
      margin: 0;
    }
  }

  .groups-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }

  .group-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.1);
    border-radius: 12px;
    padding: 20px;
    transition: all 0.2s;

    &:hover {
      border-color: rgba(99, 102, 241, 0.3);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
  }

  .group-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;

    h3 {
      margin: 0;
      color: #f8fafc;
    }

    .group-actions {
      display: flex;
      gap: 4px;
    }
  }

  .group-description {
    color: #94a3b8;
    margin: 0 0 16px 0;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  .group-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;

    .group-type {
      padding: 4px 10px;
      border-radius: 20px;
      font-weight: 500;

      &.video {
        background: rgba(99, 102, 241, 0.1);
        color: #6366f1;
      }

      &.music {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
      }
    }

    .group-date {
      color: #64748b;
    }
  }

  .dialog-overlay {
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

  .dialog {
    background: #1e293b;
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    padding: 24px;
    width: 100%;
    max-width: 450px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);

    h3 {
      margin: 0 0 20px 0;
      color: #f8fafc;
    }
  }

  .form-group {
    margin-bottom: 16px;

    label {
      display: block;
      margin-bottom: 8px;
      color: #f8fafc;
      font-weight: 500;
    }

    input, textarea, select {
      width: 100%;
      padding: 10px 12px;
      background: #0f172a;
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 8px;
      color: #f8fafc;
      font-size: 0.95rem;

      &:focus {
        outline: none;
        border-color: #6366f1;
      }
    }

    textarea {
      resize: vertical;
      min-height: 80px;
    }
  }

  .dialog-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 24px;
  }
}
</style>