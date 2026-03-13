import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { videoData } from '@/data/videos.js'

export const useVideoStore = defineStore('video', () => {
  const videos = ref([...videoData])
  const currentVideo = ref(null)
  const currentUrl = ref('')
  const currentFormat = ref('mp4')

  const hasVideos = computed(() => videos.value.length > 0)

  const setCurrentVideo = (video) => {
    currentVideo.value = video
    if (video) {
      currentUrl.value = video.url
      currentFormat.value = video.format
    }
  }

  const playVideo = (video) => {
    setCurrentVideo(video)
  }

  const addVideo = (video) => {
    videos.value.unshift({
      id: Date.now(),
      ...video,
      date: new Date().toISOString().split('T')[0]
    })
  }

  return {
    videos,
    currentVideo,
    currentUrl,
    currentFormat,
    hasVideos,
    setCurrentVideo,
    playVideo,
    addVideo
  }
})
