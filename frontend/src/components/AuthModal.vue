<template>
  <div class="auth-modal-overlay" @click.self="$emit('close')">
    <div class="auth-modal glass">
      <button class="close-btn" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 6L6 18M6 6l12 12"/>
        </svg>
      </button>

      <div class="auth-header">
        <svg class="auth-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        <h2>{{ isLogin ? '登录' : '注册' }}</h2>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label>用户名</label>
          <input 
            type="text" 
            v-model="form.username" 
            placeholder="请输入用户名"
            required
            minlength="3"
          >
        </div>

        <div v-if="!isLogin" class="form-group">
          <label>邮箱</label>
          <input 
            type="email" 
            v-model="form.email" 
            placeholder="请输入邮箱"
            required
          >
        </div>

        <div class="form-group">
          <label>密码</label>
          <input 
            type="password" 
            v-model="form.password" 
            placeholder="请输入密码"
            required
            minlength="6"
          >
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>

      <div class="auth-switch">
        <span>{{ isLogin ? '没有账号？' : '已有账号？' }}</span>
        <button type="button" class="switch-btn" @click="isLogin = !isLogin">
          {{ isLogin ? '立即注册' : '立即登录' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useHistoryStore } from '@/stores/history'

const emit = defineEmits(['close'])

const userStore = useUserStore()
const historyStore = useHistoryStore()

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  email: '',
  password: ''
})

const handleSubmit = async () => {
  error.value = ''
  loading.value = true
  
  try {
    if (isLogin.value) {
      await userStore.login(form.username, form.password)
    } else {
      await userStore.register(form.username, form.email, form.password)
    }
    await historyStore.loadHistory()
    emit('close')
  } catch (err) {
    error.value = err.message || '操作失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.auth-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3000;
  backdrop-filter: blur(8px);
}

.auth-modal {
  width: 90%;
  max-width: 420px;
  background: rgba(30, 41, 59, 0.95);
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;

  &.glass {
    backdrop-filter: blur(16px);
  }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
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

.auth-header {
  text-align: center;
  margin-bottom: 32px;

  .auth-icon {
    width: 48px;
    height: 48px;
    color: #6366f1;
    margin-bottom: 16px;
  }

  h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
  }
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;

  label {
    font-size: 0.875rem;
    color: #94a3b8;
    font-weight: 500;
  }

  input {
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: #f8fafc;
    font-size: 0.95rem;
    transition: all 0.2s;

    &::placeholder {
      color: #475569;
    }

    &:focus {
      outline: none;
      border-color: #6366f1;
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
  }
}

.error-message {
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;
  color: #fb7185;
  font-size: 0.875rem;
  text-align: center;
}

.submit-btn {
  padding: 14px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.auth-switch {
  margin-top: 24px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;

  span {
    color: #64748b;
    font-size: 0.875rem;
  }

  .switch-btn {
    background: transparent;
    border: none;
    color: #6366f1;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.2s;

    &:hover {
      color: #a5b4fc;
    }
  }
}
</style>
