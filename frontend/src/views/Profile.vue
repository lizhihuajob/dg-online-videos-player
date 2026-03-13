<template>
  <div class="profile-container">
    <div class="back-button" @click="goBack">
      <svg class="back-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M19 12H5M12 19l-7-7 7-7"/>
      </svg>
      <span>返回播放器</span>
    </div>

    <div class="profile-content">
      <div class="profile-header glass">
        <div class="avatar-section">
          <div class="avatar-wrapper">
            <div class="avatar">
              <span class="avatar-text">{{ avatarText }}</span>
            </div>
            <div class="avatar-badge">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
          </div>
          <div class="user-info">
            <h1 class="username">{{ userInfo.username }}</h1>
            <p class="user-email">{{ userInfo.email }}</p>
            <span class="member-since">注册时间: {{ formatDate(userInfo.created_at) }}</span>
          </div>
        </div>
      </div>

      <div class="profile-tabs glass">
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
      </div>

      <div class="profile-body glass">
        <div v-if="activeTab === 'info'" class="info-section">
          <h2 class="section-title">修改个人信息</h2>
          <form @submit.prevent="updateUserInfo" class="info-form">
            <div class="form-group">
              <label>用户名</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <input 
                  type="text" 
                  v-model="editForm.username" 
                  placeholder="请输入用户名"
                  required
                >
              </div>
            </div>
            <div class="form-group">
              <label>邮箱</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                <input 
                  type="email" 
                  v-model="editForm.email" 
                  placeholder="请输入邮箱"
                  required
                >
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn secondary" @click="resetInfoForm">重置</button>
              <button type="submit" class="btn primary" :disabled="isUpdating">
                {{ isUpdating ? '保存中...' : '保存修改' }}
              </button>
            </div>
          </form>
        </div>

        <div v-else class="password-section">
          <h2 class="section-title">修改密码</h2>
          <form @submit.prevent="updatePassword" class="password-form">
            <div class="form-group">
              <label>当前密码</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input 
                  :type="showOldPassword ? 'text' : 'password'" 
                  v-model="passwordForm.oldPassword" 
                  placeholder="请输入当前密码"
                  required
                >
                <button type="button" class="toggle-password" @click="showOldPassword = !showOldPassword">
                  <svg v-if="showOldPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label>新密码</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input 
                  :type="showNewPassword ? 'text' : 'password'" 
                  v-model="passwordForm.newPassword" 
                  placeholder="请输入新密码 (至少6位)"
                  required
                  minlength="6"
                >
                <button type="button" class="toggle-password" @click="showNewPassword = !showNewPassword">
                  <svg v-if="showNewPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label>确认新密码</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  v-model="passwordForm.confirmPassword" 
                  placeholder="请再次输入新密码"
                  required
                >
                <button type="button" class="toggle-password" @click="showConfirmPassword = !showConfirmPassword">
                  <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn secondary" @click="resetPasswordForm">重置</button>
              <button type="submit" class="btn primary" :disabled="isUpdatingPassword">
                {{ isUpdatingPassword ? '修改中...' : '修改密码' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg v-if="modalType === 'success'" class="modal-icon success" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M9 12l2 2 4-4"/>
          </svg>
          <svg v-else class="modal-icon error" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3>{{ modalTitle }}</h3>
        </div>
        <p class="modal-message">{{ modalMessage }}</p>
        <button class="modal-btn" @click="closeModal">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import API_BASE from '@/config/api'

const router = useRouter()

const activeTab = ref('info')
const userInfo = ref({
  username: '',
  email: '',
  created_at: ''
})
const editForm = ref({
  username: '',
  email: ''
})
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const isUpdating = ref(false)
const isUpdatingPassword = ref(false)

const showModal = ref(false)
const modalType = ref('success')
const modalTitle = ref('')
const modalMessage = ref('')

const avatarText = computed(() => {
  return userInfo.value.username ? userInfo.value.username.charAt(0).toUpperCase() : 'U'
})

const accessToken = computed(() => localStorage.getItem('access_token'))

onMounted(() => {
  loadUserInfo()
})

const loadUserInfo = async () => {
  try {
    const response = await fetch(`${API_BASE}/users/me`, {
      headers: {
        'Authorization': `Bearer ${accessToken.value}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      userInfo.value = data
      editForm.value.username = data.username
      editForm.value.email = data.email
    } else {
      openModal('error', '获取用户信息失败', '请重新登录')
      router.push('/')
    }
  } catch (err) {
    console.error('Failed to load user info:', err)
    openModal('error', '网络错误', '请检查网络连接')
  }
}

const updateUserInfo = async () => {
  if (!editForm.value.username.trim()) {
    openModal('error', '错误', '用户名不能为空')
    return
  }
  if (!editForm.value.email.trim()) {
    openModal('error', '错误', '邮箱不能为空')
    return
  }

  isUpdating.value = true
  try {
    const response = await fetch(`${API_BASE}/users/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken.value}`
      },
      body: JSON.stringify({
        username: editForm.value.username,
        email: editForm.value.email
      })
    })
    if (response.ok) {
      const data = await response.json()
      userInfo.value = data
      localStorage.setItem('current_user', JSON.stringify(data))
      openModal('success', '成功', '个人信息修改成功')
    } else {
      const error = await response.json()
      openModal('error', '修改失败', error.detail || '请稍后重试')
    }
  } catch (err) {
    console.error('Failed to update user info:', err)
    openModal('error', '网络错误', '请检查网络连接')
  } finally {
    isUpdating.value = false
  }
}

const updatePassword = async () => {
  if (passwordForm.value.newPassword.length < 6) {
    openModal('error', '错误', '新密码至少需要6位')
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    openModal('error', '错误', '两次输入的新密码不一致')
    return
  }

  isUpdatingPassword.value = true
  try {
    const response = await fetch(`${API_BASE}/users/me/password`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken.value}`
      },
      body: JSON.stringify({
        old_password: passwordForm.value.oldPassword,
        new_password: passwordForm.value.newPassword
      })
    })
    if (response.ok) {
      openModal('success', '成功', '密码修改成功，请重新登录')
      resetPasswordForm()
    } else {
      const error = await response.json()
      openModal('error', '修改失败', error.detail || '当前密码错误')
    }
  } catch (err) {
    console.error('Failed to update password:', err)
    openModal('error', '网络错误', '请检查网络连接')
  } finally {
    isUpdatingPassword.value = false
  }
}

const resetInfoForm = () => {
  editForm.value.username = userInfo.value.username
  editForm.value.email = userInfo.value.email
}

const resetPasswordForm = () => {
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  showOldPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
}

const openModal = (type, title, message) => {
  modalType.value = type
  modalTitle.value = title
  modalMessage.value = message
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const goBack = () => {
  router.push('/')
}

const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style lang="scss" scoped>
.profile-container {
  min-height: 100vh;
  padding: 24px;
  background: radial-gradient(ellipse at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%);
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 50px;
  color: #c7d2fe;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 24px;
  user-select: none;
  backdrop-filter: blur(10px);

  &:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.4);
    color: #f8fafc;
    transform: translateX(-3px);
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.3);
  }

  .back-icon {
    width: 18px;
    height: 18px;
  }
}

