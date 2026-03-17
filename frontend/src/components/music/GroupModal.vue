<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card glass" @click.stop>
      <div class="modal-header">
        <h3>切换分组</h3>
        <button class="close-btn" @click="$emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="form-group">
          <label>选择分组</label>
          <div class="group-list">
            <div
              v-for="group in groups"
              :key="group.id"
              class="group-item"
              :class="{ active: selectedGroupId === group.id }"
              @click="selectedGroupId = group.id"
            >
              <span class="group-name">{{ group.name }}</span>
              <span v-if="selectedGroupId === group.id" class="check-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="modal-btn secondary" @click="$emit('close')">取消</button>
        <button
          class="modal-btn primary"
          :disabled="isSaving"
          @click="save"
        >
          <span v-if="isSaving" class="btn-spinner"></span>
          <span v-else>确定</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  music: {
    type: Object,
    required: true
  },
  groups: {
    type: Array,
    default: () => []
  },
  isSaving: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'save'])

const selectedGroupId = ref(null)

watch(() => props.music, (newMusic) => {
  if (newMusic) {
    selectedGroupId.value = newMusic.group_id
  }
}, { immediate: true })

function save() {
  emit('save', selectedGroupId.value)
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
  max-width: 420px;
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
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);

  h3 {
    font-size: 1.2rem;
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
    background: transparent;
    border: none;
    color: #64748b;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.2s;

    &:hover {
      color: #f8fafc;
      background: rgba(255, 255, 255, 0.05);
    }

    svg {
      width: 18px;
      height: 18px;
    }
  }
}

.modal-body {
  padding: 24px;
}

.form-group {
  label {
    display: block;
    margin-bottom: 12px;
    font-size: 0.9rem;
    color: #94a3b8;
  }
}

.group-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 280px;
  overflow-y: auto;

  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.2);
    border-radius: 2px;
  }
}

.group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.3);
  }

  &.active {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.4);

    .group-name {
      color: #f8fafc;
    }
  }

  .group-name {
    font-size: 0.95rem;
    color: #94a3b8;
  }

  .check-icon {
    width: 20px;
    height: 20px;
    color: #6366f1;

    svg {
      width: 100%;
      height: 100%;
    }
  }
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid rgba(99, 102, 241, 0.1);

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

    &.primary {
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      border: none;
      color: white;
      box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);

      &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px -4px rgba(99, 102, 241, 0.5);
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
