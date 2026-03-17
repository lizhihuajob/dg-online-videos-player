<template>
  <div v-if="show" class="modal-overlay" @click.self="onClose">
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
        <button class="btn secondary" @click="onClose">取消</button>
        <button
          class="btn danger"
          :disabled="isLoading"
          @click="handleConfirm"
        >
          <span v-if="isLoading" class="btn-spinner"></span>
          <span v-else>确认删除</span>
        </button>
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
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'confirm'])

function onClose() {
  emit('close')
}

function handleConfirm() {
  emit('confirm')
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

.modal-card {
  background: #1e293b;
  border-radius: 12px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  gap: 12px;

  h3 {
    margin: 0;
    color: #f8fafc;
    font-size: 1.25rem;
    font-weight: 600;
  }
}

.warning-icon {
  width: 24px;
  height: 24px;
  color: #f59e0b;
}

.modal-body {
  padding: 24px;
  color: #e2e8f0;
  line-height: 1.6;

  .warning-text {
    color: #f87171;
    margin-top: 8px;
    font-size: 0.95rem;
  }
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
