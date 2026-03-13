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
    component: Profile
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
