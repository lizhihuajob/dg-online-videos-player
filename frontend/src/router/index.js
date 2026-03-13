import { createRouter, createWebHistory } from 'vue-router'
import VideoList from '@/views/VideoList.vue'
import VideoDetail from '@/views/VideoDetail.vue'
import Profile from '@/views/Profile.vue'

const routes = [
  {
    path: '/',
    name: 'VideoList',
    component: VideoList
  },
  {
    path: '/video/:id',
    name: 'VideoDetail',
    component: VideoDetail
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token')
    if (!token) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
