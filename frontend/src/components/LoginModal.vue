<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-card glass">
      <div class="modal-header">
        <h3>{{ isLogin ? '用户登录' : '用户注册' }}</h3>
        <button class="close-btn" @click="close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-group">
          <label>用户名</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            required
            minlength="3"
            maxlength="50"
          >
        </div>

        <div class="form-group">
          <label>密码</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            required
            minlength="6"
          >
        </div>

        <div v-if="!isLogin" class="form-group">
          <label>确认密码</label>
          <input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
            minlength="6"
          >
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          <span v-else>{{ isLogin ? '登录' : '注册' }}</span>
        </button>
      </form>

      <div class="switch-mode">
        <span>{{ isLogin ? '还没有账号？' : '已有账号？' }}</span>
        <button class="switch-btn" @click="toggleMode">
          {{ isLogin ? '立即注册' : '立即登录' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'success'])

const userStore = useUserStore()
const isLogin = ref(true)
const isLoading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const close = () => {
  emit('update:modelValue', false)
  resetForm()
}

const resetForm = () => {
  form.username = ''
  form.password = ''
  form.confirmPassword = ''
  error.value = ''
  userStore.clearError()
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  form.password = ''
  form.confirmPassword = ''
}

const handleSubmit = async () => {
  error.value = ''

  // 表单验证
  if (form.username.length < 3) {
    error.value = '用户名至少需要3个字符'
    return
  }

  if (form.password.length < 6) {
    error.value = '密码至少需要6个字符'
    return
  }

  if (!isLogin.value && form.password !== form.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  isLoading.value = true

  try {
    let success
    if (isLogin.value) {
      success = await userStore.login(form.username, form.password)
    } else {
      success = await userStore.register(form.username, form.password)
    }

    if (success) {
      emit('success')
      close()
    } else {
      error.value = userStore.error || '操作失败，请重试'
    }
  } catch (err) {
    error.value = err.message || '操作失败，请重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
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
  z-index: 3000;
}

.modal-card {
  width: 90%;
  max-width: 400px;
  background: rgba(30, 41, 59, 0.95);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);

  &.glass {
    backdrop-filter: blur(16px);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;

  h3 {
    font-size: 1.5rem;
    color: #f8fafc;
    margin: 0;
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
    transition: all 0.2s;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #f8fafc;
    }

    svg {
      width: 20px;
      height: 20px;
    }
  }
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;

  label {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 500;
  }

  input {
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    transition: all 0.3s;

    &::placeholder {
      color: #475569;
    }

    &:focus {
      border-color: #6366f1;
      background: rgba(15, 23, 42, 0.8);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
    }
  }
}

.error-message {
  padding: 10px 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.85rem;
}

.submit-btn {
  padding: 14px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 8px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.switch-mode {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9rem;
  color: #64748b;

  .switch-btn {
    background: transparent;
    border: none;
    color: #6366f1;
    font-weight: 600;
    cursor: pointer;
    margin-left: 4px;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
