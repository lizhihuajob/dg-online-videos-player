<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card glass" @click.stop>
      <div class="modal-header">
        <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <h3>确认删除</h3>
      </div>

      <div class="modal-body">
        <p class="warning-text">确定要删除 <strong>{{ music?.original_name }}</strong> 吗？</p>
        <p class="hint-text">此操作不可恢复</p>
      </div>

      <div class="modal-footer">
        <button class="modal-btn secondary" @click="$emit('close')">取消</button>
        <button
          class="modal-btn danger"
          :disabled="isDeleting"
          @click="$emit('confirm')"
        >
          <span v-if="isDeleting" class="btn-spinner"></span>
          <span v-else>删除</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  music: {
    type: Object,
    default: null
  },
  isDeleting: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close', 'confirm'])
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
  max-width: 380px;
  background: linear-gradient(145deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-radius: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  overflow: hidden;

  &.glass {
    backdrop-filter: blur(16px);
  }
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 28px 24px 16px;

  .warning-icon {
    width: 56px;
    height: 56px;
    color: #f59e0b;
    margin-bottom: 16px;
    filter: drop-shadow(0 0 15px rgba(245, 158, 11, 0.3));
  }

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
  }
}

.modal-body {
  padding: 0 24px 24px;
  text-align: center;

  .warning-text {
    font-size: 1rem;
    color: #e2e8f0;
    margin: 0 0 8px 0;
    line-height: 1.5;

    strong {
      color: #f8fafc;
    }
  }

  .hint-text {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
  }
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;

  .modal-btn {
    flex: 1;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s ease;

    &.secondary {
      background: rgba(51, 65, 85, 0.6);
      border: none;
      color: #94a3b8;

      &:hover {
        background: rgba(71, 85, 105, 0.8);
        color: #f8fafc;
      }
    }

    &.danger {
      background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      border: none;
      color: white;
      box-shadow: 0 4px 15px -3px rgba(239, 68, 68, 0.4);

      &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px -4px rgba(239, 68, 68, 0.5);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    }
  }
}

.btn-spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
