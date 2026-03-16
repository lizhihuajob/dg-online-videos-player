<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>个人中心</h1>
    </div>
    
    <div class="profile-content">
      <!-- User Card -->
      <div class="profile-card glass">
        <div class="avatar-section">
          <div class="avatar-wrapper" @click="triggerAvatarUpload">
            <div class="avatar">
              <img v-if="currentUser?.avatar" :src="getAvatarUrl(currentUser.avatar)" alt="avatar">
              <span v-else>{{ currentUser?.username?.charAt(0).toUpperCase() || 'A' }}</span>
            </div>
            <div class="avatar-overlay">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                <circle cx="12" cy="13" r="4"/>
              </svg>
              <span>更换头像</span>
            </div>
          </div>
          <input type="file" ref="avatarInput" @change="handleAvatarUpload" accept="image/*" hidden>
          <div class="user-info">
            <h2 class="username">{{ currentUser?.username }}</h2>
            <p class="email">{{ currentUser?.email }}</p>
            <span class="badge">管理员</span>
          </div>
        </div>
      </div>
      
      <!-- Tabs -->
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
          基本信息
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
      </div>
      
      <!-- Info Tab -->
      <div v-if="activeTab === 'info'" class="tab-content glass">
        <h3 class="section-title">基本信息</h3>
        <div class="form-group">
          <label>用户名</label>
          <input 
            type="text" 
            :value="currentUser?.username" 
            disabled
            class="disabled-input"
          >
          <span class="input-hint">用户名不可修改</span>
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
      
      <!-- Password Tab -->
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
    </div>
    
    <!-- Success Modal -->
    <div v-if="showSuccess" class="modal-overlay" @click="showSuccess = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="success-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M9 12l2 2 4-4"/>
          </svg>
          <h3>操作成功</h3>
        </div>
        <p>{{ successMessage }}</p>
        <button class="modal-btn" @click="showSuccess = false">确定</button>
      </div>
    </div>
    
    <!-- Error Modal -->
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
const successMessage = ref('')
const errorMessage = ref('')
const avatarInput = ref(null)

const profileForm = ref({
  email: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const hasProfileChanges = computed(() => {
  return profileForm.value.email !== currentUser.value?.email
})

const isPasswordFormValid = computed(() => {
  return passwordForm.value.currentPassword &&
         passwordForm.value.newPassword &&
         passwordForm.value.newPassword.length >= 6 &&
         passwordForm.value.newPassword === passwordForm.value.confirmPassword
})

onMounted(() => {
  const token = localStorage.getItem('access_token')
  const user = localStorage.getItem('current_user')
  if (token && user) {
    accessToken.value = token
    currentUser.value = JSON.parse(user)
    profileForm.value.email = currentUser.value.email
  } else {
    router.push('/login')
  }
})

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `${API_BASE}${avatar}`
}

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
      headers: {},
      body: formData
    })
    
    if (response.ok) {
      const data = await response.json()
      currentUser.value = { ...currentUser.value, avatar: data.avatar }
      localStorage.setItem('current_user', JSON.stringify(currentUser.value))
      successMessage.value = '头像更新成功'
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

const updateProfile = async () => {
  if (!profileForm.value.email) {
    errorMessage.value = '邮箱不能为空'
    showError.value = true
    return
  }

  isUpdating.value = true
  try {
    const response = await apiRequest('/users/me', {
      method: 'PUT',
      body: JSON.stringify({
        email: profileForm.value.email
      })
    })

    if (response.ok) {
      const updatedUser = await response.json()
      currentUser.value = updatedUser
      localStorage.setItem('current_user', JSON.stringify(updatedUser))
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
      successMessage.value = '密码修改成功'
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
.profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
  
  h1 {
    font-size: 1.75rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.profile-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  
  .avatar-section {
    display: flex;
    align-items: center;
    gap: 24px;
    
    .avatar-wrapper {
      position: relative;
      cursor: pointer;
      
      .avatar {
        width: 100px;
        height: 100px;
        border-radius: 20px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
        
        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        
        span {
          color: white;
          font-size: 2.5rem;
          font-weight: 700;
        }
      }
      
      .avatar-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        
        svg {
          width: 28px;
          height: 28px;
          color: white;
          margin-bottom: 4px;
        }
        
        span {
          color: white;
          font-size: 0.75rem;
          font-weight: 500;
        }
      }
      
      &:hover {
        .avatar-overlay {
          opacity: 1;
        }
      }
    }
    
    .user-info {
      .username {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 4px;
      }
      
      .email {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 8px;
      }
      
      .badge {
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
      
      &.disabled-input {
        background: rgba(15, 23, 42, 0.4);
        color: #64748b;
      }
    }
    
    .input-hint {
      display: block;
      margin-top: 6px;
      font-size: 0.8rem;
      color: #64748b;
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
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  
  .modal-header {
    margin-bottom: 20px;
    
    .success-icon {
      width: 48px;
      height: 48px;
      color: #10b981;
      margin: 0 auto 15px;
      filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.3));
    }
    
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
  .profile-card {
    padding: 24px;
    
    .avatar-section {
      flex-direction: column;
      text-align: center;
      
      .avatar-wrapper {
        .avatar {
          width: 80px;
          height: 80px;
          
          span {
            font-size: 2rem;
          }
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
