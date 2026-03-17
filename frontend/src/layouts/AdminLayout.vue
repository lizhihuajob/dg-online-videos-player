<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M10 8l6 4-6 4V8z" fill="currentColor"/>
          </svg>
          <span v-if="!isSidebarCollapsed" class="logo-text">视频管理</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <component :is="item.icon" class="nav-icon" />
          <span v-if="!isSidebarCollapsed" class="nav-text">{{ item.name }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info" v-if="!isSidebarCollapsed">
          <div class="user-avatar" @click="goToProfile">
            <img v-if="authStore.avatarUrl" :src="authStore.avatarUrl" alt="avatar">
            <span v-else>{{ authStore.userInitial }}</span>
          </div>
          <div class="user-details">
            <span class="username">{{ authStore.currentUser?.username }}</span>
            <span class="user-role">管理员</span>
          </div>
        </div>
        <div v-else class="user-avatar-mini" @click="goToProfile">
          <img v-if="authStore.avatarUrl" :src="authStore.avatarUrl" alt="avatar">
          <span v-else>{{ authStore.userInitial }}</span>
        </div>

        <button class="logout-btn" @click="handleLogout" :title="isSidebarCollapsed ? '退出登录' : ''">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
          </svg>
          <span v-if="!isSidebarCollapsed">退出登录</span>
        </button>
      </div>

      <!-- Collapse Toggle -->
      <button class="collapse-toggle" @click="isSidebarCollapsed = !isSidebarCollapsed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'rotated': isSidebarCollapsed }">
          <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5"/>
        </svg>
      </button>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="content-header">
        <h1 class="page-title">{{ pageTitle }}</h1>
      </header>
      <div class="content-body">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isSidebarCollapsed = ref(false)

// 菜单图标组件
const VideoIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('rect', { x: '2', y: '2', width: '20', height: '20', rx: '2.18', ry: '2.18' }),
  h('line', { x1: '7', y1: '2', x2: '7', y2: '22' }),
  h('line', { x1: '17', y1: '2', x2: '17', y2: '22' }),
  h('line', { x1: '2', y1: '12', x2: '22', y2: '12' }),
  h('line', { x1: '2', y1: '7', x2: '7', y2: '7' }),
  h('line', { x1: '2', y1: '17', x2: '7', y2: '17' }),
  h('line', { x1: '17', y1: '17', x2: '22', y2: '17' }),
  h('line', { x1: '17', y1: '7', x2: '22', y2: '7' })
])

const HistoryIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('circle', { cx: '12', cy: '12', r: '10' }),
  h('polyline', { points: '12 6 12 12 16 14' })
])

const UserIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }),
  h('circle', { cx: '12', cy: '7', r: '4' })
])

const FolderIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
  h('path', { d: 'M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z' })
])

const menuItems = [
  { name: '视频管理', path: '/', icon: VideoIcon },
  { name: '分组管理', path: '/groups', icon: FolderIcon },
  { name: '播放记录', path: '/history', icon: HistoryIcon },
  { name: '个人中心', path: '/profile', icon: UserIcon }
]

const pageTitle = computed(() => {
  const item = menuItems.find(item => item.path === route.path)
  return item?.name || '视频管理'
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

function goToProfile() {
  router.push('/profile')
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
  background: rgba(15, 23, 42, 0.9);
  border-right: 1px solid rgba(99, 102, 241, 0.12);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: width 0.3s ease;
  backdrop-filter: blur(20px);

  &.collapsed {
    width: 80px;

    .sidebar-header .logo {
      justify-content: center;
      padding: 0;
    }

    .sidebar-nav .nav-item {
      justify-content: center;
      padding: 14px;
    }

    .sidebar-footer {
      align-items: center;
      padding: 16px 12px;
    }
  }
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  .logo {
    display: flex;
    align-items: center;
    gap: 12px;

    svg {
      width: 32px;
      height: 32px;
      color: #6366f1;
      flex-shrink: 0;
    }

    .logo-text {
      font-size: 1.2rem;
      font-weight: 700;
      background: linear-gradient(135deg, #f8fafc 0%, #a5b4fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      white-space: nowrap;
    }
  }
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;

  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    margin-bottom: 4px;
    border-radius: 12px;
    color: #94a3b8;
    text-decoration: none;
    transition: all 0.25s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #c7d2fe;
    }

    &.active {
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
      color: #f8fafc;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .nav-icon {
      width: 22px;
      height: 22px;
      flex-shrink: 0;
    }

    .nav-text {
      font-size: 0.95rem;
      font-weight: 500;
      white-space: nowrap;
    }
  }
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: rgba(99, 102, 241, 0.08);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.25s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.15);
    }

    .user-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
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
      overflow: hidden;

      .username {
        font-size: 0.9rem;
        font-weight: 600;
        color: #f8fafc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .user-role {
        font-size: 0.75rem;
        color: #64748b;
      }
    }
  }

  .user-avatar-mini {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
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

  .logout-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px;
    background: transparent;
    border: 1px solid rgba(239, 68, 68, 0.2);
    border-radius: 10px;
    color: #ef4444;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.25s ease;

    &:hover {
      background: rgba(239, 68, 68, 0.1);
      border-color: rgba(239, 68, 68, 0.4);
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.collapse-toggle {
  position: absolute;
  top: 50%;
  right: -12px;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  transition: all 0.25s ease;

  &:hover {
    transform: scale(1.1);
  }

  svg {
    width: 14px;
    height: 14px;
    color: white;
    transition: transform 0.3s ease;

    &.rotated {
      transform: rotate(180deg);
    }
  }
}

.main-content {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;

  .sidebar.collapsed + & {
    margin-left: 80px;
  }
}

.content-header {
  padding: 24px 32px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  .page-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
  }
}

.content-body {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;

    .logo-text,
    .nav-text,
    .user-details,
    .logout-btn span {
      display: none;
    }

    .collapse-toggle {
      display: none;
    }
  }

  .main-content {
    margin-left: 80px;
  }

  .content-header,
  .content-body {
    padding: 20px 24px;
  }
}
</style>
