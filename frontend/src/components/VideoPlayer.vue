<template>
  <div class="video-player-container">
    <div ref="videoContainer" class="video-wrapper"></div>
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>正在加载视频...</p>
    </div>
    <div v-if="error" class="error-message">
      <p>⚠️ 视频加载失败</p>
      <p class="error-detail">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Player from 'xgplayer'
import HlsPlugin from 'xgplayer-hls'
import 'xgplayer/dist/index.min.css'

const props = defineProps({
  url: {
    type: String,
    required: true
  },
  format: {
    type: String,
    default: 'mp4'
  }
})

const emit = defineEmits(['ready', 'error', 'timeupdate'])

const videoContainer = ref(null)
let player = null
const error = ref(null)
const loading = ref(true)

const initPlayer = () => {
  if (!videoContainer.value || !props.url) return

  // 销毁旧播放器
  if (player) {
    player.destroy()
    player = null
  }

  error.value = null
  loading.value = true

  try {
    const plugins = []
    if (props.format === 'm3u8' || props.url.includes('.m3u8')) {
      plugins.push(HlsPlugin)
    }

    const config = {
      el: videoContainer.value,
      url: props.url,
      width: '100%',
      height: '100%',
      autoplay: true, // Auto play for better UX when clicking history or entering URL
      playsinline: true,
      'x5-video-player-type': 'h5',
      'x5-video-player-fullscreen': 'true',
      'webkit-playsinline': 'true',
      fluid: false,
      fitVideoSize: 'contain',
      videoFillMode: 'contain',
      lang: 'zh-cn',
      defaultPlaybackRate: 1,
      playbackRate: [0.5, 0.75, 1, 1.5, 2],
      loop: false,
      closeVideoClick: false,
      closeVideoDblclick: false,
      progressDot: true,
      miniProgressBar: true,
      controls: true,
      plugins: plugins
    }

    player = new Player(config)

    player.on('error', (err) => {
      console.error('播放器错误:', err)
      error.value = err.message || '视频播放失败'
      loading.value = false
      emit('error', err)
    })

    player.on('ready', () => {
      loading.value = false
      emit('ready')
    })

    player.on('canplay', () => {
      loading.value = false
    })

    player.on('waiting', () => {
      loading.value = true
    })

    player.on('playing', () => {
      loading.value = false
    })

    player.on('timeupdate', () => {
      if (player) {
        emit('timeupdate', {
          currentTime: player.currentTime,
          duration: player.duration
        })
      }
    })

  } catch (err) {
    console.error('播放器初始化失败:', err)
    error.value = '播放器初始化失败'
    loading.value = false
    emit('error', err)
  }
}

onMounted(() => {
  initPlayer()
})

onBeforeUnmount(() => {
  if (player) {
    player.destroy()
    player = null
  }
})

watch([() => props.url, () => props.format], () => {
  initPlayer()
})
</script>

<style lang="scss" scoped>
.video-player-container {
  width: 100%;
  height: 100%;
  background: #000;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  :deep(.xgplayer) {
    width: 100% !important;
    height: 100% !important;
    background: #000 !important;

    video {
      object-fit: contain;
    }
  }
}

.error-message {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 10;

  p {
    margin: 8px 0;
  }

  .error-detail {
    font-size: 0.9rem;
    color: #fca5a5;
  }
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 5;

  p {
    margin-top: 15px;
    font-size: 0.9rem;
    color: #94a3b8;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
