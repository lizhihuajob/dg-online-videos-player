<template>
  <div class="profile-container">
    <header class="profile-header">
      <div class="header-content">
        <div class="back-button" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          <span>返回播放器</span>
        </div>
        <h1 class="header-title">个人中心</h1>
        <div class="header-spacer"></div>
      </div>
    </header>

    <div class="profile-content">
      <div class="profile-card glass">
        <div class="user-profile-header">
          <div class="profile-avatar-wrapper">
            <div class="profile-avatar" @click="triggerAvatarUpload" title="点击更换头像">
              <img v-if="currentUser?.avatar" :src="getAvatarUrl(currentUser.avatar)" alt="头像" class="avatar-image" />
              <span v-else class="avatar-text">{{ userInitial }}</span>
            </div>
            <div class="avatar-upload-overlay" @click="triggerAvatarUpload">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                <circle cx="12" cy="13" r="4"/>
              </svg>
            </div>
            <input type="file" ref="avatarInput" @change="handleAvatarUpload" accept="image/*" hidden />
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{{ currentUser?.username }}</h2>
            <p class="profile-email">{{ currentUser?.email }}</p>
            <span class="profile-badge">普通用户</span>
          </div>
        </div>
      </div>

      <div class="profile-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'info' }"
          @click="activeTab = 'info'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          个人信息
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'password' }"
          @click="activeTab = 'password'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
          修改密码
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'logs' }"
          @click="activeTab = 'logs'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          播放日志
        </button>
      </div>

      <div v-if="activeTab === 'info'" class="tab-content glass">
        <h3 class="section-title">编辑个人信息</h3>
        <div class="form-group">
          <label>用户名</label>
          <input 
            type="text" 
            v-model="profileForm.username" 
            placeholder="请输入用户名"
            :disabled="isUpdating"
          >
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input 
            type="email" 
            v-model="profileForm.email" 
            placeholder="请输入邮箱"
            :disabled="isUpdating"
          >
        </div>
        <div class="form-actions">
          <button 
            class="save-btn" 
            @click="updateProfile"
            :disabled="isUpdating || !hasProfileChanges"
          >
            <span v-if="isUpdating" class="btn-spinner"></span>
            <span v-else>保存修改</span>
          </button>
        </div>
      </div>

      <div v-if="activeTab === 'password'" class="tab-content glass">
        <h3 class="section-title">修改密码</h3>
        <div class="form-group">
          <label>当前密码</label>
          <input 
            type="password" 
            v-model="passwordForm.currentPassword" 
            placeholder="请输入当前密码"
            :disabled="isUpdating"
          >
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input 
            type="password" 
            v-model="passwordForm.newPassword" 
            placeholder="请输入新密码（至少6位）"
            :disabled="isUpdating"
          >
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input 
            type="password" 
            v-model="passwordForm.confirmPassword" 
            placeholder="请再次输入新密码"
            :disabled="isUpdating"
          >
        </div>
        <div class="form-actions">
          <button 
            class="save-btn" 
            @click="updatePassword"
            :disabled="isUpdating || !isPasswordFormValid"
          >
            <span v-if="isUpdating" class="btn-spinner"></span>
            <span v-else>修改密码</span>
          </button>
        </div>
      </div>

      <div v-if="activeTab === 'logs'" class="tab-content glass">
        <div class="logs-header">
          <h3 class="section-title">播放日志</h3>
          <div class="search-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21l-4.35-4.35"/>
            </svg>
            <input 
              type="text" 
              v-model="searchKeyword" 
              placeholder="搜索视频名称..."
              @input="handleSearch"
            >
          </div>
        </div>
        <div v-if="filteredLogs.length === 0" class="empty-logs">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <p>{{ searchKeyword ? '未找到匹配的记录' : '暂无播放记录' }}</p>
        </div>
        <div v-else class="logs-table-container">
          <table class="logs-table">
            <thead>
              <tr>
                <th class="col-index">序号</th>
                <th class="col-name">视频名称</th>
                <th class="col-format">格式</th>
                <th class="col-time">播放时间</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(log, index) in paginatedLogs" :key="log.id">
                <td class="col-index">{{ (currentPage - 1) * pageSize + index + 1 }}</td>
                <td class="col-name" :title="log.video_name">{{ log.video_name }}</td>
                <td class="col-format">
                  <span class="format-tag">{{ log.video_format?.toUpperCase() || '-' }}</span>
                </td>
                <td class="col-time">{{ formatDateTime(log.play_time) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="pagination" v-if="totalPages > 1">
            <button 
              class="page-btn" 
              :disabled="currentPage === 1"
              @click="currentPage = 1"
            >
              首页
            </button>
            <button 
              class="page-btn" 
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              上一页
            </button>
            <div class="page-info">
              <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
              <span class="total-count">共 {{ filteredLogs.length }} 条</span>
            </div>
            <button 
              class="page-btn" 
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              下一页
            </button>
            <button 
              class="page-btn" 
              :disabled="currentPage === totalPages"
              @click="currentPage = totalPages"
            >
              末页
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showSuccess" class="modal-overlay" @click="showSuccess = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <h3>{{ successTitle }}</h3>
        </div>
        <p>{{ successMessage }}</p>
        <button class="modal-btn" @click="showSuccess = false">确定</button>
      </div>
    </div>

    <div v-if="showError" class="modal-overlay" @click="showError = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3>操作失败</h3>
        </div>
        <p>{{ errorMessage }}</p>
        <button class="modal-btn" @click="showError = false">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE = 'http://localhost:8000'

const currentUser = ref(null)
const accessToken = ref(null)
const activeTab = ref('info')
const isUpdating = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const successTitle = ref('操作成功')
const successMessage = ref('')
const errorMessage = ref('')
const avatarInput = ref(null)
const playLogs = ref([])
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

const profileForm = ref({
  username: '',
  email: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const userInitial = computed(() => {
  return currentUser.value?.username?.charAt(0).toUpperCase() || '?'
})

const hasProfileChanges = computed(() => {
  return profileForm.value.username !== currentUser.value?.username ||
         profileForm.value.email !== currentUser.value?.email
})

const isPasswordFormValid = computed(() => {
  return passwordForm.value.currentPassword &&
         passwordForm.value.newPassword &&
         passwordForm.value.newPassword.length >= 6 &&
         passwordForm.value.newPassword === passwordForm.value.confirmPassword
})

const filteredLogs = computed(() => {
  if (!searchKeyword.value.trim()) {
    return playLogs.value
  }
  const keyword = searchKeyword.value.toLowerCase().trim()
  return playLogs.value.filter(log => 
    log.video_name?.toLowerCase().includes(keyword)
  )
})

const totalPages = computed(() => {
  return Math.ceil(filteredLogs.value.length / pageSize.value) || 1
})

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredLogs.value.slice(start, end)
})

const handleSearch = () => {
  currentPage.value = 1
}

onMounted(() => {
  const token = localStorage.getItem('access_token')
  const user = localStorage.getItem('current_user')
  if (token && user) {
    accessToken.value = token
    currentUser.value = JSON.parse(user)
    profileForm.value.username = currentUser.value.username
    profileForm.value.email = currentUser.value.email
    loadPlayLogs()
  } else {
    router.push('/')
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

const getAvatarUrl = (avatar) => {
  if (!avatar) return null
  if (avatar.startsWith('http')) return avatar
  return `${API_BASE}${avatar}`
}

const goBack = () => {
  router.push('/')
}

const triggerAvatarUpload = () => {
  avatarInput.value?.click()
}

const handleAvatarUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    errorMessage.value = '请选择图片文件'
    showError.value = true
    return
  }

  isUpdating.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await apiRequest('/users/me/avatar', {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      currentUser.value = { ...currentUser.value, avatar: data.avatar }
      localStorage.setItem('current_user', JSON.stringify(currentUser.value))
      successTitle.value = '头像更新成功'
      successMessage.value = '头像已成功更新'
      showSuccess.value = true
    } else {
      const error = await response.json()
      errorMessage.value = error.detail || '头像上传失败'
      showError.value = true
    }
  } catch (err) {
    errorMessage.value = '网络错误，请稍后重试'
    showError.value = true
  } finally {
    isUpdating.value = false
    e.target.value = ''
  }
}

const loadPlayLogs = async () => {
  try {
    const response = await apiRequest('/play-logs')
    if (response.ok) {
      playLogs.value = await response.json()
    }
  } catch (err) {
    console.error('Failed to load play logs:', err)
  }
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateProfile = async () => {
  if (!profileForm.value.username || !profileForm.value.email) {
    errorMessage.value = '用户名和邮箱不能为空'
    showError.value = true
    return
  }

  isUpdating.value = true
  try {
    const response = await apiRequest('/users/me', {
      method: 'PUT',
      body: JSON.stringify({
        username: profileForm.value.username,
        email: profileForm.value.email
      })
    })

    if (response.ok) {
      const updatedUser = await response.json()
      currentUser.value = { ...currentUser.value, ...updatedUser }
      localStorage.setItem('current_user', JSON.stringify(currentUser.value))
      successTitle.value = '更新成功'
      successMessage.value = '个人信息更新成功'
      showSuccess.value = true
    } else {
      const error = await response.json()
      errorMessage.value = error.detail || '更新失败'
      showError.value = true
    }
  } catch (err) {
    errorMessage.value = '网络错误，请稍后重试'
    showError.value = true
  } finally {
    isUpdating.value = false
  }
}

const updatePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    errorMessage.value = '两次输入的新密码不一致'
    showError.value = true
    return
  }

  if (passwordForm.value.newPassword.length < 6) {
    errorMessage.value = '新密码长度至少为6位'
    showError.value = true
    return
  }

  isUpdating.value = true
  try {
    const response = await apiRequest('/users/me/password', {
      method: 'PUT',
      body: JSON.stringify({
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword
      })
    })

    if (response.ok) {
      successTitle.value = '密码修改成功'
      successMessage.value = '密码修改成功，请使用新密码重新登录'
      showSuccess.value = true
      passwordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } else {
      const error = await response.json()
      errorMessage.value = error.detail || '密码修改失败'
      showError.value = true
    }
  } catch (err) {
    errorMessage.value = '网络错误，请稍后重试'
    showError.value = true
  } finally {
    isUpdating.value = false
  }
}
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  background: radial-gradient(ellipse at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%);
  color: #f8fafc;
}

.profile-header {
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;

  .header-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .back-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #a5b4fc;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.4);
      color: #f8fafc;
      transform: translateX(-2px);
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }

  .header-title {
    font-size: 1.25rem;
    font-weight: 600;
    background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .header-spacer {
    width: 100px;
  }
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 24px;
}

.profile-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);

  .user-profile-header {
    display: flex;
    align-items: center;
    gap: 24px;

    .profile-avatar-wrapper {
      position: relative;
      cursor: pointer;

      .profile-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        overflow: hidden;
        transition: all 0.3s ease;

        .avatar-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .avatar-text {
          color: white;
          font-size: 2rem;
          font-weight: 700;
        }
      }

      .avatar-upload-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;

        svg {
          width: 24px;
          height: 24px;
          color: white;
        }
      }

      &:hover {
        .avatar-upload-overlay {
          opacity: 1;
        }
      }
    }

    .profile-info {
      .profile-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 4px;
      }

      .profile-email {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 8px;
      }

      .profile-badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        font-size: 0.75rem;
        color: #a5b4fc;
        font-weight: 500;
      }
    }
  }
}

