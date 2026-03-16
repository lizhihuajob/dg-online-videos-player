import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import AdminLayout from '@/views/AdminLayout.vue'
import VideoManagement from '@/views/VideoManagement.vue'
import PlayHistory from '@/views/PlayHistory.vue'
import AdminProfile from '@/views/AdminProfile.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/admin/videos'
      },
      {
        path: 'videos',
        name: 'VideoManagement',
        component: VideoManagement
      },
      {
        path: 'history',
        name: 'PlayHistory',
        component: PlayHistory
      },
      {
        path: 'profile',
        name: 'AdminProfile',
        component: AdminProfile
      }
    ]
  },
  {
    path: '/',
    redirect: '/admin/videos'
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/admin/videos'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.guest && token) {
    next('/admin/videos')
  } else {
    next()
  }
})

export default router
