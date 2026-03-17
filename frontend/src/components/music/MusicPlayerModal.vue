<template>
  <div v-if="show" class="modal-overlay player-overlay" @click.self="onClose">
    <div class="player-modal">
      <div class="player-header">
        <h3>{{ music?.original_name }}</h3>
        <button class="close-btn" @click="onClose">
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
            v-if="music && getMusicUrl(music)"
            :src="getMusicUrl(music)"
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
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  music: {
    type: Object,
    default: null
  },
  getMusicUrl: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['close'])

function onClose() {
  emit('close')
}
</script>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.player-overlay {
  background: rgba(0, 0, 0, 0.85);
}

.player-modal {
  background: #1e293b;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.player-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    margin: 0;
    color: #f8fafc;
    font-size: 1.25rem;
    font-weight: 600;
  }
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #f8fafc;
  }

  svg {
    width: 20px;
    height: 20px;
  }
}

.player-body {
  padding: 32px 24px;
}

.audio-player-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.music-cover {
  width: 120px;
  height: 120px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(99, 102, 241, 0.3);

  svg {
    width: 60px;
    height: 60px;
    color: rgba(99, 102, 241, 0.8);
  }
}

.audio-player {
  width: 100%;
  border-radius: 30px;
}
</style>