.profile-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;

  .tab-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 24px;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
      color: #c7d2fe;
    }

    &.active {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
      border-color: rgba(99, 102, 241, 0.4);
      color: #f8fafc;
    }
  }
}

.tab-content {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(10px);

  .section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  }

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

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }
  }

  .form-actions {
    margin-top: 32px;

    .save-btn {
      width: 100%;
      padding: 14px 24px;
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      border: none;
      border-radius: 12px;
      color: white;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
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
        width: 20px;
        height: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
      }
    }
  }
}

.empty-logs {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  color: #64748b;

  svg {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
  }

  p {
    font-size: 0.95rem;
  }
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 16px;
  flex-wrap: wrap;

  .section-title {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }

  .search-box {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    transition: all 0.25s ease;

    &:focus-within {
      border-color: rgba(99, 102, 241, 0.5);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    svg {
      width: 18px;
      height: 18px;
      color: #64748b;
      flex-shrink: 0;
    }

    input {
      background: transparent;
      border: none;
      outline: none;
      color: #f8fafc;
      font-size: 0.9rem;
      width: 180px;

      &::placeholder {
        color: #475569;
      }
    }
  }
}

.logs-table-container {
  overflow: hidden;

  .logs-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;

    thead {
      tr {
        background: rgba(99, 102, 241, 0.1);
      }

      th {
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        color: #a5b4fc;
        border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        white-space: nowrap;
      }
    }

    tbody {
      tr {
        transition: background 0.2s ease;

        &:hover {
          background: rgba(99, 102, 241, 0.05);
        }
      }

      td {
        padding: 14px 16px;
        color: #e2e8f0;
        border-bottom: 1px solid rgba(99, 102, 241, 0.08);
      }
    }

    .col-index {
      width: 60px;
      text-align: center;
      color: #64748b;
    }

    .col-name {
      max-width: 300px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .col-format {
      width: 80px;
      text-align: center;

      .format-tag {
        display: inline-block;
        padding: 3px 8px;
        background: rgba(99, 102, 241, 0.15);
        border-radius: 4px;
        color: #a5b4fc;
        font-weight: 500;
        font-size: 0.8rem;
      }
    }

    .col-time {
      width: 160px;
      color: #94a3b8;
      font-size: 0.85rem;
    }
  }
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);

  .page-btn {
    padding: 8px 14px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #a5b4fc;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover:not(:disabled) {
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.4);
      color: #f8fafc;
    }

    &:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
  }

  .page-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 16px;
    font-size: 0.85rem;
    color: #94a3b8;

    .total-count {
      font-size: 0.75rem;
      color: #64748b;
      margin-top: 2px;
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
  max-width: 380px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  padding: 28px;
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;

  .modal-header {
    margin-bottom: 20px;

    .error-icon {
      width: 48px;
      height: 48px;
      color: #ef4444;
      margin: 0 auto 15px;
      filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.3));
    }

    h3 {
      font-size: 1.25rem;
      margin: 0;
      font-weight: 600;
      color: #f8fafc;
    }
  }

  p {
    color: #94a3b8;
    margin-bottom: 24px;
    line-height: 1.6;
    font-size: 0.95rem;
  }

  .modal-btn {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

    &:hover {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-1px);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
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

@media (max-width: 640px) {
  .profile-header {
    .header-content {
      padding: 12px 16px;
    }

    .header-title {
      font-size: 1.1rem;
    }

    .back-button span {
      display: none;
    }

    .header-spacer {
      width: 50px;
    }
  }

  .profile-content {
    padding: 20px 16px;
  }

  .profile-card {
    padding: 24px;

    .user-profile-header {
      flex-direction: column;
      text-align: center;
      gap: 16px;

      .profile-avatar-wrapper {
        .profile-avatar,
        .avatar-upload-overlay {
          width: 64px;
          height: 64px;
        }

        .profile-avatar .avatar-text {
          font-size: 1.5rem;
        }
      }
    }
  }

  .profile-tabs {
    flex-direction: column;
    gap: 8px;

    .tab-btn {
      padding: 12px 16px;
    }
  }

  .tab-content {
    padding: 24px 20px;
  }
}
</style>
