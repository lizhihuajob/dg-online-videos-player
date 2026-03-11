<template>
  <div class="video-detail-container">
    <!-- 返回按钮 -->
    <div class="back-button" @click="goBack">
      <svg class="back-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M19 12H5M12 19l-7-7 7-7"/>
      </svg>
      <span>返回列表</span>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="!currentVideo" class="error-container">
      <p>⚠️ 视频不存在</p>
    </div>

    <div v-else class="content-wrapper">
      <!-- 视频播放器 -->
      <div class="player-section glass">
        <VideoPlayer
          :url="currentVideo.url"
          :format="currentVideo.format"
          @ready="onPlayerReady"
          @error="onPlayerError"
        />
      </div>

      <!-- 视频信息 -->
      <div class="video-info-section">
        <h1 class="video-title">{{ currentVideo.title }}</h1>
        <div class="video-meta">
          <span class="meta-item">
            <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            {{ currentVideo.duration }}
          </span>
          <span class="meta-item">
            <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            {{ formatDate(currentVideo.date) }}
          </span>
          <span class="meta-item format-badge">{{ currentVideo.format.toUpperCase() }}</span>
        </div>
        <p class="video-description">{{ currentVideo.description }}</p>
      </div>

      <!-- 播放列表 -->
      <div class="playlist-section">
        <h2 class="playlist-title">
          <svg class="playlist-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"/>
            <line x1="8" y1="12" x2="21" y2="12"/>
            <line x1="8" y1="18" x2="21" y2="18"/>
            <line x1="3" y1="6" x2="3.01" y2="6"/>
            <line x1="3" y1="12" x2="3.01" y2="12"/>
            <line x1="3" y1="18" x2="3.01" y2="18"/>
          </svg>
          播放列表
        </h2>
        <div class="playlist-items">
          <div
            v-for="video in videos"
            :key="video.id"
            class="playlist-item"
            :class="{ active: video.id === currentVideo.id }"
            @click="playVideo(video)"
          >
            <div class="playlist-thumb-wrapper">
              <img :src="video.cover" :alt="video.title" class="playlist-thumb" />
              <div class="playlist-duration">{{ video.duration }}</div>
              <div v-if="video.id === currentVideo.id" class="playing-indicator">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
                </svg>
              </div>
            </div>
            <div class="playlist-item-info">
              <h3 class="playlist-item-title">{{ video.title }}</h3>
              <p class="playlist-item-desc">{{ video.description }}</p>
            </div>
            <div v-if="video.id !== currentVideo.id" class="play-btn">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 自定义弹窗 -->
    <div v-if="isModalVisible" class="modal-overlay" @click.self="closeModal">
      <div class="modal-card glass">
        <div class="modal-header">
          <svg class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3>{{ modalTitle }}</h3>
        </div>
        <div class="modal-body">
          <p>{{ modalMessage }}</p>
        </div>
        <div class="modal-footer">
          <button class="modal-btn" @click="closeModal">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import VideoPlayer from '@/components/VideoPlayer.vue'

const API_BASE = '/api'

const router = useRouter()
const route = useRoute()

const videos = ref([])
const loading = ref(true)
const currentVideo = ref(null)

const savePlayRecord = async (video) => {
  try {
    await fetch(`${API_BASE}/play-records`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        video_id: String(video.id),
        video_title: video.title,
        video_url: video.url
      })
    })
  } catch (err) {
    console.warn('保存播放记录失败:', err)
  }
}

onMounted(async () => {
  const id = route.params.id
  
  if (id === 'online' || id === 'local') {
    currentVideo.value = {
      id,
      title: route.query.title || (id === 'online' ? '在线视频' : '本地视频'),
      url: route.query.url,
      format: route.query.format || 'mp4',
      description: id === 'online' ? `来源: ${route.query.url}` : '本地上传视频文件',
      date: new Date().toISOString(),
      duration: '--:--'
    }
    loading.value = false
    savePlayRecord(currentVideo.value)
  } else {
    try {
      const res = await fetch(`${API_BASE}/videos`)
      videos.value = await res.json()
      const video = videos.value.find(v => String(v.id) === id)
      if (video) {
        currentVideo.value = video
        savePlayRecord(video)
      }
      loading.value = false
    } catch (err) {
      console.error('获取视频列表失败:', err)
      loading.value = false
    }
  }
})

const goBack = () => {
  router.push('/')
}

