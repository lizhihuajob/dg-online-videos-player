<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3>切换分组</h3>
        <button class="close-btn" @click="close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <label>选择分组</label>
          <select v-model="selectedGroupId" class="group-select">
            <option :value="0">取消分组</option>
            <option v-for="group in groups" :key="group.id" :value="group.id">
              {{ group.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn secondary" @click="close">取消</button>
        <button
          class="btn primary"
          :disabled="isSaving"
          @click="save"
        >
          <span v-if="isSaving" class="btn-spinner"></span>
          <span v-else>保存</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  music: Object,
  groups: Array
})

const emit = defineEmits(['close', 'save'])

const selectedGroupId = ref(0)
const isSaving = ref(false)

watch(() => props.music, (newMusic) => {
  if (newMusic) {
    selectedGroupId.value = newMusic.group_id || 0
  }
}, { immediate: true })

function save() {
  isSaving.value = true
  emit('save', {
    groupId: selectedGroupId.value,
    onFinally: () => {
      isSaving.value = false
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
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f8fafc;
    margin: 0;
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

.modal-body {
  padding: 24px;
}

.form-group {
  label {
    display: block;
    margin-bottom: 8px;
    font-size: 0.9rem;
    color: #e2e8f0;
  }

  .group-select {
    width: 100%;
    padding: 12px 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 10px;
    color: #f8fafc;
    font-size: 0.95rem;
    outline: none;
    cursor: pointer;

    &:focus {
      border-color: rgba(99, 102, 241, 0.5);
    }

    option {
      background: #1e293b;
      color: #f8fafc;
    }
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.btn {
  padding: 10px 20px;
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

  &.primary {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    color: white;
    box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 8px 25px -5px rgba(99, 102, 241, 0.5);
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
