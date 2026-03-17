<template>
  <div class="profile-container">
    <div class="profile-layout">
      <!-- Left: User Info Card -->
      <div class="profile-left">
        <div class="profile-card">
          <div class="profile-header">
            <div class="avatar-section">
              <div class="avatar-wrapper" @click="triggerAvatarUpload">
                <img v-if="authStore.avatarUrl" :src="authStore.avatarUrl" alt="avatar" class="avatar-img">
                <div v-else class="avatar-placeholder">
                  <span>{{ authStore.userInitial }}</span>
                </div>
                <div class="avatar-overlay">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                    <circle cx="12" cy="13" r="4"/>
                  </svg>
                  <span>更换头像</span>
                </div>
              </div>
              <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                hidden
                @change="handleAvatarChange"
              >
            </div>

            <div class="user-info">
              <h2 class="username">{{ authStore.currentUser?.username }}</h2>
              <p class="user-email">{{ authStore.currentUser?.email }}</p>
              <span class="user-badge">管理员</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Password Change Section -->
      <div class="profile-right">
        <div class="section-card">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
            <div class="section-title">
              <h3>修改密码</h3>
              <p>更改您的登录密码</p>
            </div>
          </div>

          <div class="form-content">
            <div class="form-group">
              <label>当前密码</label>
              <div class="input-wrapper">
                <input
                  :type="showCurrentPassword ? 'text' : 'password'"
                  v-model="passwordForm.currentPassword"
                  placeholder="请输入当前密码"
                >
                <button class="toggle-btn" @click="showCurrentPassword = !showCurrentPassword">
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
                  :type="showNewPassword ? 'text' : 'password'"
                  v-model="passwordForm.newPassword"
                  placeholder="请输入新密码（至少6位）"
                >
                <button class="toggle-btn" @click="showNewPassword = !showNewPassword">
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
                  :type="showConfirmPassword ? 'text' : 'password'"
                  v-model="passwordForm.confirmPassword"
                  placeholder="请再次输入新密码"
                >
                <button class="toggle-btn" @click="showConfirmPassword = !showConfirmPassword">
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

            <div class="password-strength" v-if="passwordForm.newPassword">
              <div class="strength-bar">
                <div class="strength-fill" :style="{ width: passwordStrength + '%', background: strengthColor }"></div>
              </div>
              <span class="strength-text" :style="{ color: strengthColor }">{{ strengthText }}</span>
            </div>

            <button
              class="submit-btn"
              :disabled="!isPasswordFormValid || isUpdatingPassword"
              @click="updatePassword"
            >
              <span v-if="isUpdatingPassword" class="btn-spinner"></span>
              <span v-else>修改密码</span>
            </button>
          </div>
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
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()

// State
const avatarInput = ref(null)
const isUploadingAvatar = ref(false)

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const isUpdatingPassword = ref(false)

// Toast state
const toastMessage = ref('')
const toastType = ref('success')

// Computed
const isPasswordFormValid = computed(() => {
  return passwordForm.value.currentPassword &&
         passwordForm.value.newPassword &&
         passwordForm.value.newPassword.length >= 6 &&
         passwordForm.value.newPassword === passwordForm.value.confirmPassword
})

const passwordStrength = computed(() => {
  const pwd = passwordForm.value.newPassword
  if (!pwd) return 0

  let strength = 0
  if (pwd.length >= 6) strength += 20
  if (pwd.length >= 10) strength += 20
  if (/[a-z]/.test(pwd)) strength += 15
  if (/[A-Z]/.test(pwd)) strength += 15
  if (/[0-9]/.test(pwd)) strength += 15
  if (/[^a-zA-Z0-9]/.test(pwd)) strength += 15

  return Math.min(strength, 100)
})

const strengthColor = computed(() => {
  const strength = passwordStrength.value
  if (strength < 40) return '#ef4444'
  if (strength < 70) return '#f59e0b'
  return '#10b981'
})

const strengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength < 40) return '弱'
  if (strength < 70) return '中'
  return '强'
})

// Methods
function triggerAvatarUpload() {
  avatarInput.value?.click()
}

