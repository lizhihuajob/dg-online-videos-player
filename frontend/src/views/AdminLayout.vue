<template>
  <div class="admin-layout">
    <aside class="sidebar glass">
      <div class="sidebar-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M10 8l6 4-6 4V8z" fill="currentColor"/>
          </svg>
          <span>Vision Player</span>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/admin/videos" class="nav-item" :class="{ active: $route.path === '/admin/videos' }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
            <line x1="7" y1="2" x2="7" y2="22"/>
            <line x1="17" y1="2" x2="17" y2="22"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <line x1="2" y1="7" x2="7" y2="7"/>
            <line x1="2" y1="17" x2="7" y2="17"/>
            <line x1="17" y1="17" x2="22" y2="17"/>
            <line x1="17" y1="7" x2="22" y2="7"/>
          </svg>
          <span>视频管理</span>
        </router-link>
        
        <router-link to="/admin/history" class="nav-item" :class="{ active: $route.path === '/admin/history' }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <span>播放记录</span>
        </router-link>
        
        <router-link to="/admin/profile" class="nav-item" :class="{ active: $route.path === '/admin/profile' }">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          <span>个人中心</span>
        </router-link>
      </nav>
      
      <div class="sidebar-footer">
        <div class="user-info" @click="goToProfile">
          <div class="user-avatar">
            <img v-if="currentUser?.avatar" :src="getAvatarUrl(currentUser.avatar)" alt="avatar">
            <span v-else>{{ currentUser?.username?.charAt(0).toUpperCase() || 'A' }}</span>
          </div>
          <div class="user-details">
            <span class="username">{{ currentUser?.username }}</span>
            <span class="role">管理员</span>
          </div>
        </div>
        <button class="logout-btn" @click="logout" title="退出登录">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </div>
    </aside>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE = 'http://localhost:8000'

const currentUser = ref(null)

onMounted(() => {
  const user = localStorage.getItem('current_user')
  if (user) {
    currentUser.value = JSON.parse(user)
  }
})

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `${API_BASE}${avatar}`
}

const goToProfile = () => {
  router.push('/admin/profile')
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('current_user')
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: radial-gradient(ellipse at 20% 0%, #1e1b4b 0%, #0f172a 40%, #020617 100%);
}

.sidebar {
  width: 260px;
  background: rgba(15, 23, 42, 0.8);
  border-right: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 100;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  
  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
    
    svg {
      width: 36px;
      height: 36px;
      color: #6366f1;
    }
    
    span {
      font-size: 1.25rem;
      font-weight: 700;
      background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
  }
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  
  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 12px;
    color: #94a3b8;
    text-decoration: none;
    margin-bottom: 4px;
    transition: all 0.25s ease;
    
    svg {
      width: 20px;
      height: 20px;
    }
    
    span {
      font-size: 0.95rem;
      font-weight: 500;
    }
    
    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #c7d2fe;
    }
    
    &.active {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
      color: #f8fafc;
      box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.2);
    }
  }
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;
  
  .user-info {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    background: rgba(30, 41, 59, 0.5);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.25s ease;
    
    &:hover {
      background: rgba(99, 102, 241, 0.15);
    }
    
    .user-avatar {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      span {
        color: white;
        font-size: 1rem;
        font-weight: 600;
      }
    }
    
    .user-details {
      display: flex;
      flex-direction: column;
      
      .username {
        font-size: 0.9rem;
        font-weight: 600;
        color: #f8fafc;
      }
      
      .role {
        font-size: 0.75rem;
        color: #64748b;
      }
    }
  }
  
  .logout-btn {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.25s ease;
    
    svg {
      width: 20px;
      height: 20px;
    }
    
    &:hover {
      background: rgba(239, 68, 68, 0.2);
      border-color: rgba(239, 68, 68, 0.4);
      color: #f87171;
    }
  }
}

.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 24px;
  min-height: 100vh;
}

.glass {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

@media (max-width: 768px) {
  .sidebar {
    width: 70px;
    
    .sidebar-header .logo span,
    .sidebar-nav .nav-item span,
    .sidebar-footer .user-details {
      display: none;
    }
    
    .sidebar-nav .nav-item {
      justify-content: center;
      padding: 14px;
    }
    
    .sidebar-footer {
      flex-direction: column;
      gap: 8px;
      
      .user-info {
        justify-content: center;
        padding: 8px;
      }
    }
  }
  
  .main-content {
    margin-left: 70px;
  }
}
</style>
