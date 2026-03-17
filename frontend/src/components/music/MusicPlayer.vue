<template>
  <div class="player-overlay" @click.self="$emit('close')">
    <div class="player-modal" @click.stop>
      <div class="player-header">
        <h3>{{ music.original_name }}</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
      <div class="player-body">
        <div class="music-visual">
          <div class="visual-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 18V5l12-2v13"/>
              <circle cx="6" cy="18" r="3"/>
              <circle cx="18" cy="16" r="3"/>
            </svg>
          </div>
          <div class="visual-waves">
            <span v-for="i in 5" :key="i" :style="{ animationDelay: i * 0.1 + 's' }"></span>
          </div>
        </div>
        <audio
          ref="audioPlayer"
          :src="musicUrl"
          controls
          autoplay
          @ended="$emit('close')"
        ></audio>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  music: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const audioPlayer = ref(null)
const API_BASE = 'http://localhost:8000'

const musicUrl = computed(() => {
  return `${API_BASE}/music/${props.music.id}/stream`
})

onMounted(() => {
  if (audioPlayer.value) {
    audioPlayer.value.play().catch(() => {})
  }
})
</script>

<style lang="scss" scoped>
.player-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(12px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.player-modal {
  width: 90%;
  max-width: 500px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 24px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  overflow: hidden;
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    padding-right: 16px;
  }

  .close-btn {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.15);
    border-radius: 10px;
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
      color: #f8fafc;
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.player-body {
  padding: 40px 24px;
}

.music-visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;

  .visual-icon {
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.05) 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid rgba(16, 185, 129, 0.3);

    svg {
      width: 56px;
      height: 56px;
      color: #10b981;
    }
  }

  .visual-waves {
    display: flex;
    gap: 4px;
    align-items: center;
    height: 40px;

    span {
      width: 4px;
      height: 100%;
      background: linear-gradient(to top, #10b981, #34d399);
      border-radius: 2px;
      animation: wave 1s ease-in-out infinite;
    }
  }
}

audio {
  width: 100%;
  height: 48px;
  border-radius: 8px;
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(1); }
}
</style>
