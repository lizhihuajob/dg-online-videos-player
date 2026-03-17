<template>
  <div class="profile-page">
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

    <!-- Page Header -->
    <div class="page-header">
      <h1 class="page-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        个人中心
      </h1>
      <p class="page-subtitle">管理您的个人信息和账户安全</p>
    </div>

    <!-- Main Content - Two Column Layout -->
    <div class="profile-content">
      <!-- Left Column - User Info -->
      <div class="left-column">
        <!-- Avatar Card -->
        <div class="profile-card avatar-card">
          <div class="card-header">
            <h3>头像设置</h3>
          </div>
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <img v-if="authStore.avatarUrl" :src="authStore.avatarUrl" alt="Avatar" class="avatar-img">
              <div v-else class="avatar-placeholder">
                <span>{{ authStore.userInitial }}</span>
              </div>
              <div class="avatar-overlay" @click="triggerFileInput">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                  <circle cx="12" cy="13" r="4"/>
                </svg>
                <span>更换头像</span>
              </div>
            </div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleAvatarChange"
              hidden
            >
            <p class="avatar-hint">点击头像上传新图片</p>
          </div>
        </div>

        <!-- User Info Card -->
        <div class="profile-card info-card">
          <div class="card-header">
            <h3>基本信息</h3>
          </div>
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">用户名</span>
              <span class="info-value">{{ authStore.currentUser?.username }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">用户ID</span>
              <span class="info-value">{{ authStore.currentUser?.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">注册时间</span>
              <span class="info-value">{{ formatDate(authStore.currentUser?.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column - Settings -->
      <div class="right-column">
        <!-- Password Change Card -->
        <div class="profile-card password-card">
          <div class="card-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <h3>修改密码</h3>
          </div>
          <form @submit.prevent="changePassword" class="password-form">
            <div class="form-group">
              <label>当前密码</label>
              <div class="input-wrapper">
                <input
                  v-model="passwordForm.currentPassword"
                  :type="showCurrentPassword ? 'text' : 'password'"
                  placeholder="请输入当前密码"
                  required
                >
                <button type="button" class="toggle-btn" @click="showCurrentPassword = !showCurrentPassword">
                  <svg v-if="showCurrentPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label>新密码</label>
              <div class="input-wrapper">
                <input
                  v-model="passwordForm.newPassword"
                  :type="showNewPassword ? 'text' : 'password'"
                  placeholder="请输入新密码"
                  required
                  minlength="6"
                >
                <button type="button" class="toggle-btn" @click="showNewPassword = !showNewPassword">
                  <svg v-if="showNewPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label>确认新密码</label>
              <div class="input-wrapper">
                <input
                  v-model="passwordForm.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="请再次输入新密码"
                  required
                  minlength="6"
                >
                <button type="button" class="toggle-btn" @click="showConfirmPassword = !showConfirmPassword">
                  <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>
            <button type="submit" class="submit-btn" :disabled="isChangingPassword">
              <span v-if="isChangingPassword" class="btn-spinner"></span>
              <span v-else>修改密码</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const fileInput = ref(null)

// Toast
const toastMessage = ref('')
const toastType = ref('success')

// Password form
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const isChangingPassword = ref(false)

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

function triggerFileInput() {
  fileInput.value.click()
}

async function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    showToast('图片大小不能超过5MB', 'error')
    return
  }

  const result = await authStore.updateAvatar(file)
  if (result.success) {
    showToast('头像更新成功')
  } else {
    showToast(result.error || '头像更新失败', 'error')
  }
}

async function changePassword() {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    showToast('两次输入的新密码不一致', 'error')
    return
  }

  if (passwordForm.newPassword.length < 6) {
    showToast('新密码长度至少为6位', 'error')
    return
  }

  isChangingPassword.value = true
  const result = await authStore.updatePassword(
    passwordForm.currentPassword,
    passwordForm.newPassword
  )

  if (result.success) {
    showToast('密码修改成功')
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } else {
    showToast(result.error || '密码修改失败', 'error')
  }
  isChangingPassword.value = false
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
.profile-page {
  padding: 24px;
  max-width: 1200px;
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

// Page Header
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
      color: #6366f1;
    }
  }

  .page-subtitle {
    color: #64748b;
    font-size: 0.95rem;
  }
}

// Main Content - Two Column Layout
.profile-content {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

// Cards
.profile-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;

  &:hover {
    border-color: rgba(99, 102, 241, 0.25);
  }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  svg {
    width: 22px;
    height: 22px;
    color: #6366f1;
  }

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
  }
}

// Left Column
.left-column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// Avatar Card
.avatar-card {
  .avatar-section {
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .avatar-wrapper {
    position: relative;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    overflow: hidden;
    cursor: pointer;
    border: 4px solid rgba(99, 102, 241, 0.2);
    transition: all 0.3s ease;

    &:hover {
      border-color: rgba(99, 102, 241, 0.4);
      transform: scale(1.02);

      .avatar-overlay {
        opacity: 1;
      }
    }
  }

  .avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .avatar-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    display: flex;
    align-items: center;
    justify-content: center;

    span {
      font-size: 3rem;
      font-weight: 700;
      color: white;
    }
  }

  .avatar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;

    svg {
      width: 32px;
      height: 32px;
      color: white;
      margin-bottom: 8px;
    }

    span {
      font-size: 0.85rem;
      color: white;
      font-weight: 500;
    }
  }

  .avatar-hint {
    margin-top: 16px;
    font-size: 0.85rem;
    color: #64748b;
  }
}

// Info Card
.info-card {
  .info-list {
    padding: 16px 24px 24px;
  }

  .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid rgba(99, 102, 241, 0.1);

    &:last-child {
      border-bottom: none;
    }
  }

  .info-label {
    font-size: 0.9rem;
    color: #94a3b8;
  }

  .info-value {
    font-size: 0.95rem;
    color: #f8fafc;
    font-weight: 500;
  }
}

// Right Column
.right-column {
  display: flex;
  flex-direction: column;
}

// Password Card
.password-card {
  height: fit-content;

  .password-form {
    padding: 24px;
  }

  .form-group {
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #94a3b8;
    }
  }

  .input-wrapper {
    position: relative;

    input {
      width: 100%;
      padding: 12px 44px 12px 16px;
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
    }

    .toggle-btn {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
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

      &:hover {
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.05);
      }

      svg {
        width: 18px;
        height: 18px;
      }
    }
  }

  .submit-btn {
    width: 100%;
    padding: 14px 24px;
    margin-top: 8px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

    &:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
    }

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }
  }
}

.btn-spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

// Responsive
@media (max-width: 768px) {
  .profile-page {
    padding: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .avatar-card .avatar-wrapper {
    width: 120px;
    height: 120px;
  }

  .avatar-placeholder span {
    font-size: 2.5rem;
  }
}
</style>