async function handleAvatarChange(e) {
  const file = e.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    showToast('请选择图片文件', 'error')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    showToast('图片大小不能超过5MB', 'error')
    return
  }

  isUploadingAvatar.value = true
  const result = await authStore.updateAvatar(file)

  if (result.success) {
    showToast('头像上传成功', 'success')
  } else {
    showToast(result.error, 'error')
  }

  isUploadingAvatar.value = false
  avatarInput.value.value = ''
}

async function updatePassword() {
  if (!isPasswordFormValid.value) return

  isUpdatingPassword.value = true
  const result = await authStore.updatePassword(
    passwordForm.value.currentPassword,
    passwordForm.value.newPassword
  )

  if (result.success) {
    showToast('密码修改成功', 'success')
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } else {
    showToast(result.error, 'error')
  }

  isUpdatingPassword.value = false
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
.profile-container {
  min-height: 100%;
}

.profile-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 24px;
  align-items: start;
}

.profile-left {
  position: sticky;
  top: 24px;
}

.profile-right {
  min-width: 0;
}

.profile-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 20px;

  .avatar-section {
    flex-shrink: 0;
  }

  .avatar-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    cursor: pointer;

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
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.6);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.25s ease;

      svg {
        width: 28px;
        height: 28px;
        color: white;
        margin-bottom: 6px;
      }

      span {
        font-size: 0.85rem;
        color: white;
      }
    }

    &:hover .avatar-overlay {
      opacity: 1;
    }
  }

  .user-info {
    .username {
      font-size: 1.5rem;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 6px;
    }

    .user-email {
      font-size: 0.95rem;
      color: #94a3b8;
      margin-bottom: 12px;
    }

    .user-badge {
      display: inline-block;
      padding: 6px 16px;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: 20px;
      font-size: 0.8rem;
      color: #a5b4fc;
      font-weight: 500;
    }
  }
}

.section-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  .section-icon {
    width: 48px;
    height: 48px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;

    svg {
      width: 24px;
      height: 24px;
      color: #6366f1;
    }
  }

  .section-title {
    h3 {
      font-size: 1.1rem;
      font-weight: 600;
      color: #f8fafc;
      margin-bottom: 4px;
    }

    p {
      font-size: 0.85rem;
      color: #64748b;
    }
  }
}

.form-content {
  .form-group {
    margin-bottom: 20px;

    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #e2e8f0;
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
          color: #64748b;
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
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: none;
        color: #64748b;
        cursor: pointer;
        transition: color 0.2s ease;

        &:hover {
          color: #94a3b8;
        }

        svg {
          width: 18px;
          height: 18px;
        }
      }
    }
  }

  .password-strength {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;

    .strength-bar {
      flex: 1;
      height: 4px;
      background: rgba(99, 102, 241, 0.1);
      border-radius: 2px;
      overflow: hidden;

      .strength-fill {
        height: 100%;
        border-radius: 2px;
        transition: all 0.3s ease;
      }
    }

    .strength-text {
      font-size: 0.8rem;
      font-weight: 500;
      min-width: 20px;
    }
  }

  .submit-btn {
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
      transform: translateY(-2px);
      box-shadow: 0 8px 25px -5px rgba(99, 102, 241, 0.5);
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

@keyframes spin {
  to { transform: rotate(360deg); }
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

@media (max-width: 900px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }

  .profile-left {
    position: static;
  }

  .profile-header {
    flex-direction: row;
    text-align: left;
  }

  .avatar-wrapper {
    width: 100px;
    height: 100px;

    .avatar-placeholder span {
      font-size: 2.5rem;
    }
  }
}

@media (max-width: 640px) {
  .profile-card {
    padding: 24px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;

    .avatar-wrapper {
      width: 80px;
      height: 80px;

      .avatar-placeholder span {
        font-size: 2rem;
      }
    }
  }

  .section-card {
    padding: 20px;
  }

  .section-header {
    .section-icon {
      width: 40px;
      height: 40px;

      svg {
        width: 20px;
        height: 20px;
      }
    }

    .section-title {
      h3 {
        font-size: 1rem;
      }
    }
  }
}
</style>
