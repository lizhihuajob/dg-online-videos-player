import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import Login from '@/views/Login.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import VideoManagement from '@/views/VideoManagement.vue'
import PlayHistory from '@/views/PlayHistory.vue'
import Profile from '@/views/Profile.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true }
  },
  {
    path: '/',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'VideoManagement',
        component: VideoManagement
      },
      {
        path: '/history',
        name: 'PlayHistory',
        component: PlayHistory
      },
      {
        path: '/profile',
        name: 'Profile',
        component: Profile
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Initialize auth state
  if (!authStore.isLoggedIn) {
    authStore.init()
  }

  // Redirect to login if not authenticated
  if (!to.meta.public && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && authStore.isLoggedIn) {
    // Redirect to home if already logged in
    next('/')
  } else {
    next()
  }
})

export default router
