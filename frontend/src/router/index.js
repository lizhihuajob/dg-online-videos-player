import { createRouter, createWebHistory } from 'vue-router'
import VideoList from '@/views/VideoList.vue'
import VideoDetail from '@/views/VideoDetail.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
