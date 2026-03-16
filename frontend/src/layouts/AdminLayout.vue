<template>
  <div class="admin-layout">
    <aside class="sidebar glass">
      <div class="sidebar-header">
        <div class="logo">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M10 8l6 4-6 4V8z" fill="currentColor"/>
          </svg>
          <h2>视频管理系统</h2>
        </div>
      </div>

      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li class="nav-item">
            <router-link 
              to="/videos" 
              class="nav-link" 
              :class="{ active: $route.path === '/videos' }"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
                <line x1="7" y1="2" x2="7" y2="22"/>
                <line x1="17" y1="2" x2="17" y2="22"/>
                <line x1="2" y1="12" x2="22" y2="12"/>
              </svg>
              <span>视频管理</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link 
              to="/history" 
              class="nav-link" 
              :class="{ active: $route.path === '/history' }"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18V5l12-2v13"/>
                <circle cx="6" cy="18" r="3"/>
                <circle cx="18" cy="16" r="3"/>
              </svg>
              <span>播放历史</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link 
              to="/profile" 
              class="nav-link" 
              :class="{ active: $route.path === '/profile' }"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <span>个人中心</span>
            </router-link>
          </li>
        </ul>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info" @click="goToProfile">
          <div class="user-avatar">
            <img v-if="currentUser?.avatar" :src="currentUser.avatar" :alt="currentUser?.username" class="avatar-img">
            <span v-else class="avatar-text">{{ userInitial }}</span>
          </div>
          <div class="user-details">
            <span class="username">{{ currentUser?.username }}</span>
            <span class="user-role">管理员</span>
          </div>
        </div>
        <button class="logout-btn" @click="logout" title="退出登录">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentUser = ref(null)

const userInitial = computed(() => {
  return currentUser.value?.username?.charAt(0).toUpperCase() || 'A'
})

onMounted(() => {
  const user = localStorage.getItem('current_user')
  if (user) {
    currentUser.value = JSON.parse(user)
  }
})

const goToProfile = () => {
  router.push('/profile')
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
  width: 240px;
  background: rgba(30, 41, 59, 0.6);
  border-right: 1px solid rgba(99, 102, 241, 0.15);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  .logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;

    .logo-icon {
      width: 48px;
      height: 48px;
      color: #6366f1;
      filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.3));
    }

    h2 {
      font-size: 1.25rem;
      font-weight: 600;
      background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 0;
    }
  }
}

.sidebar-nav {
  flex: 1;
  padding: 16px 0;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin: 4px 12px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: #94a3b8;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  font-weight: 500;

  svg {
    width: 20px;
    height: 20px;
  }

  &:hover {
    background: rgba(99, 102, 241, 0.1);
    color: #f8fafc;
  }

  &.active {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
    color: #f8fafc;
    border-left: 3px solid #6366f1;
    border-radius: 0 8px 8px 0;
    margin-left: -3px;
  }
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
    cursor: pointer;
    padding: 8px;
    border-radius: 8px;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
    }
  }

  .user-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;

    .avatar-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .avatar-text {
      color: white;
      font-weight: 600;
      font-size: 1rem;
    }
  }

  .user-details {
    display: flex;
    flex-direction: column;

    .username {
      color: #f8fafc;
      font-weight: 500;
      font-size: 0.9rem;
    }

    .user-role {
      color: #94a3b8;
      font-size: 0.75rem;
    }
  }

  .logout-btn {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background: rgba(99, 102, 241, 0.1);
    color: #94a3b8;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;

    svg {
      width: 18px;
      height: 18px;
    }

    &:hover {
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
    }
  }
}

.main-content {
  flex: 1;
  overflow: auto;
  padding: 24px;
}

.glass {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
</style>
