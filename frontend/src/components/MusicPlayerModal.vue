<template>
  <div v-if="show" class="modal-overlay player-overlay" @click.self="close">
    <div class="player-modal">
      <div class="player-header">
        <h3>{{ music?.original_name }}</h3>
        <button class="close-btn" @click="close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
      <div class="player-body">
        <div class="audio-player-container">
          <div class="music-cover">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 18V5l12-2v13"/>
              <circle cx="6" cy="18" r="3"/>
              <circle cx="18" cy="16" r="3"/>
            </svg>
          </div>
          <audio
            v-if="music"
            :src="musicUrl"
            controls
            autoplay
            class="audio-player"
          ></audio>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: Boolean,
  music: Object,
  apiBase: {
    type: String,
    default: 'http://localhost:8000'
  }
})

const emit = defineEmits(['close'])

const musicUrl = computed(() => {
  if (!props.music) return ''
  return `${props.apiBase}${props.music.url}`
})

function close() {
  emit('close')
}
</script>

<style lang="scss" scoped>
.player-overlay {
  background: rgba(0, 0, 0, 0.9);
}

.player-modal {
  width: 100%;
  max-width: 500px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
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
    margin-right: 16px;
  }

  .close-btn {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 8px;
    color: #64748b;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      color: #f8fafc;
    }

    svg {
      width: 16px;
      height: 16px;
    }
  }
}

.player-body {
  padding: 40px 24px;
}

.audio-player-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

.music-cover {
  width: 180px;
  height: 180px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.3);
  animation: pulse 2s ease-in-out infinite;

  svg {
    width: 80px;
    height: 80px;
    color: #10b981;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.3);
  }
  50% {
    transform: scale(1.02);
    box-shadow: 0 25px 50px -10px rgba(16, 185, 129, 0.4);
  }
}

.audio-player {
  width: 100%;
  height: 50px;
  border-radius: 25px;
  background: rgba(15, 23, 42, 0.6);
  outline: none;

  &::-webkit-media-controls-panel {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 25px;
  }
}
</style>