const playVideo = (video) => {
  if (video.id !== currentVideo.value?.id) {
    currentVideo.value = video
    // 滚动到播放器顶部
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const onPlayerReady = () => {
  console.log('播放器准备就绪')
}

const onPlayerError = (err) => {
  console.error('播放器错误:', err)
  showModal('播放失败', `无法加载视频资源，请检查 URL 是否正确。错误信息: ${err.message || '未知错误'}`)
}

const modalTitle = ref('')
const modalMessage = ref('')
const isModalVisible = ref(false)

const showModal = (title, message) => {
  modalTitle.value = title
  modalMessage.value = message
  isModalVisible.value = true
}

const closeModal = () => {
  isModalVisible.value = false
}
</script>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  width: 90%;
  max-width: 400px;
  background: rgba(30, 41, 59, 0.9);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  text-align: center;

  &.glass {
    backdrop-filter: blur(16px);
  }
}

.modal-header {
  margin-bottom: 20px;

  .modal-icon {
    width: 48px;
    height: 48px;
    color: #ef4444;
    margin: 0 auto 15px;
  }

  h3 {
    font-size: 1.5rem;
    color: #f8fafc;
    margin: 0;
  }
}

.modal-body {
  margin-bottom: 30px;
  p {
    color: #94a3b8;
    line-height: 1.6;
    margin: 0;
  }
}

.modal-btn {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
  }
}

.video-detail-container {
  min-height: 100vh;
  padding: 20px;
  background: var(--background-gradient);
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: white;
  border-radius: 50px;
  color: #6366f1;
  font-weight: 500;
  cursor: pointer;
  box-shadow: var(--card-shadow);
  transition: var(--transition);
  margin-bottom: 24px;
  user-select: none;

  &:hover {
    background: #6366f1;
    color: white;
    transform: translateX(-3px);
    box-shadow: var(--card-hover-shadow);
  }

  &:active {
    transform: translateX(-1px);
  }
}

.back-icon {
  width: 20px;
  height: 20px;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  font-size: 1.1rem;
  color: #6b7280;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.player-section {
  margin-bottom: 30px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
  background: #000;
  border: 1px solid rgba(255, 255, 255, 0.1);

  &.glass {
    backdrop-filter: blur(10px);
  }
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.player-section {
  background: #000;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--card-shadow);
  margin-bottom: 24px;
  position: relative;
}

.video-info-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--card-shadow);
  margin-bottom: 32px;
}

.video-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 16px;
  line-height: 1.3;
}

.video-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
  align-items: center;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #6b7280;
  font-size: 0.95rem;
}

.meta-icon {
  width: 18px;
  height: 18px;
}

.format-badge {
  padding: 4px 12px;
  background: linear-gradient(135deg, #6366f1, #ec4899);
  color: white;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.video-description {
  color: #6b7280;
  line-height: 1.7;
  font-size: 1rem;
}

.playlist-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--card-shadow);
}

.playlist-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 24px;
}

.playlist-icon {
  width: 28px;
  height: 28px;
  color: #6366f1;
}

.playlist-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: var(--transition);
  border: 2px solid transparent;

  &:hover {
    background: #f9fafb;
    transform: translateX(5px);
  }

  &:active {
    transform: translateX(2px);
  }

  &.active {
    background: #f0fdf4;
    border-color: #6366f1;
  }
}

.playlist-thumb-wrapper {
  position: relative;
  width: 140px;
  padding-top: 56.25%; // 16:9
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.playlist-thumb {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.playlist-duration {
  position: absolute;
  bottom: 6px;
  right: 6px;
  background: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  backdrop-filter: blur(4px);
}

.playing-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(99, 102, 241, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;

  svg {
    width: 32px;
    height: 32px;
    color: #6366f1;
    animation: pulse 1.5s ease-in-out infinite;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.playlist-item-info {
  flex: 1;
  min-width: 0;
}

.playlist-item-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-item-desc {
  font-size: 0.85rem;
  color: #9ca3af;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.play-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #ec4899);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  transition: var(--transition);

  svg {
    width: 20px;
    height: 20px;
    margin-left: 2px;
  }
}

.playlist-item:hover .play-btn {
  transform: scale(1.1);
}

// 移动端适配
@media (max-width: 768px) {
  .video-detail-container {
    padding: 16px;
  }

  .back-button {
    padding: 10px 16px;
    font-size: 0.9rem;
    margin-bottom: 16px;
  }

  .video-info-section {
    padding: 16px;
    margin-bottom: 24px;
  }

  .video-title {
    font-size: 1.4rem;
  }

  .video-meta {
    gap: 12px;
  }

  .meta-item {
    font-size: 0.85rem;
  }

  .playlist-section {
    padding: 16px;
  }

  .playlist-title {
    font-size: 1.3rem;
  }

  .playlist-item {
    flex-direction: column;
    align-items: stretch;
    padding: 12px;
  }

  .playlist-thumb-wrapper {
    width: 100%;
  }

  .playlist-item-info {
    margin-top: 10px;
  }

  .play-btn {
    display: none;
  }
}

// 平板适配
@media (min-width: 769px) and (max-width: 1024px) {
  .video-title {
    font-size: 1.5rem;
  }

  .playlist-thumb-wrapper {
    width: 120px;
  }
}
</style>
