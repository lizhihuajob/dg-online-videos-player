<template>
  <div class="login-container">
    <div class="login-card glass">
      <div class="login-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M10 8l6 4-6 4V8z" fill="currentColor"/>
          </svg>
        </div>
        <h1>Vision Player</h1>
        <p>视频管理系统</p>
      </div>
      
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <input 
              type="text" 
              v-model="form.username" 
              placeholder="请输入用户名"
              :disabled="loading"
            >
          </div>
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <input 
              type="password" 
              v-model="form.password" 
              placeholder="请输入密码"
              :disabled="loading"
            >
          </div>
        </div>
        
        <div v-if="errorMessage" class="error-message">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ errorMessage }}
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading || !isFormValid">
          <span v-if="loading" class="btn-spinner"></span>
          <span v-else>登 录</span>
        </button>
      </form>
      
      <div class="login-footer">
        <p>默认账号: admin / 123456</p>
      </div>
    </div>
    
    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE = 'http://localhost:8000'

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const errorMessage = ref('')

const isFormValid = computed(() => {
  return form.value.username.trim() && form.value.password.trim()
})

const handleLogin = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  errorMessage.value = ''
  
  try {
    const formData = new FormData()
    formData.append('username', form.value.username)
    formData.append('password', form.value.password)
    
    const response = await fetch(`${API_BASE}/token`, {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('current_user', JSON.stringify(data.user))
      router.push('/admin/videos')
    } else {
      const error = await response.json()
      errorMessage.value = error.detail || '登录失败，请检查用户名和密码'
    }
  } catch (err) {
    errorMessage.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 24px;
  padding: 40px;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  position: relative;
  z-index: 10;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  
  .logo {
    width: 72px;
    height: 72px;
    margin: 0 auto 20px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
    
    svg {
      width: 40px;
      height: 40px;
      color: white;
    }
  }
  
  h1 {
    font-size: 1.75rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }
  
  p {
    color: #64748b;
    font-size: 0.95rem;
  }
}

.login-form {
  .form-group {
    margin-bottom: 24px;
    
    label {
      display: block;
      margin-bottom: 8px;
      font-size: 0.9rem;
      color: #94a3b8;
      font-weight: 500;
    }
    
    .input-wrapper {
      position: relative;
      
      svg {
        position: absolute;
        left: 16px;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        color: #64748b;
      }
      
      input {
        width: 100%;
        padding: 14px 16px 14px 48px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        color: #f8fafc;
        font-size: 1rem;
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
  }
  
  .error-message {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 10px;
    color: #fca5a5;
    font-size: 0.9rem;
    margin-bottom: 20px;
    
    svg {
      width: 18px;
      height: 18px;
      flex-shrink: 0;
    }
  }
  
  .login-btn {
    width: 100%;
    padding: 14px 24px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 1rem;
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

.login-footer {
  margin-top: 32px;
  text-align: center;
  
  p {
    color: #64748b;
    font-size: 0.85rem;
    padding: 12px 16px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 8px;
  }
}

.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  
  .circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.1;
    
    &.circle-1 {
      width: 600px;
      height: 600px;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      top: -200px;
      right: -200px;
    }
    
    &.circle-2 {
      width: 400px;
      height: 400px;
      background: linear-gradient(135deg, #8b5cf6, #a78bfa);
      bottom: -100px;
      left: -100px;
    }
    
    &.circle-3 {
      width: 300px;
      height: 300px;
      background: linear-gradient(135deg, #6366f1, #4f46e5);
      top: 50%;
      left: 10%;
      transform: translateY(-50%);
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

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }
  
  .login-header {
    .logo {
      width: 60px;
      height: 60px;
      border-radius: 16px;
      
      svg {
        width: 32px;
        height: 32px;
      }
    }
    
    h1 {
      font-size: 1.5rem;
    }
  }
}
</style>