.profile-content {
  max-width: 600px;
  margin: 0 auto;
}

.profile-header {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 20px;
  backdrop-filter: blur(12px);
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-wrapper {
  position: relative;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4);
  border: 3px solid rgba(255, 255, 255, 0.1);
}

.avatar-text {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.avatar-badge {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #0f172a;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);

  svg {
    width: 14px;
    height: 14px;
    color: white;
  }
}

.user-info {
  flex: 1;

  .username {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 8px 0;
  }

  .user-email {
    font-size: 0.95rem;
    color: #94a3b8;
    margin: 0 0 8px 0;
  }

  .member-since {
    font-size: 0.85rem;
    color: #64748b;
    background: rgba(99, 102, 241, 0.1);
    padding: 4px 12px;
    border-radius: 20px;
    display: inline-block;
  }
}

.profile-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 8px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  backdrop-filter: blur(12px);

  .tab-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 20px;
    background: transparent;
    border: none;
    border-radius: 12px;
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;

    svg {
      width: 20px;
      height: 20px;
    }

    &:hover {
      color: #c7d2fe;
      background: rgba(99, 102, 241, 0.1);
    }

    &.active {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.2) 100%);
      color: #f8fafc;
      box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.3);
    }
  }
}

.profile-body {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(12px);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f8fafc;
  margin: 0 0 24px 0;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.15);
}

.form-group {
  margin-bottom: 20px;

  label {
    display: block;
    margin-bottom: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    color: #94a3b8;
  }
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;

  .input-icon {
    position: absolute;
    left: 14px;
    width: 20px;
    height: 20px;
    color: #6366f1;
    opacity: 0.7;
  }

  input {
    width: 100%;
    padding: 14px 14px 14px 44px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
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
  }

  .toggle-password {
    position: absolute;
    right: 14px;
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
    transition: all 0.2s;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      color: #94a3b8;
      background: rgba(99, 102, 241, 0.1);
    }
  }
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.btn {
  flex: 1;
  padding: 14px 24px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  border: none;

  &.secondary {
    background: rgba(51, 65, 85, 0.6);
    color: #94a3b8;

    &:hover {
      background: rgba(71, 85, 105, 0.8);
      color: #f8fafc;
    }
  }

  &.primary {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}

.glass {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  width: 90%;
  max-width: 380px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);

  .modal-header {
    margin-bottom: 16px;

    .modal-icon {
      width: 48px;
      height: 48px;
      margin: 0 auto 12px;

      &.success {
        color: #10b981;
        filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.3));
      }

      &.error {
        color: #ef4444;
        filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.3));
      }
    }

    h3 {
      font-size: 1.25rem;
      margin: 0;
      color: #f8fafc;
    }
  }

  .modal-message {
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
    }
  }
}

@media (max-width: 640px) {
  .profile-container {
    padding: 16px;
  }

  .avatar-section {
    flex-direction: column;
    text-align: center;
  }

  .avatar {
    width: 80px;
    height: 80px;
  }

  .avatar-text {
    font-size: 2rem;
  }

  .user-info .username {
    font-size: 1.5rem;
  }

  .profile-tabs {
    flex-direction: column;
  }

  .profile-body {
    padding: 24px;
  }
}
</style>
