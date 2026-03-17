<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <div class="warning-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <h3>确认删除</h3>
      </div>

      <div class="modal-body">
        <p>确定要删除音乐 "<strong>{{ music?.original_name }}</strong>" 吗？</p>
        <p class="warning-text">此操作不可恢复，音乐文件将被永久删除。</p>
      </div>

      <div class="modal-footer">
        <button class="btn secondary" @click="close">取消</button>
        <button
          class="btn danger"
          :disabled="isDeleting"
          @click="confirmDelete"
        >
          <span v-if="isDeleting" class="btn-spinner"></span>
          <span v-else>确认删除</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  show: Boolean,
  music: Object
})

const emit = defineEmits(['close', 'confirm'])

const isDeleting = ref(false)

function confirmDelete() {
  isDeleting.value = true
  emit('confirm', {
    onFinally: () => {
      isDeleting.value = false
    }
  })
}

function close() {
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
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.modal-card {
  width: 100%;
  max-width: 420px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  .warning-icon {
    width: 48px;
    height: 48px;
    background: rgba(239, 68, 68, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;

    svg {
      width: 24px;
      height: 24px;
      color: #ef4444;
    }
  }

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
  }
}

.modal-body {
  padding: 24px;
  text-align: center;

  p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 8px;

    strong {
      color: #f8fafc;
    }
  }

  .warning-text {
    color: #ef4444;
    font-size: 0.85rem;
  }
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.btn {
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  &.secondary {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    color: #94a3b8;

    &:hover {
      background: rgba(99, 102, 241, 0.1);
      border-color: rgba(99, 102, 241, 0.3);
      color: #f8fafc;
    }
  }

  &.danger {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border: none;
    color: white;
    box-shadow: 0 4px 15px -3px rgba(239, 68, 68, 0.4);

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 8px 25px -5px rgba(239, 68, 68, 0.5);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }

  .btn-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
