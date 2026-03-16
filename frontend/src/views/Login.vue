<template>
  <div class="login-container">
    <div class="login-card glass">
      <div class="login-header">
        <div class="logo">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M10 8l6 4-6 4V8z" fill="currentColor"/>
          </svg>
          <h2>视频管理系统</h2>
        </div>
        <p>请使用管理员账号登录</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input 
            type="text" 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            required
          >
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            type="password" 
            v-model="loginForm.password" 
            placeholder="请输入密码"
            required
          >
        </div>
        <div class="hint-text">
          默认账号: admin / 123456
        </div>
        <button 
          type="submit" 
          class="login-btn"
          :disabled="isLoggingIn"
        >
          <span v-if="isLoggingIn" class="btn-spinner"></span>
          <span v-else>登录系统</span>
        </button>
      </form>
    </div>

    <div v-if="showError" class="modal-overlay" @click="showError = false">
      <div class="modal-card glass" @click.stop>
        <div class="modal-header">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3>登录失败</h3>
        </div>
        <p>{{ errorMessage }}</p>
        <button class="modal-btn" @click="showError = false">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE = 'http://localhost:8000'

const loginForm = ref({
  username: 'admin',
  password: '123456'
})
const isLoggingIn = ref(false)
const showError = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  isLoggingIn.value = true
  try {
    const formData = new FormData()
    formData.append('username', loginForm.value.username)
    formData.append('password', loginForm.value.password)
    
    const response = await fetch(`${API_BASE}/token`, {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('current_user', JSON.stringify(data.user))
      router.push('/')
    } else {
      const error = await response.json()
      errorMessage.value = error.detail || '用户名或密码错误'
      showError.value = true
    }
  } catch (err) {
    errorMessage.value = '网络错误，请稍后重试'
    showError.value = true
  } finally {
    isLoggingIn.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  background: radial-gradient(ellipse at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(10px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;

  .logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;

    .logo-icon {
      width: 48px;
      height: 48px;
      color: #6366f1;
      filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.3));
    }

    h2 {
      font-size: 1.5rem;
      font-weight: 600;
      background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
  }

  p {
    color: #94a3b8;
    font-size: 0.95rem;
  }
}

.login-form {
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
    }
  }

  .hint-text {
    margin-bottom: 24px;
    color: #6366f1;
    font-size: 0.85rem;
    text-align: center;
  }

  .login-btn {
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
</style>
