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
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import Player from 'xgplayer'
import 'xgplayer/dist/index.min.css'

const props = defineProps({
  url: {
    type: String,
    required: true
  },
  format: {
    type: String,
    default: 'mp4'
  },
  hasPrev: {
    type: Boolean,
    default: false
  },
  hasNext: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['ready', 'error', 'timeupdate', 'prev', 'next'])

const videoContainer = ref(null)
let player = null
const error = ref(null)
const loading = ref(true)

const addCustomButtons = async () => {
  if (!player || !player.root) return

  // 等待控制栏渲染完成
  await nextTick()

  const controls = player.root.querySelector('.xgplayer-controls')
  const playBtn = player.root.querySelector('.xgplayer-play')
  if (!controls || !playBtn) {
    // 如果控制栏还没渲染，延迟再试
    setTimeout(addCustomButtons, 100)
    return
  }

  // 移除已存在的自定义按钮
  const existingPrev = controls.querySelector('.xgplayer-prev-btn')
  const existingNext = controls.querySelector('.xgplayer-next-btn')
  if (existingPrev) existingPrev.remove()
  if (existingNext) existingNext.remove()

  // 添加上一个按钮
  if (props.hasPrev) {
    const prevBtn = document.createElement('div')
    prevBtn.className = 'xgplayer-prev-btn xgplayer-custom-btn'
    prevBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6V6zm3.5 6l8.5 6V6l-8.5 6z"/></svg>'
    prevBtn.title = '上一个'
    prevBtn.style.cssText = 'width:40px;height:40px;display:flex;align-items:center;justify-content:center;cursor:pointer;margin:0 4px;'
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation()
      e.preventDefault()
      emit('prev')
    })
    playBtn.insertAdjacentElement('afterend', prevBtn)
  }

  // 添加下一个按钮
  if (props.hasNext) {
    const nextBtn = document.createElement('div')
    nextBtn.className = 'xgplayer-next-btn xgplayer-custom-btn'
    nextBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>'
    nextBtn.title = '下一个'
    nextBtn.style.cssText = 'width:40px;height:40px;display:flex;align-items:center;justify-content:center;cursor:pointer;margin:0 4px;'
    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation()
      e.preventDefault()
      emit('next')
    })
    playBtn.insertAdjacentElement('afterend', nextBtn)
  }
}

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
    const config = {
      el: videoContainer.value,
      url: props.url,
      width: '100%',
      height: '100%',
      autoplay: true,
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
      controls: true
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
      // 添加自定义上一个/下一个按钮
      addCustomButtons()
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
  background: linear-gradient(145deg, #0a0a0a 0%, #1a1a2e 100%);
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 16px;
  overflow: hidden;
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
    background: transparent !important;

    video {
      object-fit: contain;
    }

    .xgplayer-controls {
      background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent) !important;
    }

    .xgplayer-progress {
      .xgplayer-progress-played {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
      }
    }

    .xgplayer-time {
      color: #e2e8f0 !important;
    }

    .xgplayer-custom-btn {
      width: 40px !important;
      height: 40px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      cursor: pointer !important;
      margin: 0 4px !important;
      flex-shrink: 0 !important;

      svg {
        width: 24px !important;
        height: 24px !important;
        color: #e2e8f0 !important;
        transition: all 0.2s ease;
        pointer-events: none;
      }

      &:hover svg {
        color: #6366f1 !important;
        transform: scale(1.1);
      }

      &:active svg {
        transform: scale(0.95);
      }
    }
  }
}

.error-message {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #f8fafc;
  z-index: 10;
  backdrop-filter: blur(8px);

  p {
    margin: 8px 0;
  }

  .error-detail {
    font-size: 0.85rem;
    color: #fca5a5;
    max-width: 80%;
    text-align: center;
    line-height: 1.5;
  }
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #f8fafc;
  z-index: 5;
  backdrop-filter: blur(4px);

  p {
    margin-top: 16px;
    font-size: 0.9rem;
    color: #94a3b8;
    letter-spacing: 0.5px;
  }

  .spinner {
    width: 44px;
    height: 44px;
    border: 3px solid rgba(99, 102, 241, 0.2);
    border-top-color: #6366f1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
